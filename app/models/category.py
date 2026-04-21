from . import db

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(20))

    books = db.relationship('Book', backref='category', lazy=True)

    @classmethod
    def create(cls, name, color=None):
        category = cls(name=name, color=color)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def update(self, name=None, color=None):
        if name:
            self.name = name
        if color:
            self.color = color
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
