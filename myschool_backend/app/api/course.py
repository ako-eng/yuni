from flask import Blueprint, request, jsonify
from app.services.course_service import CourseService

bp = Blueprint('course', __name__)
course_service = CourseService()

@bp.route('/courses', methods=['GET'])
def get_courses():
    """获取用户的课程表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        courses = course_service.get_courses(user_id)
        return jsonify({
            'status': 'success',
            'data': courses
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    """根据 ID 获取课程"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        course = course_service.get_course_by_id(course_id, user_id)
        if not course:
            return jsonify({'status': 'error', 'message': '课程不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'data': course
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/courses', methods=['POST'])
def add_course():
    """添加课程"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = course_service.add_course(data, user_id)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    """更新课程"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = course_service.update_course(course_id, data, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    """删除课程"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = course_service.delete_course(course_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
