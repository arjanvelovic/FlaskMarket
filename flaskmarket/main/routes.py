from flask import render_template, request, Blueprint
from flaskmarket.models import Item

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.enddate.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', items=items)

@main.route("/about")
def about():
    return render_template('about.html', title='About')