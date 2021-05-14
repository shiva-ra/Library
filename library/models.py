from datetime import datetime

from library import db

books = db.Table('books',
                 db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                 db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True)
                 )


class Book(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)


class Member(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Integer, nullable=True, default=0)
    books = db.relationship('Book', secondary=books, lazy='subquery',
                            backref=db.backref('members', lazy=True))


class Transaction(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'), nullable=False)
    book_id = db.Column(db.String(20), db.ForeignKey('book.id'), nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False)
    date_returned = db.Column(db.DateTime)
