from datetime import datetime
from . import db

book_tag = db.Table('book_tag',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20))
    cover_url = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'))
    rating = db.Column(db.Integer)
    status = db.Column(db.String(20), nullable=False, default='想讀')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notes = db.relationship('Note', backref='book', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=book_tag, lazy='subquery', backref=db.backref('books', lazy=True))

    @classmethod
    def create(cls, title, author=None, year=None, isbn=None, cover_url=None, category_id=None, rating=None, status='想讀'):
        book = cls(
            title=title, author=author, year=year, isbn=isbn, cover_url=cover_url,
            category_id=category_id, rating=rating, status=status
        )
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
