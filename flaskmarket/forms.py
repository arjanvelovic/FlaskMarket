from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskmarket.models import User, Bid
from sqlalchemy import func

class SignUpForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired()])
    lastname = StringField('Last Name',
                           validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    phonenumber = StringField('Phone Number',
                           validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class SignInForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired()])
    lastname = StringField('Last Name',
                           validators=[DataRequired()])
    address = StringField('Address',
                           validators=[DataRequired()])
    phonenumber = StringField('Phone Number',
                           validators=[DataRequired(), Length(min=10, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class ItemForm(FlaskForm):
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
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    startingprice = DecimalField('Starting Price', places = 2, validators=[DataRequired()])
    category = SelectField('Categories', choices = CATEGORIES, validators=[DataRequired()])
    picture = FileField('Upload Item Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('List Item')

class BidForm(FlaskForm):
    currentbid = DecimalField('Place a Bid', validators=[DataRequired()])
    submit = SubmitField('Place Bid')

class WatchlistForm(FlaskForm):
    watching = BooleanField('Add to Watchlist')
    submit = SubmitField('Add to Watchlist')