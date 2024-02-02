from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    CATEGORIES = [
        (None,'--- select a category ---'),
        ('Business & Industrial','Business & Industrial'),
        ('Collectibles','Collectibles'),
        ('Electronics','Electronics'),
        ('Fashion','Fashion'),
        ('Home & Garden','Home & Garden'),
        ('Jewelry','Jewelry'),
        ('Motors','Motors'),
        ('Sporting Goods','Sporting Goods'),
        ('Toys','Toys'),
        ('Other','Other')
    ]
    title = StringField('Title')
    category = SelectField('Categories', choices = CATEGORIES)
    ended = BooleanField('Ended?')
    submit = SubmitField('Search Item')