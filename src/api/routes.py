from flask import Blueprint, request, jsonify
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from flask import send_file

from src.models.student_model import StudentModel
from src.models.course_model import CourseModel
from src.models.score_model import ScoreModel



api_bp = Blueprint("api", __name__, url_prefix="/api")


# =========================
# 通用返回封装
# =========================
def success(data=None, message="success", code=200):
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


def fail(message="fail", code=400, data=None):
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


def get_json():
    return request.get_json(silent=True) or {}

def create_excel_response(title, headers, rows, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    ws.append(headers)
    for row in rows:
        ws.append(row)

    header_fill = PatternFill("solid", fgColor="4F81BD")
    header_font = Font(color="FFFFFF", bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment

    for column_cells in ws.columns:
        max_length = 0
        column_letter = column_cells[0].column_letter
        for cell in column_cells:
            try:
                cell_value = str(cell.value) if cell.value is not None else ""
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
            except Exception:
                pass
        ws.column_dimensions[column_letter].width = max_length + 4

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# =========================
# 学生 API
# =========================

@api_bp.route("/students", methods=["GET"])
def get_students():
    students = StudentModel.get_all_students()
    return success(students)


@api_bp.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    student = StudentModel.get_student_by_id(student_id)
    if not student:
        return fail("学生不存在", 404)
    return success(student)


@api_bp.route("/students/search", methods=["GET"])
def search_students():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return fail("keyword 不能为空", 400)

    result = StudentModel.search_students(keyword)
    return success(result)


@api_bp.route("/students/count", methods=["GET"])
def count_students():
    total = StudentModel.count_students()
    return success({"total": total})


@api_bp.route("/students", methods=["POST"])
def add_student():
    data = get_json()

    student_no = data.get("student_no")
    name = data.get("name")
    gender = data.get("gender", "其他")
    birthday = data.get("birthday")
    phone = data.get("phone")
    email = data.get("email")
    major = data.get("major")
    grade_year = data.get("grade_year")
    status = data.get("status", 1)

    if not student_no or not name:
        return fail("student_no 和 name 不能为空", 400)

    try:
        affected = StudentModel.add_student(
            student_no, name, gender, birthday,
            phone, email, major, grade_year, status
        )

        if affected > 0:
            return success(message="学生添加成功", code=201)
        return fail("学生添加失败", 500)

    except Exception as e:
        return fail(f"学生添加失败：{str(e)}", 500)


@api_bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = get_json()

    student_no = data.get("student_no")
    name = data.get("name")
    gender = data.get("gender", "其他")
    birthday = data.get("birthday")
    phone = data.get("phone")
    email = data.get("email")
    major = data.get("major")
    grade_year = data.get("grade_year")
    status = data.get("status", 1)

    if not student_no or not name:
        return fail("student_no 和 name 不能为空", 400)

    try:
        affected = StudentModel.update_student(
            student_id, student_no, name, gender, birthday,
            phone, email, major, grade_year, status
        )

        if affected > 0:
            return success(message="学生修改成功")
        return fail("学生不存在或未更新", 404)

    except Exception as e:
        return fail(f"学生修改失败：{str(e)}", 500)


@api_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        affected = StudentModel.delete_student(student_id)
        if affected > 0:
            return success(message="学生删除成功")
        return fail("学生不存在或未删除", 404)

    except Exception as e:
        return fail(f"学生删除失败：{str(e)}", 500)


@api_bp.route("/students/<int:student_id>/status", methods=["PATCH"])
def update_student_status(student_id):
    data = get_json()
    status = data.get("status")

    if status not in [0, 1]:
        return fail("status 只能是 0 或 1", 400)

    try:
        affected = StudentModel.update_status(student_id, status)
        if affected > 0:
            return success(message="学生状态修改成功")
        return fail("学生不存在或状态未修改", 404)

    except Exception as e:
        return fail(f"学生状态修改失败：{str(e)}", 500)


# =========================
# 课程 API
# =========================

@api_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = CourseModel.get_all_courses()
    return success(courses)


@api_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    course = CourseModel.get_course_by_id(course_id)
    if not course:
        return fail("课程不存在", 404)
    return success(course)


@api_bp.route("/courses/search", methods=["GET"])
def search_courses():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return fail("keyword 不能为空", 400)

    result = CourseModel.search_courses(keyword)
    return success(result)


@api_bp.route("/courses/count", methods=["GET"])
def count_courses():
    total = CourseModel.count_courses()
    return success({"total": total})


@api_bp.route("/courses", methods=["POST"])
def add_course():
    data = get_json()

    course_no = data.get("course_no")
    course_name = data.get("course_name")
    credit = data.get("credit", 0.0)
    teacher = data.get("teacher")
    description = data.get("description")
    status = data.get("status", 1)

    if not course_no or not course_name:
        return fail("course_no 和 course_name 不能为空", 400)

    try:
        affected = CourseModel.add_course(
            course_no, course_name, credit, teacher, description, status
        )

        if affected > 0:
            return success(message="课程添加成功", code=201)
        return fail("课程添加失败", 500)

    except Exception as e:
        return fail(f"课程添加失败：{str(e)}", 500)


@api_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = get_json()

    course_no = data.get("course_no")
    course_name = data.get("course_name")
    credit = data.get("credit", 0.0)
    teacher = data.get("teacher")
    description = data.get("description")
    status = data.get("status", 1)

    if not course_no or not course_name:
        return fail("course_no 和 course_name 不能为空", 400)

    try:
        affected = CourseModel.update_course(
            course_id, course_no, course_name, credit, teacher, description, status
        )

        if affected > 0:
            return success(message="课程修改成功")
        return fail("课程不存在或未更新", 404)

    except Exception as e:
        return fail(f"课程修改失败：{str(e)}", 500)


@api_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        affected = CourseModel.delete_course(course_id)
        if affected > 0:
            return success(message="课程删除成功")
        return fail("课程不存在或未删除", 404)

    except Exception as e:
        return fail(f"课程删除失败：{str(e)}", 500)


@api_bp.route("/courses/<int:course_id>/status", methods=["PATCH"])
def update_course_status(course_id):
    data = get_json()
    status = data.get("status")

    if status not in [0, 1]:
        return fail("status 只能是 0 或 1", 400)

    try:
        affected = CourseModel.update_status(course_id, status)
        if affected > 0:
            return success(message="课程状态修改成功")
        return fail("课程不存在或状态未修改", 404)

    except Exception as e:
        return fail(f"课程状态修改失败：{str(e)}", 500)


# =========================
# 成绩 API
# =========================

@api_bp.route("/scores", methods=["GET"])
def get_scores():
    scores = ScoreModel.get_all_scores()
    return success(scores)


@api_bp.route("/scores/<int:score_id>", methods=["GET"])
def get_score_by_id(score_id):
    score = ScoreModel.get_score_by_id(score_id)
    if not score:
        return fail("成绩不存在", 404)
    return success(score)


@api_bp.route("/scores/search", methods=["GET"])
def search_scores():
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return fail("keyword 不能为空", 400)

    result = ScoreModel.search_scores(keyword)
    return success(result)


@api_bp.route("/scores/count", methods=["GET"])
def count_scores():
    total = ScoreModel.count_scores()
    return success({"total": total})


@api_bp.route("/scores/rankings", methods=["GET"])
def get_rankings():
    course_id = request.args.get("course_id", type=int)
    term = request.args.get("term")
    limit = request.args.get("limit", type=int)

    result = ScoreModel.get_rankings(course_id=course_id, term=term, limit=limit)
    return success(result)


@api_bp.route("/scores/statistics/student/<int:student_id>", methods=["GET"])
def statistics_by_student(student_id):
    result = ScoreModel.get_statistics_by_student(student_id)
    if not result:
        return fail("没有找到该学生的成绩统计", 404)
    return success(result)


@api_bp.route("/scores/statistics/course/<int:course_id>", methods=["GET"])
def statistics_by_course(course_id):
    result = ScoreModel.get_statistics_by_course(course_id)
    if not result:
        return fail("没有找到该课程的成绩统计", 404)
    return success(result)


@api_bp.route("/scores", methods=["POST"])
def add_score():
    data = get_json()

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    usual_score = data.get("usual_score", 0)
    exam_score = data.get("exam_score", 0)
    total_score = data.get("total_score")
    term = data.get("term")
    remark = data.get("remark")

    if not student_id or not course_id:
        return fail("student_id 和 course_id 不能为空", 400)

    try:
        affected = ScoreModel.add_score(
            student_id, course_id, usual_score, exam_score,
            total_score, term, remark
        )

        if affected > 0:
            return success(message="成绩添加成功", code=201)
        return fail("成绩添加失败", 500)

    except Exception as e:
        return fail(f"成绩添加失败：{str(e)}", 500)


@api_bp.route("/scores/<int:score_id>", methods=["PUT"])
def update_score(score_id):
    data = get_json()

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    usual_score = data.get("usual_score", 0)
    exam_score = data.get("exam_score", 0)
    total_score = data.get("total_score")
    term = data.get("term")
    remark = data.get("remark")

    if not student_id or not course_id:
        return fail("student_id 和 course_id 不能为空", 400)

    try:
        affected = ScoreModel.update_score(
            score_id, student_id, course_id,
            usual_score, exam_score, total_score, term, remark
        )

        if affected > 0:
            return success(message="成绩修改成功")
        return fail("成绩不存在或未更新", 404)

    except Exception as e:
        return fail(f"成绩修改失败：{str(e)}", 500)


@api_bp.route("/scores/<int:score_id>", methods=["DELETE"])
def delete_score(score_id):
    try:
        affected = ScoreModel.delete_score(score_id)
        if affected > 0:
            return success(message="成绩删除成功")
        return fail("成绩不存在或未删除", 404)

    except Exception as e:
        return fail(f"成绩删除失败：{str(e)}", 500)


@api_bp.route("/scores/student/<int:student_id>", methods=["GET"])
def get_scores_by_student(student_id):
    result = ScoreModel.get_scores_by_student(student_id)
    return success(result)


@api_bp.route("/scores/course/<int:course_id>", methods=["GET"])
def get_scores_by_course(course_id):
    result = ScoreModel.get_scores_by_course(course_id)
    return success(result)

@api_bp.route("/export/students", methods=["GET"])
def export_students():
    students = StudentModel.get_all_students()

    headers = ["ID", "学号", "姓名", "性别", "出生日期", "手机号", "邮箱", "专业", "年级", "状态"]

    rows = []
    for s in students:
        rows.append([
            s.get("id"),
            s.get("student_no"),
            s.get("name"),
            s.get("gender"),
            s.get("birthday"),
            s.get("phone"),
            s.get("email"),
            s.get("major"),
            s.get("grade_year"),
            "正常" if s.get("status") == 1 else "禁用"
        ])

    return create_excel_response(
        title="学生信息",
        headers=headers,
        rows=rows,
        filename="学生信息导出.xlsx"
    )



@api_bp.route("/export/scores", methods=["GET"])
def export_scores():
    scores = ScoreModel.get_all_scores()

    headers = ["ID", "学号", "姓名", "课程编号", "课程名称", "平时成绩", "期末成绩", "总评成绩", "学期", "备注"]

    rows = []
    for s in scores:
        rows.append([
            s.get("id"),
            s.get("student_no"),
            s.get("student_name"),
            s.get("course_no"),
            s.get("course_name"),
            s.get("usual_score"),
            s.get("exam_score"),
            s.get("total_score"),
            s.get("term"),
            s.get("remark")
        ])

    return create_excel_response(
        title="成绩信息",
        headers=headers,
        rows=rows,
        filename="成绩信息导出.xlsx"
    )
