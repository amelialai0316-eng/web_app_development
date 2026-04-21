from flask import Blueprint, render_template, request
from ..models.book import Book
from ..models.note import Note
from sqlalchemy import or_

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def results():
    """
    全文搜尋功能
    接收參數 q 並對書名、作者、心得進行模糊搜尋。
    渲染 search/results.html。
    """
    query = request.args.get('q', '')
    if not query:
        return render_template('search/results.html', books=[], query='')
        
    # 搜尋書籍（標題或作者）
    books_found = Book.query.filter(
        or_(
            Book.title.contains(query),
            Book.author.contains(query)
        )
    ).all()
    
    # 搜尋心得內容
    notes_found = Note.query.filter(Note.content.contains(query)).all()
    
    # 取得心得所屬的書籍（扣除重複）
    books_from_notes = [n.book for n in notes_found if n.book not in books_found]
    
    all_results = books_found + books_from_notes
    
    return render_template('search/results.html', books=all_results, query=query)
