from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.note import Note
from ..models.book import Book
from ..forms import NoteForm

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/books/<int:book_id>/notes/create', methods=['GET', 'POST'])
def create(book_id):
    """
    為特定書籍新增心得
    """
    book = Book.get_by_id(book_id)
    if not book:
        flash('找不到該書籍。', 'warning')
        return redirect(url_for('books.list_books'))
        
    form = NoteForm()
    if form.validate_on_submit():
        note = Note.create(
            book_id=book_id,
            content=form.content.data,
            highlight=form.highlight.data,
            start_date=form.start_date.data,
            finish_date=form.finish_date.data
        )
        if note:
            flash('心得已儲存。', 'success')
            return redirect(url_for('books.detail', id=book_id))
        else:
            flash('儲存失敗。', 'danger')
            
    return render_template('notes/create.html', form=form, book=book)

@notes_bp.route('/notes/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    編輯心得
    """
    note = Note.get_by_id(id)
    if not note:
        flash('找不到該心得。', 'warning')
        return redirect(url_for('books.list_books'))
        
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        success = note.update(
            content=form.content.data,
            highlight=form.highlight.data,
            start_date=form.start_date.data,
            finish_date=form.finish_date.data
        )
        if success:
            flash('心得已更新。', 'success')
            return redirect(url_for('books.detail', id=note.book_id))
        else:
            flash('更新失敗。', 'danger')
            
    return render_template('notes/edit.html', form=form, note=note)

@notes_bp.route('/notes/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除單筆心得
    """
    note = Note.get_by_id(id)
    if note:
        book_id = note.book_id
        if note.delete():
            flash('心得已刪除。', 'success')
        else:
            flash('刪除失敗。', 'danger')
        return redirect(url_for('books.detail', id=book_id))
    return redirect(url_for('books.list_books'))
