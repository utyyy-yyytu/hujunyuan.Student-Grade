import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'student.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stu_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            class_name TEXT,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            credit REAL,
            teacher TEXT
        );

        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            score REAL,
            semester TEXT,
            FOREIGN KEY (student_id) REFERENCES student(id),
            FOREIGN KEY (course_id) REFERENCES course(id)
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('数据库初始化成功！')
