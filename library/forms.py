from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired


class NewBook(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    total_quantity = IntegerField('Total Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewMember(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    balance = IntegerField('Balance')
    submit = SubmitField('Submit')


class IssueBook(FlaskForm):
    member_id = StringField('MemberId', validators=[DataRequired()])
    book_id = StringField('BookId', validators=[DataRequired()])
    date_issued = DateField('Date of Issue (MM-DD-YYYY)', format="%m-%d-%Y", validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReturnBook(FlaskForm):
    date_returned = DateField('Date of Return (MM-DD-YYYY)', format="%m-%d-%Y", validators=[DataRequired()])
    submit = SubmitField('Submit')


class SearchMember(FlaskForm):
    query = StringField('Type name of the Member')
    submit = SubmitField('Search')


class SearchBooks(FlaskForm):
    query = StringField('Type name or author of the book')
    submit = SubmitField('Search')


class SearchTransaction(FlaskForm):
    query = StringField('Type Transaction Id')
    submit = SubmitField('Search')