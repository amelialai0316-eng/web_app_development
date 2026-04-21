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
        """
        建立心得筆記。
        :return: Note 物件 或 None
        """
        try:
            note = cls(book_id=book_id, content=content, highlight=highlight, start_date=start_date, finish_date=finish_date)
            db.session.add(note)
            db.session.commit()
            return note
        except Exception as e:
            db.session.rollback()
            print(f"建立心得失敗: {e}")
            return None

    @classmethod
    def get_all(cls, book_id=None):
        """
        取得心得清單。
        :param book_id: 指定書籍 ID (選填)
        """
        try:
            query = cls.query
            if book_id:
                query = query.filter_by(book_id=book_id)
            return query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"讀取心得清單失敗: {e}")
            return []

    @classmethod
    def get_by_id(cls, id):
        """
        依 ID 取得單一心得。
        """
        try:
            return cls.query.get(id)
        except Exception as e:
            print(f"讀取心得 {id} 失敗: {e}")
            return None

    def update(self, **kwargs):
        """
        更新心得內容。
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新心得失敗: {e}")
            return False

    def delete(self):
        """
        刪除此心得。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除心得失敗: {e}")
            return False
