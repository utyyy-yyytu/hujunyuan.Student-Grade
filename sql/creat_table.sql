-- 创建数据库
CREATE DATABASE IF NOT EXISTS student_management
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE student_management;

-- =========================
-- 1. 学生表
-- =========================
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '学生ID',
    student_no VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender ENUM('男', '女', '其他') DEFAULT '其他' COMMENT '性别',
    birthday DATE DEFAULT NULL COMMENT '出生日期',
    phone VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    email VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    major VARCHAR(100) DEFAULT NULL COMMENT '专业',
    grade_year INT DEFAULT NULL COMMENT '年级，如2022',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常，0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_major (major)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生表';

-- =========================
-- 2. 课程表
-- =========================
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID',
    course_no VARCHAR(20) NOT NULL UNIQUE COMMENT '课程编号',
    course_name VARCHAR(100) NOT NULL COMMENT '课程名称',
    credit DECIMAL(3,1) DEFAULT 0.0 COMMENT '学分',
    teacher VARCHAR(50) DEFAULT NULL COMMENT '授课教师',
    description VARCHAR(255) DEFAULT NULL COMMENT '课程简介',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常，0停用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_course_name (course_name),
    INDEX idx_teacher (teacher)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程表';

-- =========================
-- 3. 成绩表
-- =========================
CREATE TABLE IF NOT EXISTS scores (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '成绩ID',
    student_id INT NOT NULL COMMENT '学生ID',
    course_id INT NOT NULL COMMENT '课程ID',
    usual_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '平时成绩',
    exam_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '期末成绩',
    total_score DECIMAL(5,2) DEFAULT 0.00 COMMENT '总评成绩',
    term VARCHAR(20) DEFAULT NULL COMMENT '学期，如2024-2025上学期',
    remark VARCHAR(255) DEFAULT NULL COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    -- 同一个学生同一门课程只能有一条成绩记录
    UNIQUE KEY uk_student_course (student_id, course_id),

    INDEX idx_student_id (student_id),
    INDEX idx_course_id (course_id),
    INDEX idx_total_score (total_score),

    CONSTRAINT fk_scores_student
        FOREIGN KEY (student_id) REFERENCES students(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_scores_course
        FOREIGN KEY (course_id) REFERENCES courses(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成绩表';
