from flask import Blueprint, jsonify

# 创建蓝图
bp = Blueprint('health', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok'})
