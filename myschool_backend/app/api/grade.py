from flask import Blueprint, request, jsonify
from app.services.grade_service import GradeService

bp = Blueprint('grade', __name__)
grade_service = GradeService()

@bp.route('/grades', methods=['GET'])
def get_grades():
    """获取用户的成绩列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        grades = grade_service.get_grades(user_id)
        return jsonify({
            'status': 'success',
            'data': grades
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/grades/<grade_id>', methods=['GET'])
def get_grade(grade_id):
    """根据 ID 获取成绩"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        grade = grade_service.get_grade_by_id(grade_id, user_id)
        if not grade:
            return jsonify({'status': 'error', 'message': '成绩不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'data': grade
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/grades', methods=['POST'])
def add_grade():
    """添加成绩"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = grade_service.add_grade(data, user_id)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/grades/<grade_id>', methods=['PUT'])
def update_grade(grade_id):
    """更新成绩"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = grade_service.update_grade(grade_id, data, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/grades/<grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    """删除成绩"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = grade_service.delete_grade(grade_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
