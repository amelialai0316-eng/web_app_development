from . import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(20))

    books = db.relationship('Book', backref='category', lazy=True)

    @classmethod
    def create(cls, name, color=None):
        """
        建立新的分類記錄。
        :param name: 分類名稱 (必填)
        :param color: 分類代表色 (選填)
        :return: Category 物件 或 None
        """
        try:
            category = cls(name=name, color=color)
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            print(f"建立分類失敗: {e}")
            return None

    @classmethod
    def get_all(cls):
        """
        取得所有分類。
        :return: Category 物件清單
        """
        try:
            return cls.query.all()
        except Exception as e:
            print(f"讀取分類列表失敗: {e}")
            return []

    @classmethod
    def get_by_id(cls, id):
        """
        依 ID 取得單一分類。
        :param id: 分類 ID
        :return: Category 物件 或 None
        """
        try:
            return cls.query.get(id)
        except Exception as e:
            print(f"讀取分類 {id} 失敗: {e}")
            return None

    def update(self, name=None, color=None):
        """
        更新分類資料。
        :param name: 新名稱
        :param color: 新顏色
        :return: Boolean 是否成功
        """
        try:
            if name:
                self.name = name
            if color:
                self.color = color
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新分類失敗: {e}")
            return False

    def delete(self):
        """
        刪除此分類。
        :return: Boolean 是否成功
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除分類失敗: {e}")
            return False
