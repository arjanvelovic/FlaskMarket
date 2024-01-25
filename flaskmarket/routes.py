import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskmarket import app, db, bcrypt
from flaskmarket.forms import SignUpForm, SignInForm, UpdateAccountForm, ItemForm, BidForm, WatchlistForm
from flaskmarket.models import User, Item, Bid, Watchlist
from flask_login import login_user, current_user, logout_user, login_required
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from datetime import datetime

@app.route("/")
@app.route("/home")
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, address=form.address.data, phonenumber=form.phonenumber.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('signin.html', title='Sign In', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (175, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture2(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/item_pics', picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.address = form.address.data
        current_user.phonenumber = form.phonenumber.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        form.phonenumber.data = current_user.phonenumber
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/item/new", methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            item = Item(title=form.title.data, description=form.description.data, category=form.category.data, image_file=picture_file, startingprice=form.startingprice.data, author=current_user)
        else:
            item = Item(title=form.title.data, description=form.description.data, category=form.category.data, startingprice=form.startingprice.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_item.html', title='New Item',
                           form=form, legend='New Item')

@app.route("/item/<int:item_id>", methods=['GET', 'POST'])
def item(item_id):
    item = Item.query.get_or_404(item_id)

    bidform = BidForm()
    watchlistform = WatchlistForm()
    bidform.currentbid.validators = [NumberRange(min=item.startingprice+1, message='You must beat the current bid by at least $1')]
    # bidform.currentbid.data = item.startingprice+1

    # app.logger.info('this prints stuff')

    if current_user.is_authenticated:
        if bidform.validate_on_submit():
            if Bid.query.filter_by(item_id=item_id).all():
                bid = Bid.query.filter_by(item_id=item_id).first()
                bid.currentbid = bidform.currentbid.data
                bid.user_id = current_user.id
                bid.bidtime = datetime.utcnow()
            else:
                bid = Bid(currentbid=bidform.currentbid.data, item_id=item_id, user_id=current_user.id)
                db.session.add(bid)
            
            item.startingprice = bidform.currentbid.data
            db.session.commit()
            flash('You have the highest Bid', 'success')
            return redirect(url_for('item', item_id=item.id))
        
        watchlistform.watching.data = Watchlist.query.filter_by(item_id=item_id, user_id=current_user.id).all()

        if watchlistform.validate_on_submit():
            app.logger.info(watchlistform.watching.raw_data)
            if watchlistform.watching.raw_data:
                app.logger.info('added to watchlist')
                watchlist = Watchlist(watching = True, item_id=item_id, user_id=current_user.id)
                db.session.add(watchlist)
                flash('Added to Watch List', 'success')
            else:
                app.logger.info('deleted from watchlist')
                watchlist = Watchlist.query.filter_by(item_id=item_id, user_id=current_user.id).first()
                try:
                    db.session.delete(watchlist)
                    flash('Removed from Watch List', 'success')
                except:
                    print("Something else went wrong")

            db.session.commit()
            return redirect(url_for('item', item_id=item.id))

    return render_template('item.html', item=item, bidform=bidform, watchlistform = watchlistform)

@app.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        item.title = form.title.data
        item.content = form.content.data
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('item', item_id=item.id))
    elif request.method == 'GET':
        form.title.data = item.title
        form.content.data = item.content
    return render_template('create_post.html', title='Update Item',
                           form=form, legend='Update Item')


@app.route("/item/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('home'))