from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁 / 儀表板
    渲染 index.html，包含閱讀統計與近期筆記。
    """
    pass
