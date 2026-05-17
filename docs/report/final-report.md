# 学生成绩管理系统 结项报告

## 1. 项目背景与目标
本项目开发一个学生成绩查询系统，实现学生在线查看成绩、教师和管理员进行成绩管理。  
最终交付一个基于 Flask 的 Web 应用，具备用户注册登录、成绩增删改查、数据导出等完整功能。

## 2. 最终交付物清单
### 2.1 文档
| 文档名称 | 路径 |
|----------|------|
| 需求分析文档 | docs/plan/requirements.md |
| 架构设计文档 | docs/design/architecture.md |
| 数据库设计文档 | docs/design/database.md |
| 接口文档 | docs/design/api.md |
| 测试用例 | docs/test/test-cases.md |
| 测试报告 | docs/test/test-report.md |
| 会议纪要 | docs/meeting/meeting-notes.md |
| 任务分解 | docs/meeting/task-breakdown.md |
| 使用说明书 | docs/report/user-manual.md |
| 中期报告 | docs/report/mid-term-report.md |
| 项目汇报 PPT | docs/report/presentation.pptx |
| 结项报告 | docs/report/final-report.md |

### 2.2 代码
- 用户模型：src/models/user.py
- 用户路由：src/routes/auth.py
- 数据库模型：src/models/database.py
- 主应用：src/app.py
- 前端模板：src/templates/ (base.html, index.html, students.html 等)
- 测试脚本：src/tests/test_auth.py

### 2.3 其他
- Git 标签：v1-plan、v2-design、v3-final
- 原型图：ui/ 目录

## 3. 个人贡献总结（lengye241）
### 3.1 文档工作
独立完成全部项目文档共 12 份，包括需求分析、系统设计、测试设计、项目管理、用户手册等，保证文档体系完整。

### 3.2 测试工作
设计测试用例 10 条（覆盖注册、登录、成绩查询），并编写自动化单元测试脚本（test_auth.py），确保核心模块可验证。

### 3.3 项目管理工作
- 组织小组会议，编写会议纪要
- 分解任务，制定时间计划
- 维护 Git 仓库结构，保证提交规范、标签清晰
- 解决团队初期遇到的 Git 代理、网络等问题

### 3.4 代码贡献
实现用户注册、登录模块的模型和路由，代码已集成到主项目中并通过测试。

## 4. 项目亮点
- **Git 工作流规范**：全程小步提交，commit 信息具体，阶段标签明确
- **文档与代码同步**：每个阶段都有对应的文档产出，设计先于编码
- **测试先行**：在编码前完成测试用例设计，编码后立即编写自动化测试
- **完整交付**：从计划、设计、编码、测试到文档、汇报材料，全流程覆盖

## 5. 遇到的问题与反思
- 初期 Git 克隆失败：通过查找 VPN 本地端口 15715，配置 Git 代理解决
- 目录结构冲突：先 pull 远端，再按需创建文件，未覆盖组员代码
- 时间协调：通过会议纪要和任务分解明确分工，保证并行推进

## 6. 致谢
感谢全体组员的协作与努力，感谢老师的指导。

## 7. 结项标签
Git 标签：v3-final