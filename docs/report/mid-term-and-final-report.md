# 学生成绩管理系统 中期与结项报告

---

## 第一部分：中期设计报告

### 1. 项目概述
本项目开发一个基于 Web 的学生成绩管理系统，支持学生在线查询成绩、管理员进行成绩和课程管理。  
技术栈：Python 3.12 + Flask + SQLAlchemy + MySQL（开发）+ Bootstrap 前端。  
当前已完成全部系统设计工作，进入编码实现和测试阶段。

### 2. 团队分工
| 成员 | 角色 | 主要任务 |
|------|------|----------|
| **lengye241** | 测试+文档+项目管理+部分开发 | 需求分析、架构设计、数据库设计、接口文档、测试用例/报告、会议纪要、任务分解、PPT、使用说明书；用户注册/登录模块编码；单元测试编写 |
| **utyyy-yyytu** | 后端开发+前端 | Flask 项目初始化、路由设计、页面模板（base.html、index.html）、学生/课程/成绩管理CRUD、Excel导出、UI优化、Git 仓库管理 |
| **chenghlixue** | 数据库设计与后端核心 | 数据库表设计、SQL建表脚本、所有数据模型（学生、课程、成绩）、核心API逻辑、数据库连接配置 |

### 3. 中期完成情况
#### 3.1 文档（lengye241 负责）
- [x] 需求分析文档（docs/plan/requirements.md）
- [x] 架构设计文档（docs/design/architecture.md）
- [x] 数据库设计文档（docs/design/database.md）
- [x] 接口文档（docs/design/api.md）
- [x] 测试用例文档（docs/test/test-cases.md）
- [x] 测试报告框架（docs/test/test-report.md）
- [x] 会议纪要（docs/meeting/meeting-notes.md）
- [x] 任务分解（docs/meeting/task-breakdown.md）
- [x] 使用说明书（docs/report/user-manual.md）

#### 3.2 代码（全组合作）
- [x] Flask 项目骨架搭建，路由规划（utyyy-yyytu）
- [x] 基础页面模板（base.html、index.html）及 Bootstrap 美化（utyyy-yyytu）
- [x] 数据库建表脚本（sql/）和所有数据模型定义（chenghlixue）
- [x] 学生信息增删改查功能（utyyy-yyytu）
- [x] 课程信息增删改查功能（utyyy-yyytu）
- [x] 成绩录入、编辑、删除、搜索功能（utyyy-yyytu）
- [x] 用户注册/登录模块模型与路由（lengye241）
- [x] 数据库连接配置及模型对接（chenghlixue）

#### 3.3 测试（lengye241 负责）
- [x] 编写用户模块单元测试用例 10 条（test_auth.py）
- [x] 测试报告框架已就绪，待执行测试后填写实际通过率

### 4. 技术方案
- **后端框架**：Flask + Jinja2 模板引擎
- **数据库**：MySQL（生产）+ SQLAlchemy ORM（便于切换 SQLite 测试）
- **前端**：HTML5 + Bootstrap 5，响应式布局
- **项目结构**：