# 学生成绩管理系统 数据库设计文档

## 1. 数据库选择
- 开发环境：SQLite
- 生产环境：MySQL（可切换）
- ORM：SQLAlchemy

## 2. E-R 图（待补充）
（此处后续插入实体关系图）

## 3. 表结构设计

### 3.1 用户表（users）
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 用户ID |
| username | VARCHAR(80) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(128) | NOT NULL | 密码哈希值 |
| role | VARCHAR(20) | DEFAULT 'student' | 角色：student/admin |

### 3.2 课程表（courses）
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 课程ID |
| name | VARCHAR(100) | NOT NULL | 课程名称 |
| semester | VARCHAR(10) | | 开课学期 |

### 3.3 成绩表（scores）
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 成绩ID |
| student_id | INTEGER | FOREIGN KEY (users.id) | 学生ID |
| course_id | INTEGER | FOREIGN KEY (courses.id) | 课程ID |
| score | FLOAT | | 分数 |

## 4. 索引设计
- users 表：username 建立唯一索引
- scores 表：student_id、course_id 建立普通索引

## 5. 数据库脚本（待补充）
（SQL 脚本将放在 sql/ 目录）