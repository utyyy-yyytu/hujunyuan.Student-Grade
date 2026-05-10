# src/models/score_model.py

from src.config import execute_sql, query_sql


class ScoreModel:
    """
    成绩模型：对应 scores 表
    支持：
    - 新增
    - 修改
    - 删除
    - 按ID查询
    - 按学生/课程查询
    - 查询全部
    - 模糊查询
    - 排名
    - 统计
    """

    @staticmethod
    def calc_total_score(usual_score, exam_score, usual_weight=0.4, exam_weight=0.6):
        """
        计算总评成绩
        默认：平时40%，期末60%
        如果你有别的规则，可以改这里
        """
        if usual_score is None:
            usual_score = 0
        if exam_score is None:
            exam_score = 0
        return round(float(usual_score) * usual_weight + float(exam_score) * exam_weight, 2)

    @staticmethod
    def add_score(student_id, course_id, usual_score=0, exam_score=0,
                  total_score=None, term=None, remark=None):
        """
        新增成绩
        如果 total_score 为空，则自动按平时40%、期末60%计算
        """
        if total_score is None:
            total_score = ScoreModel.calc_total_score(usual_score, exam_score)

        sql = """
            INSERT INTO scores
            (student_id, course_id, usual_score, exam_score, total_score, term, remark)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (student_id, course_id, usual_score, exam_score, total_score, term, remark)
        return execute_sql(sql, params)

    @staticmethod
    def update_score(score_id, student_id, course_id, usual_score=0, exam_score=0,
                     total_score=None, term=None, remark=None):
        """
        修改成绩
        """
        if total_score is None:
            total_score = ScoreModel.calc_total_score(usual_score, exam_score)

        sql = """
            UPDATE scores
            SET student_id = %s,
                course_id = %s,
                usual_score = %s,
                exam_score = %s,
                total_score = %s,
                term = %s,
                remark = %s
            WHERE id = %s
        """
        params = (student_id, course_id, usual_score, exam_score, total_score, term, remark, score_id)
        return execute_sql(sql, params)

    @staticmethod
    def delete_score(score_id):
        """
        删除成绩
        """
        sql = "DELETE FROM scores WHERE id = %s"
        return execute_sql(sql, (score_id,))

    @staticmethod
    def get_score_by_id(score_id):
        """
        根据ID查询成绩
        同时查出学生姓名、学号、课程名称
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            WHERE sc.id = %s
        """
        result = query_sql(sql, (score_id,))
        return result[0] if result else None

    @staticmethod
    def get_score_by_student_course(student_id, course_id):
        """
        根据学生ID和课程ID查询成绩
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            WHERE sc.student_id = %s AND sc.course_id = %s
        """
        result = query_sql(sql, (student_id, course_id))
        return result[0] if result else None

    @staticmethod
    def get_all_scores():
        """
        查询所有成绩
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            ORDER BY sc.id DESC
        """
        return query_sql(sql)

    @staticmethod
    def get_scores_by_student(student_id):
        """
        查询某个学生的所有成绩
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            WHERE sc.student_id = %s
            ORDER BY sc.total_score DESC, sc.id DESC
        """
        return query_sql(sql, (student_id,))

    @staticmethod
    def get_scores_by_course(course_id):
        """
        查询某门课程的所有成绩
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            WHERE sc.course_id = %s
            ORDER BY sc.total_score DESC, sc.id DESC
        """
        return query_sql(sql, (course_id,))

    @staticmethod
    def search_scores(keyword):
        """
        模糊查询成绩
        可根据：
        - 学号
        - 姓名
        - 课程编号
        - 课程名称
        - 学期
        查询
        """
        sql = """
            SELECT
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark,
                sc.created_at,
                sc.updated_at
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            WHERE st.student_no LIKE %s
               OR st.name LIKE %s
               OR c.course_no LIKE %s
               OR c.course_name LIKE %s
               OR sc.term LIKE %s
            ORDER BY sc.total_score DESC, sc.id DESC
        """
        like_keyword = f"%{keyword}%"
        params = (like_keyword, like_keyword, like_keyword, like_keyword, like_keyword)
        return query_sql(sql, params)

    @staticmethod
    def get_rankings(course_id=None, term=None, limit=None):
        """
        成绩排名
        默认按 total_score 降序排名

        参数：
        - course_id: 某门课程排名
        - term: 某学期排名
        - limit: 只取前N名
        """
        where_clauses = []
        params = []

        if course_id is not None:
            where_clauses.append("sc.course_id = %s")
            params.append(course_id)

        if term is not None:
            where_clauses.append("sc.term = %s")
            params.append(term)

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        limit_sql = ""
        if limit is not None:
            limit_sql = "LIMIT %s"
            params.append(limit)

        sql = f"""
            SELECT
                ROW_NUMBER() OVER (ORDER BY sc.total_score DESC, sc.id ASC) AS ranking,
                sc.id,
                sc.student_id,
                st.student_no,
                st.name AS student_name,
                sc.course_id,
                c.course_no,
                c.course_name,
                sc.usual_score,
                sc.exam_score,
                sc.total_score,
                sc.term,
                sc.remark
            FROM scores sc
            LEFT JOIN students st ON sc.student_id = st.id
            LEFT JOIN courses c ON sc.course_id = c.id
            {where_sql}
            ORDER BY sc.total_score DESC, sc.id ASC
            {limit_sql}
        """
        return query_sql(sql, tuple(params))

    @staticmethod
    def get_statistics_by_student(student_id):
        """
        统计某个学生的成绩情况
        返回：
        - 课程数
        - 平均分
        - 最高分
        - 最低分
        - 及格门数
        - 及格率
        """
        sql = """
            SELECT
                COUNT(*) AS course_count,
                ROUND(AVG(total_score), 2) AS avg_score,
                MAX(total_score) AS max_score,
                MIN(total_score) AS min_score,
                SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) AS pass_count,
                ROUND(
                    SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
                    2
                ) AS pass_rate
            FROM scores
            WHERE student_id = %s
        """
        result = query_sql(sql, (student_id,))
        return result[0] if result else None

    @staticmethod
    def get_statistics_by_course(course_id):
        """
        统计某门课程的成绩情况
        返回：
        - 学生数
        - 平均分
        - 最高分
        - 最低分
        - 及格人数
        - 及格率
        """
        sql = """
            SELECT
                COUNT(*) AS student_count,
                ROUND(AVG(total_score), 2) AS avg_score,
                MAX(total_score) AS max_score,
                MIN(total_score) AS min_score,
                SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) AS pass_count,
                ROUND(
                    SUM(CASE WHEN total_score >= 60 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
                    2
                ) AS pass_rate
            FROM scores
            WHERE course_id = %s
        """
        result = query_sql(sql, (course_id,))
        return result[0] if result else None

    @staticmethod
    def count_scores():
        """
        统计成绩记录总数
        """
        sql = "SELECT COUNT(*) AS total FROM scores"
        result = query_sql(sql)
        return result[0]["total"] if result else 0
