from datetime import datetime
from . import db

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # 必修, 選修, 通識
    status = db.Column(db.String(50), nullable=False)    # 已完成, 修習中, 待修習
    score = db.Column(db.Float)                          # 百分制成績
    grade = db.Column(db.String(10))                     # 等級制成績
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, name, credits, category, status, score=None, grade=None):
        try:
            course = cls(
                name=name,
                credits=float(credits),
                category=category,
                status=status,
                score=float(score) if score else None,
                grade=grade
            )
            # 如果有 score 但沒 grade，或者有 grade 但沒 score，可以處理想法，但在這先簡單存
            db.session.add(course)
            db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            print(f"建立課程失敗: {e}")
            return None

    @classmethod
    def get_all(cls):
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"讀取課程清單失敗: {e}")
            return []

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.get(id)
        except Exception as e:
            print(f"讀取課程 {id} 失敗: {e}")
            return None

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    if key == 'credits' or key == 'score':
                        value = float(value) if value else None
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"更新課程失敗: {e}")
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"刪除課程失敗: {e}")
            return False

    @staticmethod
    def get_grade_points(grade, scale=4.3):
        """
        將等第成績轉換為積分
        """
        mapping_43 = {
            'A+': 4.3, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'F': 0.0, 'X': 0.0
        }
        mapping_40 = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'F': 0.0, 'X': 0.0
        }
        
        mapping = mapping_43 if scale == 4.3 else mapping_40
        return mapping.get(grade, 0.0)

    @staticmethod
    def score_to_grade(score):
        """
        將百分制轉換為等第
        """
        if score is None: return None
        if score >= 90: return 'A+'
        if score >= 85: return 'A'
        if score >= 80: return 'A-'
        if score >= 77: return 'B+'
        if score >= 73: return 'B'
        if score >= 70: return 'B-'
        if score >= 67: return 'C+'
        if score >= 63: return 'C'
        if score >= 60: return 'C-'
        return 'F'
