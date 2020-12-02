from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(64), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan', passive_deletes = True)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(120), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    # order = db.relationship('Post',
    #                 backref = db.backref('user', cascade = 'all, delete-orphan')
    #             )