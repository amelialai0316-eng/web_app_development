from flask import Blueprint, render_template, request, redirect, url_for, flash

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories')
def list_categories():
    """
    顯示分類管理頁面
    渲染 categories/list.html。
    """
    pass

@categories_bp.route('/categories/create', methods=['POST'])
def create():
    """
    建立新分類
    """
    pass

@categories_bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除分類
    """
    pass
