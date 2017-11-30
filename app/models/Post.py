from app.instances.db import db
from sqlalchemy.dialects.mysql import LONGTEXT
from config import posts
import datetime

# noinspection PyUnresolvedReferences
import app.models.Category


post_categories = db.Table(
    'post_categories',
    db.metadata,
    db.Column('category_name', db.Integer, db.ForeignKey('categories.name'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


class Post(db.Model):
    """
    Represnts a post (e.g. challenge)
    """

    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(posts['max_title']), nullable=False)
    body = db.Column(LONGTEXT, nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    categories = db.relationship('Category', secondary='post_categories', backref='posts', lazy='dynamic')

    def to_json(self):
        return {
            'title': self.title,
            'body': self.body,
            'owner': self.user.to_json()
        }
    
    def __repr__(self):
        return '<Post(%r) by %r>' % (self.id, self.user.name)
