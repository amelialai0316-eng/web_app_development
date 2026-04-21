from flask import Blueprint, render_template, request

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def results():
    """
    全文搜尋功能
    接收參數 q 並對書名、作者、心得進行模糊搜尋。
    渲染 search/results.html。
    """
    pass
