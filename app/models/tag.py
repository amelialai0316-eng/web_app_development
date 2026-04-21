from . import db

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def create(cls, name):
        """
        建立新的標籤。
        :param name: 標籤名稱 (唯一)
        :return: Tag 物件 或 None
        """
        try:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            print(f"建立標籤失敗: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有標籤。
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"讀取標籤列表失敗: {e}")
            return []

    @classmethod
    def get_by_id(cls, id):
        """
        依 ID 取得標籤。
        """
        try:
            return cls.query.get(id)
        except Exception as e:
            print(f"讀取標籤 {id} 失敗: {e}")
            return None

    def update(self, name):
        """
        更新標籤名稱。
        """
        try:
            self.name = name
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新標籤失敗: {e}")
            return False

    def delete(self):
        """
        刪除標籤。
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除標籤失敗: {e}")
            return False
