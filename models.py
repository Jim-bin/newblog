# -*- coding:utf-8 -*_

from exts import db
from datetime import datetime


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     telephone = db.Column(db.String(11), nullable=False)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(100), nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    comments = db.relationship('Comment', backref='post')

    # author = db.relationship('User', backref=db.backref('question'))
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    reply_time = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # post = db.relationship('Post', backref=db.backref('comments', order_by=id.desc()))

    # author = db.relationship('User', backref=db.backref('comments'))
    # question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
