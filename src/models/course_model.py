# src/models/course_model.py

from src.config import execute_sql, query_sql


class CourseModel:
    """
    课程模型：对应 courses 表
    支持：
    - 新增
    - 修改
    - 删除
    - 按ID查询
    - 按课程编号查询
    - 查询全部
    - 模糊查询
    - 修改状态
    - 统计课程总数
    """

    @staticmethod
    def add_course(course_no, course_name, credit=0.0, teacher=None, description=None, status=1):
        """
        新增课程
        """
        sql = """
            INSERT INTO courses
            (course_no, course_name, credit, teacher, description, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (course_no, course_name, credit, teacher, description, status)
        return execute_sql(sql, params)

    @staticmethod
    def update_course(course_id, course_no, course_name, credit=0.0, teacher=None, description=None, status=1):
        """
        修改课程信息
        """
        sql = """
            UPDATE courses
            SET course_no = %s,
                course_name = %s,
                credit = %s,
                teacher = %s,
                description = %s,
                status = %s
            WHERE id = %s
        """
        params = (course_no, course_name, credit, teacher, description, status, course_id)
        return execute_sql(sql, params)

    @staticmethod
    def delete_course(course_id):
        """
        删除课程
        """
        sql = "DELETE FROM courses WHERE id = %s"
        return execute_sql(sql, (course_id,))

    @staticmethod
    def get_course_by_id(course_id):
        """
        根据ID查询课程
        """
        sql = "SELECT * FROM courses WHERE id = %s"
        result = query_sql(sql, (course_id,))
        return result[0] if result else None

    @staticmethod
    def get_course_by_no(course_no):
        """
        根据课程编号查询课程
        """
        sql = "SELECT * FROM courses WHERE course_no = %s"
        result = query_sql(sql, (course_no,))
        return result[0] if result else None

    @staticmethod
    def get_all_courses():
        """
        查询所有课程
        """
        sql = "SELECT * FROM courses ORDER BY id DESC"
        return query_sql(sql)

    @staticmethod
    def search_courses(keyword):
        """
        模糊查询课程
        可根据 课程编号 / 课程名称 / 教师 / 简介 查询
        """
        sql = """
            SELECT * FROM courses
            WHERE course_no LIKE %s
               OR course_name LIKE %s
               OR teacher LIKE %s
               OR description LIKE %s
            ORDER BY id DESC
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword, like_keyword)
        return query_sql(sql, params)

    @staticmethod
    def update_status(course_id, status):
        """
        修改课程状态
        status: 1 正常，0 停用
        """
        sql = "UPDATE courses SET status = %s WHERE id = %s"
        return execute_sql(sql, (status, course_id))

    @staticmethod
    def count_courses():
        """
        统计课程总数
        """
        sql = "SELECT COUNT(*) AS total FROM courses"
        result = query_sql(sql)
        return result[0]["total"] if result else 0
