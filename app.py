from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    favorite = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    book = Book(title=title, author=author)
    db.session.add(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle_favorite/<int:book_id>')
def toggle_favorite(book_id):
    book = Book.query.get(book_id)
    book.favorite = not book.favorite
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/rate/<int:book_id>', methods=['POST'])
def rate(book_id):
    book = Book.query.get(book_id)
    book.rating = int(request.form['rating'])
    book.review = request.form['review']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
