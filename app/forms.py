from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Optional, URL

class BookForm(FlaskForm):
    """書籍表單"""
    title = StringField('書名', validators=[DataRequired(message='請輸入書名'), Length(max=200)])
    author = StringField('作者', validators=[Optional(), Length(max=100)])
    year = IntegerField('出版年份', validators=[Optional()])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    cover_url = StringField('封面圖片 URL', validators=[Optional(), URL(message='請輸入有效的網址'), Length(max=500)])
    category_id = SelectField('分類', coerce=int, validators=[Optional()])
    status = SelectField('閱讀狀態', choices=[('想讀', '想讀'), ('閱讀中', '閱讀中'), ('已讀完', '已讀完')], default='想讀')
    rating = IntegerField('評分 (1-5)', validators=[Optional()])
    submit = SubmitField('儲存')

class NoteForm(FlaskForm):
    """心得表單"""
    content = TextAreaField('心得內容', validators=[DataRequired(message='請輸入心得內容')])
    highlight = StringField('重點摘錄 (金句)', validators=[Optional()])
    start_date = DateField('開始閱讀日期', validators=[Optional()])
    finish_date = DateField('完成閱讀日期', validators=[Optional()])
    submit = SubmitField('儲存心得')

class CategoryForm(FlaskForm):
    """分類表單"""
    name = StringField('分類名稱', validators=[DataRequired(message='請輸入分類名稱'), Length(max=50)])
    color = StringField('代表顏色 (CSS 顏色)', validators=[Optional(), Length(max=20)])
    submit = SubmitField('新增分類')
