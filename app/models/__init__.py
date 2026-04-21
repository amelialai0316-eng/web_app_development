from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .category import Category
from .tag import Tag
from .book import Book, book_tag
from .note import Note
