from flask import render_template, request, Blueprint, redirect, url_for, current_app
from flaskmarket.models import Item
from flaskmarket.main.forms import SearchForm
from flaskmarket import db

main = Blueprint('main', __name__)

# @main.route("/")
# @main.route("/home", methods=['GET', 'POST'])
# def home():
#     page = request.args.get('page', 1, type=int)
#     items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
#     return render_template('home.html', items=items)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    if form.validate_on_submit():
        
        if form.ended.data == []:
            ended = False
        else:
            ended = True
        title = form.title.data
        category = form.category.data

        if title == '' and category == 'None':
            items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
        elif title == '' and category != 'None':
            items = Item.query.filter_by(category=category).order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
        elif title != '' and category == 'None':
            items = Item.query.filter_by(title=title).order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
        else:
            items = Item.query.filter_by(title=title, category=category).order_by(Item.enddate.desc()).paginate(page=page, per_page=5)

        current_app.logger.info(f'{form.title.raw_data}, {form.category.raw_data}, {ended}')

        return render_template('home.html', form=form, items = items)

    elif request.method == 'GET':
        # form.title.data = title
        # form.category.data = category
        # form.ended.data = ended

        items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
    
        return render_template('home.html', form=form, items = items)