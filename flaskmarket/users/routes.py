from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flaskmarket import db, bcrypt
from flaskmarket.models import User, Item, Bid
from flaskmarket.users.forms import (SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from flaskmarket.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, address=form.address.data, phonenumber=form.phonenumber.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.signin'))
    return render_template('signup.html', title='Sign Up', form=form)


@users.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('signin.html', title='Sign In', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        form.phonenumber.data = current_user.phonenumber
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/useritems/<string:email>")
def user_items(email):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=email).first_or_404()
    if Item.query.filter_by(author=user).count() == 0:
        return render_template('empty.html', user=user, keyword = 'listings')
    else:
        items = Item.query.filter_by(author=user)\
            .order_by(Item.enddate.desc())\
            .paginate(page=page, per_page=5)
        return render_template('user_items.html', items=items, user=user)

@users.route("/userbids/<string:email>")
def user_bids(email):
    user = User.query.filter_by(email=email).first_or_404()
    allbids = Bid.query.filter_by(bidder=user)\
        .order_by(Bid.bidtime.desc())
    bids = []
    for bid in allbids:
        if bid.item.notactive == False:
            bids.append(bid)
    if len(bids) == 0:
        return render_template('empty.html', user=user, keyword = 'bids')
    else:
        return render_template('user_bids.html', bids=bids, user=user)
    
@users.route("/userpurchases/<string:email>")
def user_purchases(email):
    user = User.query.filter_by(email=email).first_or_404()
    allbids = Bid.query.filter_by(bidder=user)\
        .order_by(Bid.bidtime.desc())
    purchases = []
    for bid in allbids:
        if bid.item.hasbuyer:
            purchases.append(bid)
    # current_app.logger.info(f'{purchases}')
    if len(purchases) == 0:
        return render_template('empty.html', user=user, keyword = 'purchases')
    else:
        return render_template('user_purchases.html', purchases=purchases, user=user)
    

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.signin'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.signin'))
    return render_template('reset_token.html', title='Reset Password', form=form)