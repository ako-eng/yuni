from flask import Blueprint, request, jsonify
from app.services.search_service import SearchService

bp = Blueprint('search', __name__)
search_service = SearchService()

@bp.route('/search/history', methods=['GET'])
def get_search_history():
    """获取用户的搜索历史"""
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 10, type=int)
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        history = search_service.get_search_history(user_id, limit)
        return jsonify({
            'status': 'success',
            'data': history
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search/history', methods=['POST'])
def add_search_history():
    """添加搜索历史"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    keyword = data.get('keyword')
    
    if not user_id or not keyword:
        return jsonify({'status': 'error', 'message': '用户 ID 和关键词不能为空'}), 400
    
    try:
        result = search_service.add_search_history(user_id, keyword)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search/history', methods=['DELETE'])
def delete_search_history():
    """删除搜索历史"""
    if not request.is_json:
        return jsonify({'status': 'error', 'message': '请求需使用 Content-Type: application/json'}), 400
    
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'status': 'error', 'message': '无效的 JSON 请求体'}), 400
    
    user_id = data.get('user_id')
    keyword = data.get('keyword')
    
    if not user_id:
        return jsonify({'status': 'error', 'message': '用户 ID 不能为空'}), 400
    
    try:
        result = search_service.delete_search_history(user_id, keyword)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search/hot', methods=['GET'])
def get_hot_searches():
    """获取热门搜索"""
    limit = request.args.get('limit', 10, type=int)
    
    try:
        hot_searches = search_service.get_hot_searches(limit)
        return jsonify({
            'status': 'success',
            'data': hot_searches
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
