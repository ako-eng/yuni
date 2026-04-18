from flask import Blueprint, request, jsonify
from app.services.exam_service import ExamService

bp = Blueprint('exam', __name__)
exam_service = ExamService()

@bp.route('/exams', methods=['GET'])
def get_exams():
    """获取用户的考试列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        exams = exam_service.get_exams(user_id)
        return jsonify({
            'status': 'success',
            'data': exams
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/exams/<exam_id>', methods=['GET'])
def get_exam(exam_id):
    """根据 ID 获取考试"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        exam = exam_service.get_exam_by_id(exam_id, user_id)
        if not exam:
            return jsonify({'status': 'error', 'message': '考试不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'data': exam
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/exams', methods=['POST'])
def add_exam():
    """添加考试"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = exam_service.add_exam(data, user_id)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/exams/<exam_id>', methods=['PUT'])
def update_exam(exam_id):
    """更新考试"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = exam_service.update_exam(exam_id, data, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/exams/<exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    """删除考试"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = exam_service.delete_exam(exam_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
