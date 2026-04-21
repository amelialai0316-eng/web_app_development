from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.category import Category
from ..forms import CategoryForm

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories', methods=['GET', 'POST'])
def list_categories():
    """
    顯示分類管理頁面，兼具新增分類功能
    """
    form = CategoryForm()
    if form.validate_on_submit():
        if Category.create(name=form.name.data, color=form.color.data):
            flash('分類已建立！', 'success')
            return redirect(url_for('categories.list_categories'))
        else:
            flash('分類建立失敗（可能名稱已存在）。', 'danger')
            
    categories = Category.get_all()
    return render_template('categories/list.html', categories=categories, form=form)

@categories_bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除分類
    """
    category = Category.get_by_id(id)
    if category:
        # 檢查是否還有書籍使用此分類
        if category.books:
            flash('無法刪除：尚有書籍屬於此分類。請先更改該書籍的分類。', 'warning')
        elif category.delete():
            flash('分類已刪除。', 'success')
        else:
            flash('刪除失敗。', 'danger')
    return redirect(url_for('categories.list_categories'))
