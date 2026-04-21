from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化資料庫
    db.init_app(app)

    # 註冊 Blueprint
    from .routes.main import main_bp
    from .routes.books import books_bp
    from .routes.notes import notes_bp
    from .routes.categories import categories_bp
    from .routes.search import search_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(search_bp)

    with app.app_context():
        db.create_all()

    return app
