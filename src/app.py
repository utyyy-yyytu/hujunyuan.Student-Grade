from flask import Flask, render_template, request, redirect, url_for, send_file
from models.student_model import StudentModel
from models.course_model import CourseModel
from models.score_model import ScoreModel

app = Flask(__name__)

# 首页
@app.route('/')
def index():
    student_count = StudentModel.count_students()
    course_count = CourseModel.count_courses()
    score_count = ScoreModel.count_scores()
    return render_template('index.html',
        student_count=student_count,
        course_count=course_count,
        score_count=score_count)

# 学生列表
@app.route('/students')
def student_list():
    keyword = request.args.get('keyword', '')
    if keyword:
        students = StudentModel.search_students(keyword)
    else:
        students = StudentModel.get_all_students()
    return render_template('students.html', students=students, keyword=keyword)

# 添加学生
@app.route('/students/add', methods=['GET', 'POST'])
def student_add():
    if request.method == 'POST':
        StudentModel.add_student(
            student_no=request.form['student_no'],
            name=request.form['name'],
            gender=request.form['gender'],
            birthday=request.form.get('birthday') or None,
            phone=request.form.get('phone') or None,
            email=request.form.get('email') or None,
            major=request.form.get('major') or None,
            grade_year=request.form.get('grade_year') or None
        )
        return redirect(url_for('student_list'))
    return render_template('student_form.html', student=None)

# 编辑学生
@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def student_edit(id):
    if request.method == 'POST':
        StudentModel.update_student(
            student_id=id,
            student_no=request.form['student_no'],
            name=request.form['name'],
            gender=request.form['gender'],
            birthday=request.form.get('birthday') or None,
            phone=request.form.get('phone') or None,
            email=request.form.get('email') or None,
            major=request.form.get('major') or None,
            grade_year=request.form.get('grade_year') or None
        )
        return redirect(url_for('student_list'))
    student = StudentModel.get_student_by_id(id)
    return render_template('student_form.html', student=student)

# 删除学生
@app.route('/students/delete/<int:id>')
def student_delete(id):
    StudentModel.delete_student(id)
    return redirect(url_for('student_list'))

# 课程列表
@app.route('/courses')
def course_list():
    keyword = request.args.get('keyword', '')
    if keyword:
        courses = CourseModel.search_courses(keyword)
    else:
        courses = CourseModel.get_all_courses()
    return render_template('courses.html', courses=courses, keyword=keyword)

# 添加课程
@app.route('/courses/add', methods=['GET', 'POST'])
def course_add():
    if request.method == 'POST':
        CourseModel.add_course(
            course_no=request.form['course_no'],
            course_name=request.form['course_name'],
            credit=request.form.get('credit') or 0,
            teacher=request.form.get('teacher') or None,
            description=request.form.get('description') or None
        )
        return redirect(url_for('course_list'))
    return render_template('course_form.html', course=None)

# 编辑课程
@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
def course_edit(id):
    if request.method == 'POST':
        CourseModel.update_course(
            course_id=id,
            course_no=request.form['course_no'],
            course_name=request.form['course_name'],
            credit=request.form.get('credit') or 0,
            teacher=request.form.get('teacher') or None,
            description=request.form.get('description') or None
        )
        return redirect(url_for('course_list'))
    course = CourseModel.get_course_by_id(id)
    return render_template('course_form.html', course=course)

# 删除课程
@app.route('/courses/delete/<int:id>')
def course_delete(id):
    CourseModel.delete_course(id)
    return redirect(url_for('course_list'))

# 成绩列表
@app.route('/scores')
def score_list():
    keyword = request.args.get('keyword', '')
    if keyword:
        scores = ScoreModel.search_scores(keyword)
    else:
        scores = ScoreModel.get_all_scores()
    return render_template('scores.html', scores=scores, keyword=keyword)

