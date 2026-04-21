from datetime import datetime
from . import db

class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text)
    highlight = db.Column(db.Text)
    start_date = db.Column(db.Date)
    finish_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, book_id, content=None, highlight=None, start_date=None, finish_date=None):
        note = cls(book_id=book_id, content=content, highlight=highlight, start_date=start_date, finish_date=finish_date)
        db.session.add(note)
        db.session.commit()
        return note

    @classmethod
    def get_all(cls, book_id=None):
        query = cls.query
        if book_id:
            query = query.filter_by(book_id=book_id)
        return query.order_by(cls.created_at.desc()).all()

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
