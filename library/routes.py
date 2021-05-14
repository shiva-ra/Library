from uuid import uuid4

from flask import render_template, flash, url_for, redirect, request
from library import app, db
from library.forms import NewBook, NewMember, IssueBook, ReturnBook, SearchMember, SearchBooks, SearchTransaction
from library.models import Book, Member, Transaction


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchBooks()
    if form.validate_on_submit() and form.query.data:
        books = Book.query.filter((Book.name == form.query.data) | (Book.author == form.query.data)).all()
    else:
        books = Book.query.all()
    return render_template('home.html', books=books, form=form)


@app.route("/about")
def about():
    return "about page"


@app.route("/books/new", methods=['GET', 'POST'])
def new_book():
    form = NewBook()
    if form.validate_on_submit():
        book = Book(id=str(uuid4())[-6:],
                    name=form.name.data,
                    author=form.author.data,
                    description=form.description.data,
                    quantity=form.quantity.data,
                    total_quantity=form.total_quantity.data)
        db.session.add(book)
        db.session.commit()
        flash('Book has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', title='New Book',
                           form=form, legend='New Book')


@app.route("/book/<book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.name, book=book)


@app.route("/book/<book_id>/update", methods=['GET', 'POST'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = NewBook()
    if form.validate_on_submit():
        book.name = form.name.data
        book.author = form.author.data
        book.description = form.description.data
        book.quantity = form.quantity.data
        book.total_quantity = form.total_quantity.data
        db.session.commit()
        flash('Book has been updated!', 'success')
        return redirect(url_for('book', book_id=book.id))

    elif request.method == 'GET':
        form.name.data = book.name
        form.author.data = book.author
        form.description.data = book.description
        form.quantity.data = book.quantity
        form.total_quantity.data = book.total_quantity
    return render_template('add_book.html', title='Update Book',
                           form=form, legend='Update Book')


@app.route("/book/<book_id>/delete", methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book has been Deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/members", methods=['GET', 'POST'])
def members():
    form = SearchMember()
    if form.validate_on_submit() and form.query.data:
        members = Member.query.filter_by(name=form.query.data)

    else:
        members = Member.query.all()
    return render_template('members.html', members=members, form=form)


@app.route("/member/<member_id>", methods=['GET', 'POST'])
def member(member_id):
    member = Member.query.get_or_404(member_id)
    return render_template('member.html', title=member.name, member=member)


@app.route("/members/new", methods=['GET', 'POST'])
def new_member():
    form = NewMember()
    if form.validate_on_submit():
        member = Member(id=str(uuid4())[-6:],
                        name=form.name.data,
                        address=form.address.data,
                        balance=form.balance.data)
        db.session.add(member)
        db.session.commit()
        flash('Member has been created!', 'success')
        return redirect(url_for('members'))
    return render_template('add_member.html', title='New Member',
                           form=form, legend='New Member')


@app.route("/member/<member_id>/update", methods=['GET', 'POST'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    form = NewMember()
    if form.validate_on_submit():
        member.name = form.name.data
        member.address = form.address.data
        member.balance = form.balance.data
        db.session.commit()
        flash('Member has been updated!', 'success')
        return redirect(url_for('member', member_id=member.id))

    elif request.method == 'GET':
        form.name.data = member.name
        form.address.data = member.address
        form.balance.data = member.balance

    return render_template('add_member.html', title='Update Member',
                           form=form, legend='Update Member')


@app.route("/member/<member_id>/delete", methods=['GET', 'POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash('Member has been Deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/issue_book", methods=['GET', 'POST'])
def issue_book():
    form = IssueBook()
    if form.validate_on_submit():
        member = Member.query.get_or_404(form.member_id.data)
        book = Book.query.get_or_404(form.book_id.data)

        if member.balance <= 500 and book.quantity > 0:
            book.quantity -= 1
            member.books.append(book)
            trans = Transaction(id=str(uuid4())[-6:],
                                member_id=form.member_id.data,
                                book_id=form.book_id.data,
                                date_issued=form.date_issued.data)

            db.session.add(trans)
            db.session.commit()
            flash('Book Issued!', 'success')
            return redirect(url_for('home'))

        else:
            flash('Book Could Not be Issued!', 'danger')
    return render_template('issue_book.html', title='Issue Book',
                           form=form, legend='Issue Book')


@app.route("/transactions", methods=['GET', 'POST'])
def transactions():
    form = SearchTransaction()
    if form.validate_on_submit() and form.query.data:
        trans = Transaction.query.filter_by(id=form.query.data)
    else:
        trans = Transaction.query.all()
    return render_template('transactions.html', trans=trans, form=form)


@app.route("/transaction/<transaction_id>", methods=['GET', 'POST'])
def transaction(transaction_id):

    form = ReturnBook()
    trans = Transaction.query.filter_by(id=transaction_id).first()
    if form.validate_on_submit() and form.date_returned.data:
        book = Book.query.get_or_404(trans.book_id)
        member = Member.query.get_or_404(trans.member_id)
        try:
            member.books.remove(book)
        except ValueError:
            pass
        trans.date_returned = form.date_returned.data
        book.quantity += 1
        db.session.commit()
        member.balance += (trans.date_returned - trans.date_issued).days * 10
        db.session.commit()
        flash('Book Returned!', 'success')
    return render_template('transaction.html', trans=trans, form=form)


@app.route("/return_book", methods=['GET', 'POST'])
def return_book():
    form = SearchTransaction()
    if form.validate_on_submit() and form.query.data:
        trans = Transaction.query.get_or_404(form.query.data)
        book = Book.query.get_or_404(trans.book_id)
        member = Member.query.get_or_404(trans.member_id)

        trans.date_returned = form.date_returned.data
        book.quantity += 1
        member.balance += (trans.date_returned - trans.date_issued).days * 10
        db.session.commit()
        flash('Book Returned!', 'success')
        return redirect(url_for('home'))

    return render_template('return_book.html', title='Issue Book',
                           form=form, legend='Issue Book')
