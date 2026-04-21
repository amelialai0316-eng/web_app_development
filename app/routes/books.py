from flask import Blueprint, render_template, request, redirect, url_for, flash

books_bp = Blueprint('books', __name__)

@books_bp.route('/books')
def list_books():
    """
    顯示書籍列表
    支援依分類、評分篩選，並渲染 books/list.html。
    """
    pass

@books_bp.route('/books/create', methods=['GET', 'POST'])
def create():
    """
    新增書籍
    GET: 渲染 books/create.html。
    POST: 接收表單並建立書籍記錄。
    """
    pass

@books_bp.route('/books/<int:id>')
def detail(id):
    """
    顯示書籍詳情
    渲染 books/detail.html，包含書籍資訊與相關心得。
    """
    pass

@books_bp.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯書籍
    GET: 渲染帶有既有資料的 books/edit.html。
    POST: 更新資料庫記錄。
    """
    pass

@books_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除書籍
    從資料庫移除書籍及其關聯資料。
    """
    pass
