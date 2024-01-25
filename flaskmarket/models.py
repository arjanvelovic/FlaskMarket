from datetime import datetime, timedelta
from flaskmarket import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Item', backref='author', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)
    watching = db.relationship('Watchlist', backref='watcher', lazy=True)

    def __repr__(self):
        return f"User{self.id}('{self.firstname}', '{self.email}', '{self.datecreated}')"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default2.jpg')
    startingprice = db.Column(db.Numeric, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listeddate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    enddate = db.Column(db.DateTime, nullable=False, default=(datetime.utcnow() + timedelta(days=7) - timedelta(hours=5)))
    active = db.Column(db.Boolean, nullable = False, default = True)
    bids = db.relationship('Bid', backref='item', lazy=True)
    watches = db.relationship('Watchlist', backref='item', lazy=True)

    def __repr__(self):
        return f"Item{self.id}('{self.title}', '{self.user_id}', '{self.listeddate}', '{self.enddate}', '{self.bids}')"
    
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentbid = db.Column(db.Numeric, nullable=False)
    bidtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bid{self.id}('{self.currentbid}', '{self.item_id}', '{self.user_id}')"
    
class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watching = db.Column(db.Boolean, nullable=False, default=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bid{self.id}('{self.watching}', '{self.item_id}', '{self.user_id}')"