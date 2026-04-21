from flask import Blueprint, render_template
from ..models.book import Book
from ..models.note import Note
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁 / 儀表板
    渲染 index.html，包含閱讀統計與近期筆記。
    """
    stats = {
        'total_books': Book.query.count(),
        'finished_books': Book.query.filter_by(status='已讀完').count(),
        'avg_rating': Book.query.with_entities(func.avg(Book.rating)).scalar() or 0
    }
    recent_notes = Note.query.order_by(Note.created_at.desc()).limit(5).all()
    return render_template('index.html', stats=stats, recent_notes=recent_notes)
