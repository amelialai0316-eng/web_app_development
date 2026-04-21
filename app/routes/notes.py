from flask import Blueprint, render_template, request, redirect, url_for, flash

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/books/<int:book_id>/notes/create', methods=['GET', 'POST'])
def create(book_id):
    """
    為特定書籍新增心得
    GET: 渲染 notes/create.html。
    POST: 建立新的筆記記錄。
    """
    pass

@notes_bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯心得
    GET: 渲染 notes/edit.html。
    POST: 更新筆記記錄。
    """
    pass

@notes_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除單筆心得
    """
    pass
