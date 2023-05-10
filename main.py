import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from forms import Form, EditForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)


#Database
db = SQLAlchemy(app)
class Books(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    rating = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"<Books {self.title}>"



app.app_context().push()



#Render Books
@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books = all_books)

#Add books
@app.route("/add", methods= ["POST", "GET"])
def add():
    form = Form()
    if form.validate_on_submit():
        new_book = Books(title= form.title.data, author= form.author.data, rating= form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form = form)

#Edit Books
@app.route("/edit/<int:id>", methods = ["POST", "GET"])
def edit(id):
    form =EditForm()
    all_books = db.session.query(Books).all()
    if form.validate_on_submit():
        book_to_update = Books.query.get(id)
        book_to_update.title = form.title.data
        book_to_update.author = form.author.data
        book_to_update.rating = form.rating.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", id=id, books=all_books, form=form)

#Delete Books
@app.route("/delete/<int:id>")
def delete(id):
    book_to_delete = Books.query.get(id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

