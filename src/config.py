
import pymysql


class DBConfig:
    HOST = "localhost"
    PORT = 3306
    USER = "root"
    PASSWORD = "123456"   # 改成你自己的 MySQL 密码
    DATABASE = "student_management"
    CHARSET = "utf8mb4"


def get_connection():
    """
    获取数据库连接
    """
    return pymysql.connect(
        host=DBConfig.HOST,
        port=DBConfig.PORT,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD,
        database=DBConfig.DATABASE,
        charset=DBConfig.CHARSET,
        autocommit=False
    )


def execute_sql(sql, params=None):
    """
    执行增删改操作
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"SQL执行失败: {e}")
        return -1
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def query_sql(sql, params=None):
    """
    执行查询操作，返回所有结果
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql, params or ())
        return cursor.fetchall()
    except Exception as e:
        print(f"查询失败: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
