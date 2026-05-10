# src/models/student_model.py

from src.config import execute_sql, query_sql


class StudentModel:
    """
    学生模型：对应 students 表
    支持：
    - 新增
    - 修改
    - 删除
    - 按ID查询
    - 按学号查询
    - 查询全部
    - 模糊查询
    - 修改状态
    """

    @staticmethod
    def add_student(student_no, name, gender="其他", birthday=None,
                    phone=None, email=None, major=None, grade_year=None, status=1):
        """
        新增学生
        """
        sql = """
            INSERT INTO students
            (student_no, name, gender, birthday, phone, email, major, grade_year, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            student_no, name, gender, birthday, phone,
            email, major, grade_year, status
        )
        return execute_sql(sql, params)

    @staticmethod
    def update_student(student_id, student_no, name, gender="其他", birthday=None,
                       phone=None, email=None, major=None, grade_year=None, status=1):
        """
        修改学生信息
        """
        sql = """
            UPDATE students
            SET student_no = %s,
                name = %s,
                gender = %s,
                birthday = %s,
                phone = %s,
                email = %s,
                major = %s,
                grade_year = %s,
                status = %s
            WHERE id = %s
        """
        params = (
            student_no, name, gender, birthday, phone,
            email, major, grade_year, status, student_id
        )
        return execute_sql(sql, params)

    @staticmethod
    def delete_student(student_id):
        """
        删除学生
        """
        sql = "DELETE FROM students WHERE id = %s"
        return execute_sql(sql, (student_id,))

    @staticmethod
    def get_student_by_id(student_id):
        """
        根据ID查询学生
        """
        sql = "SELECT * FROM students WHERE id = %s"
        result = query_sql(sql, (student_id,))
        return result[0] if result else None

    @staticmethod
    def get_student_by_no(student_no):
        """
        根据学号查询学生
        """
        sql = "SELECT * FROM students WHERE student_no = %s"
        result = query_sql(sql, (student_no,))
        return result[0] if result else None

    @staticmethod
    def get_all_students():
        """
        查询所有学生
        """
        sql = "SELECT * FROM students ORDER BY id DESC"
        return query_sql(sql)

    @staticmethod
    def search_students(keyword):
        """
        模糊查询学生
        可根据 学号 / 姓名 / 专业 / 手机号 / 邮箱 查询
        """
        sql = """
            SELECT * FROM students
            WHERE student_no LIKE %s
               OR name LIKE %s
               OR major LIKE %s
               OR phone LIKE %s
               OR email LIKE %s
            ORDER BY id DESC
        """
        like_keyword = f"%{keyword}%"
        params = (
            like_keyword, like_keyword, like_keyword,
            like_keyword, like_keyword
        )
        return query_sql(sql, params)

    @staticmethod
    def update_status(student_id, status):
        """
        修改学生状态
        status: 1 正常，0 禁用
        """
        sql = "UPDATE students SET status = %s WHERE id = %s"
        return execute_sql(sql, (status, student_id))

    @staticmethod
    def count_students():
        """
        统计学生总数
        """
        sql = "SELECT COUNT(*) AS total FROM students"
        result = query_sql(sql)
        return result[0]["total"] if result else 0