# 录入成绩
@app.route('/scores/add', methods=['GET', 'POST'])
def score_add():
    if request.method == 'POST':
        ScoreModel.add_score(
            student_id=request.form['student_id'],
            course_id=request.form['course_id'],
            usual_score=request.form.get('usual_score') or 0,
            exam_score=request.form.get('exam_score') or 0,
            term=request.form.get('term') or None,
            remark=request.form.get('remark') or None
        )
        return redirect(url_for('score_list'))
    students = StudentModel.get_all_students()
    courses = CourseModel.get_all_courses()
    return render_template('score_form.html', score=None, students=students, courses=courses)

# 编辑成绩
@app.route('/scores/edit/<int:id>', methods=['GET', 'POST'])
def score_edit(id):
    if request.method == 'POST':
        ScoreModel.update_score(
            score_id=id,
            student_id=request.form['student_id'],
            course_id=request.form['course_id'],
            usual_score=request.form.get('usual_score') or 0,
            exam_score=request.form.get('exam_score') or 0,
            term=request.form.get('term') or None,
            remark=request.form.get('remark') or None
        )
        return redirect(url_for('score_list'))
    score = ScoreModel.get_score_by_id(id)
    students = StudentModel.get_all_students()
    courses = CourseModel.get_all_courses()
    return render_template('score_form.html', score=score, students=students, courses=courses)

# 删除成绩
@app.route('/scores/delete/<int:id>')
def score_delete(id):
    ScoreModel.delete_score(id)
    return redirect(url_for('score_list'))

# 导出成绩为Excel
@app.route('/scores/export')
def score_export():
    from openpyxl import Workbook
    import io

    scores = ScoreModel.get_all_scores()

    wb = Workbook()
    ws = wb.active
    ws.title = '成绩表'

    headers = ['学号', '学生姓名', '课程编号', '课程名称', '平时成绩', '期末成绩', '总评成绩', '学期', '备注']
    ws.append(headers)

    for s in scores:
        ws.append([
            s['student_no'],
            s['student_name'],
            s['course_no'],
            s['course_name'],
            s['usual_score'],
            s['exam_score'],
            s['total_score'],
            s['term'] or '',
            s['remark'] or ''
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='成绩表.xlsx'
    )

# 数据统计
@app.route('/statistics')
def statistics():
    student_count = StudentModel.count_students()
    course_count = CourseModel.count_courses()
    score_count = ScoreModel.count_scores()

    courses = CourseModel.get_all_courses()
    bar_labels = []
    bar_data = []
    for c in courses:
        stats = ScoreModel.get_statistics_by_course(c['id'])
        if stats and stats['avg_score'] is not None:
            bar_labels.append(c['course_name'])
            bar_data.append(float(stats['avg_score']))

    all_scores = ScoreModel.get_all_scores()
    dist = {'优秀(90-100)': 0, '良好(80-89)': 0, '中等(70-79)': 0, '及格(60-69)': 0, '不及格(<60)': 0}
    for s in all_scores:
        total = s['total_score'] or 0
        if total >= 90:
            dist['优秀(90-100)'] += 1
        elif total >= 80:
            dist['良好(80-89)'] += 1
        elif total >= 70:
            dist['中等(70-79)'] += 1
        elif total >= 60:
            dist['及格(60-69)'] += 1
        else:
            dist['不及格(<60)'] += 1
    pie_data = [{"name": k, "value": v} for k, v in dist.items() if v > 0]

    selected_course = request.args.get('course_id', '')
    course_stats = None
    if selected_course:
        course_stats = ScoreModel.get_statistics_by_course(int(selected_course))

    rank_course = request.args.get('rank_course_id', '')
    ranking = []
    if rank_course:
        ranking = ScoreModel.get_rankings(course_id=int(rank_course))

    return render_template('statistics.html',
        student_count=student_count,
        course_count=course_count,
        score_count=score_count,
        bar_labels=bar_labels,
        bar_data=bar_data,
        pie_data=pie_data,
        courses=courses,
        course_stats=course_stats,
        selected_course=selected_course,
        ranking=ranking,
        rank_course=rank_course
    )

if __name__ == '__main__':
    app.run(debug=True)
