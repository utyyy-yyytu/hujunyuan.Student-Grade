from flask import Flask, render_template, request, redirect, url_for
from models.database import get_db, init_db

app = Flask(__name__)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 学生列表
@app.route('/students')
def student_list():
    keyword = request.args.get('keyword', '')
    db = get_db()
    if keyword:
        students = db.execute(
            "SELECT * FROM student WHERE stu_no LIKE ? OR name LIKE ?",
            (f'%{keyword}%', f'%{keyword}%')
        ).fetchall()
    else:
        students = db.execute("SELECT * FROM student").fetchall()
    db.close()
    return render_template('students.html', students=students, keyword=keyword)

# 添加学生
@app.route('/students/add', methods=['GET', 'POST'])
def student_add():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO student (stu_no, name, gender, class_name, phone) VALUES (?, ?, ?, ?, ?)",
            (request.form['stu_no'], request.form['name'],
             request.form['gender'], request.form['class_name'], request.form['phone'])
        )
        db.commit()
        db.close()
        return redirect(url_for('student_list'))
    return render_template('student_form.html', student=None)

# 编辑学生
@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def student_edit(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE student SET stu_no=?, name=?, gender=?, class_name=?, phone=? WHERE id=?",
            (request.form['stu_no'], request.form['name'],
             request.form['gender'], request.form['class_name'], request.form['phone'], id)
        )
        db.commit()
        db.close()
        return redirect(url_for('student_list'))
    student = db.execute("SELECT * FROM student WHERE id=?", (id,)).fetchone()
    db.close()
    return render_template('student_form.html', student=student)

# 删除学生
@app.route('/students/delete/<int:id>')
def student_delete(id):
    db = get_db()
    db.execute("DELETE FROM student WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('student_list'))

# 课程列表
@app.route('/courses')
def course_list():
    db = get_db()
    courses = db.execute("SELECT * FROM course").fetchall()
    db.close()
    return render_template('courses.html', courses=courses)

# 添加课程
@app.route('/courses/add', methods=['GET', 'POST'])
def course_add():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            "INSERT INTO course (course_no, name, credit, teacher) VALUES (?, ?, ?, ?)",
            (request.form['course_no'], request.form['name'],
             request.form['credit'], request.form['teacher'])
        )
        db.commit()
        db.close()
        return redirect(url_for('course_list'))
    return render_template('course_form.html', course=None)

# 编辑课程
@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
def course_edit(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE course SET course_no=?, name=?, credit=?, teacher=? WHERE id=?",
            (request.form['course_no'], request.form['name'],
             request.form['credit'], request.form['teacher'], id)
        )
        db.commit()
        db.close()
        return redirect(url_for('course_list'))
    course = db.execute("SELECT * FROM course WHERE id=?", (id,)).fetchone()
    db.close()
    return render_template('course_form.html', course=course)

# 删除课程
@app.route('/courses/delete/<int:id>')
def course_delete(id):
    db = get_db()
    db.execute("DELETE FROM course WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('course_list'))

# 成绩列表
@app.route('/scores')
def score_list():
    keyword = request.args.get('keyword', '')
    db = get_db()
    if keyword:
        scores = db.execute("""
            SELECT score.*, student.stu_no, student.name as student_name, course.name as course_name
            FROM score
            JOIN student ON score.student_id = student.id
            JOIN course ON score.course_id = course.id
            WHERE student.name LIKE ? OR course.name LIKE ?
        """, (f'%{keyword}%', f'%{keyword}%')).fetchall()
    else:
        scores = db.execute("""
            SELECT score.*, student.stu_no, student.name as student_name, course.name as course_name
            FROM score
            JOIN student ON score.student_id = student.id
            JOIN course ON score.course_id = course.id
        """).fetchall()
    db.close()
    return render_template('scores.html', scores=scores, keyword=keyword)

# 录入成绩
@app.route('/scores/add', methods=['GET', 'POST'])
def score_add():
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "INSERT INTO score (student_id, course_id, score, semester) VALUES (?, ?, ?, ?)",
            (request.form['student_id'], request.form['course_id'],
             request.form['score'], request.form['semester'])
        )
        db.commit()
        db.close()
        return redirect(url_for('score_list'))
    students = db.execute("SELECT * FROM student").fetchall()
    courses = db.execute("SELECT * FROM course").fetchall()
    db.close()
    return render_template('score_form.html', score=None, students=students, courses=courses)

# 编辑成绩
@app.route('/scores/edit/<int:id>', methods=['GET', 'POST'])
def score_edit(id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            "UPDATE score SET student_id=?, course_id=?, score=?, semester=? WHERE id=?",
            (request.form['student_id'], request.form['course_id'],
             request.form['score'], request.form['semester'], id)
        )
        db.commit()
        db.close()
        return redirect(url_for('score_list'))
    score = db.execute("SELECT * FROM score WHERE id=?", (id,)).fetchone()
    students = db.execute("SELECT * FROM student").fetchall()
    courses = db.execute("SELECT * FROM course").fetchall()
    db.close()
    return render_template('score_form.html', score=score, students=students, courses=courses)

# 删除成绩
@app.route('/scores/delete/<int:id>')
def score_delete(id):
    db = get_db()
    db.execute("DELETE FROM score WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(url_for('score_list'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
