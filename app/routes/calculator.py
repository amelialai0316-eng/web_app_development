from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.course import Course
from ..models import db

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/calculator')
def index():
    """
    計分引擎儀表板：顯示學分統計與 GPA
    """
    courses = Course.get_all()
    
    # 計算統計數據
    total_credits = sum(c.credits for c in courses)
    completed_credits = sum(c.credits for c in courses if c.status == '已完成')
    studying_credits = sum(c.credits for c in courses if c.status == '修習中')
    pending_credits = sum(c.credits for c in courses if c.status == '待修習')
    
    # GPA 計算 (僅針對已完成且有成績的課程)
    completed_with_grade = [c for c in courses if c.status == '已完成' and (c.grade or c.score)]
    
    def calculate_gpa(scale):
        total_points = 0
        total_gpa_credits = 0
        for c in completed_with_grade:
            grade = c.grade
            if not grade and c.score is not None:
                grade = Course.score_to_grade(c.score)
            
            if grade:
                points = Course.get_grade_points(grade, scale=scale)
                total_points += points * c.credits
                total_gpa_credits += c.credits
        
        return round(total_points / total_gpa_credits, 2) if total_gpa_credits > 0 else 0.0

    gpa_43 = calculate_gpa(4.3)
    gpa_40 = calculate_gpa(4.0)
    
    current_scale = session.get('gpa_scale', 4.3)
    display_gpa = gpa_43 if current_scale == 4.3 else gpa_40

    return render_template('calculator/index.html', 
                           courses=courses,
                           total_credits=total_credits,
                           completed_credits=completed_credits,
                           studying_credits=studying_credits,
                           pending_credits=pending_credits,
                           gpa_43=gpa_43,
                           gpa_40=gpa_40,
                           display_gpa=display_gpa,
                           current_scale=current_scale)

@calculator_bp.route('/calculator/add', methods=['GET', 'POST'])
def add_course():
    """
    新增課程：GET 顯示表單，POST 處理資料儲存
    """
    if request.method == 'POST':
        name = request.form.get('name')
        credits = request.form.get('credits')
        category = request.form.get('category')
        status = request.form.get('status')
        score = request.form.get('score')
        grade = request.form.get('grade')
        
        if not name or not credits or not category or not status:
            flash('請填寫所有必填欄位', 'danger')
            return render_template('calculator/add.html')
        
        # 自動轉換成績
        if score and not grade:
            grade = Course.score_to_grade(float(score))
        
        course = Course.create(name, credits, category, status, score, grade)
        if course:
            flash(f'課程 {name} 已新增', 'success')
            return redirect(url_for('calculator.index'))
        else:
            flash('新增失敗，請檢查輸入格式', 'danger')
    
    return render_template('calculator/add.html')

@calculator_bp.route('/calculator/edit/<int:id>', methods=['GET'])
def edit_course(id):
    """
    編輯課程：顯示特定課程的編輯表單
    """
    course = Course.get_by_id(id)
    if not course:
        flash('找不到該課程', 'warning')
        return redirect(url_for('calculator.index'))
    return render_template('calculator/edit.html', course=course)

@calculator_bp.route('/calculator/update/<int:id>', methods=['POST'])
def update_course(id):
    """
    更新課程：執行資料庫更新操作
    """
    course = Course.get_by_id(id)
    if not course:
        flash('找不到該課程', 'warning')
        return redirect(url_for('calculator.index'))
    
    name = request.form.get('name')
    credits = request.form.get('credits')
    category = request.form.get('category')
    status = request.form.get('status')
    score = request.form.get('score')
    grade = request.form.get('grade')
    
    # 自動轉換
    if score and not grade:
        grade = Course.score_to_grade(float(score))
    
    success = course.update(name=name, credits=credits, category=category, 
                            status=status, score=score, grade=grade)
    
    if success:
        flash('課程已更新', 'success')
    else:
        flash('更新失敗', 'danger')
        
    return redirect(url_for('calculator.index'))

@calculator_bp.route('/calculator/delete/<int:id>', methods=['POST'])
def delete_course(id):
    """
    刪除課程：執行資料庫刪除操作
    """
    course = Course.get_by_id(id)
    if course:
        course.delete()
        flash('課程已刪除', 'info')
    return redirect(url_for('calculator.index'))

@calculator_bp.route('/calculator/toggle-scale', methods=['POST'])
def toggle_scale():
    """
    切換 GPA 計算標準 (4.0/4.3)
    """
    current = session.get('gpa_scale', 4.3)
    new_scale = 4.0 if current == 4.3 else 4.3
    session['gpa_scale'] = new_scale
    flash(f'已切換至 {new_scale} 分制', 'info')
    return redirect(url_for('calculator.index'))
