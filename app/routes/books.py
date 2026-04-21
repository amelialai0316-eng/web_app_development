from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.book import Book
from ..models.category import Category
from ..forms import BookForm
from ..models import db

books_bp = Blueprint('books', __name__)

@books_bp.route('/books')
def list_books():
    """
    顯示書籍列表
    支援依分類、評分篩選，並渲染 books/list.html。
    """
    category_id = request.args.get('category_id', type=int)
    rating = request.args.get('rating', type=int)
    
    query = Book.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if rating:
        query = query.filter_by(rating=rating)
    
    books = query.order_by(Book.created_at.desc()).all()
    categories = Category.get_all()
    return render_template('books/list.html', books=books, categories=categories)

@books_bp.route('/books/create', methods=['GET', 'POST'])
def create():
    """
    新增書籍
    GET: 渲染 books/create.html。
    POST: 接收表單並建立書籍記錄。
    """
    form = BookForm()
    # 動態載入分類選項
    form.category_id.choices = [(0, '未分類')] + [(c.id, c.name) for c in Category.get_all()]
    
    if form.validate_on_submit():
        category_id = form.category_id.data if form.category_id.data != 0 else None
        book = Book.create(
            title=form.title.data,
            author=form.author.data,
            year=form.year.data,
            isbn=form.isbn.data,
            cover_url=form.cover_url.data,
            category_id=category_id,
            rating=form.rating.data,
            status=form.status.data
        )
        if book:
            flash('成功新增書籍！', 'success')
            return redirect(url_for('books.list_books'))
        else:
            flash('新增書籍失敗，請稍後再試。', 'danger')
            
    return render_template('books/create.html', form=form)

@books_bp.route('/books/<int:id>')
def detail(id):
    """
    顯示書籍詳情
    渲染 books/detail.html，包含書籍資訊與相關心得。
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('books.list_books'))
    return render_template('books/detail.html', book=book)

@books_bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯書籍
    GET: 渲染帶有既有資料的 books/edit.html。
    POST: 更新資料庫記錄。
    """
    book = Book.get_by_id(id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('books.list_books'))
        
    form = BookForm(obj=book)
    form.category_id.choices = [(0, '未分類')] + [(c.id, c.name) for c in Category.get_all()]
    
    if form.validate_on_submit():
        category_id = form.category_id.data if form.category_id.data != 0 else None
        success = book.update(
            title=form.title.data,
            author=form.author.data,
            year=form.year.data,
            isbn=form.isbn.data,
            cover_url=form.cover_url.data,
            category_id=category_id,
            rating=form.rating.data,
            status=form.status.data
        )
        if success:
            flash('書籍資料已更新。', 'success')
            return redirect(url_for('books.detail', id=book.id))
        else:
            flash('更新失敗。', 'danger')
            
    # 設定目前的分類 ID
    if not request.method == 'POST':
        form.category_id.data = book.category_id if book.category_id else 0
        
    return render_template('books/edit.html', form=form, book=book)

@books_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除書籍
    從資料庫移除書籍及其關聯資料。
    """
    book = Book.get_by_id(id)
    if book:
        if book.delete():
            flash('書籍已刪除。', 'success')
        else:
            flash('刪除失敗。', 'danger')
    else:
        flash('找不到該書籍。', 'warning')
    return redirect(url_for('books.list_books'))
