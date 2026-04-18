from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

# 创建蓝图
bp = Blueprint('auth', __name__)
# 实例化服务
auth_service = AuthService()

@bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    student_id = (data.get('student_id') or '').strip()
    password = (data.get('password') or '').strip()
    
    if not student_id or not password:
        return jsonify({'status': 'error', 'message': '学号和密码不能为空'}), 400
    
    try:
        result = auth_service.login(student_id, password)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    student_id = (data.get('student_id') or '').strip()
    password = (data.get('password') or '').strip()
    name = data.get('name')
    department = data.get('department')
    major = data.get('major')
    grade = data.get('grade')
    avatar_name = data.get('avatar_name')
    
    if not student_id or not password:
        return jsonify({'status': 'error', 'message': '学号和密码不能为空'}), 400
    
    try:
        result = auth_service.register(student_id, password, name, department, major, grade, avatar_name)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/auth/check', methods=['POST'])
def check_user():
    """检查用户是否存在"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    student_id = (data.get('student_id') or '').strip()
    
    if not student_id:
        return jsonify({'status': 'error', 'message': '学号不能为空'}), 400
    
    try:
        exists = auth_service.check_user_exists(student_id)
        return jsonify({
            'status': 'success',
            'data': {
                'exists': exists
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/auth/info', methods=['GET'])
def get_user_info():
    """获取用户信息"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        user_info = auth_service.get_user_info(user_id)
        return jsonify({
            'status': 'success',
            'data': user_info
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/auth/info', methods=['PUT'])
def update_user_info():
    """更新用户信息"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    name = data.get('name')
    department = data.get('department')
    major = data.get('major')
    grade = data.get('grade')
    avatar_name = data.get('avatar_name')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = auth_service.update_user_info(user_id, name, department, major, grade, avatar_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
