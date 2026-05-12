from flask import Blueprint, request, jsonify, session
from src.models.user import User
from src.models.database import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 400
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        session['role'] = user.role
        return jsonify({'message': '登录成功', 'role': user.role}), 200
    return jsonify({'message': '用户名或密码错误'}), 401