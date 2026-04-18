from flask import Blueprint, request, jsonify
from app.services.award_service import AwardService

bp = Blueprint('award', __name__)
award_service = AwardService()

@bp.route('/awards', methods=['GET'])
def get_awards():
    """获取用户的获奖列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        awards = award_service.get_awards(user_id)
        return jsonify({
            'status': 'success',
            'data': awards
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/awards/<award_id>', methods=['GET'])
def get_award(award_id):
    """根据 ID 获取获奖"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        award = award_service.get_award_by_id(award_id, user_id)
        if not award:
            return jsonify({'status': 'error', 'message': '获奖记录不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'data': award
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/awards', methods=['POST'])
def add_award():
    """添加获奖"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = award_service.add_award(data, user_id)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/awards/<award_id>', methods=['PUT'])
def update_award(award_id):
    """更新获奖"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = award_service.update_award(award_id, data, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/awards/<award_id>', methods=['DELETE'])
def delete_award(award_id):
    """删除获奖"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = award_service.delete_award(award_id, user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
