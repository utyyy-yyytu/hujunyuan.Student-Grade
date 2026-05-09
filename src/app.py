from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>学生成绩管理系统</h1><p>项目已成功启动！</p>'

if __name__ == '__main__':
    app.run(debug=True)
