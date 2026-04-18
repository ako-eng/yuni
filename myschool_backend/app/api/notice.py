from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services.notice_service import NoticeService
from app.services.spider_service import SpiderService

bp = Blueprint('notice', __name__)
notice_service = NoticeService()
spider_service = SpiderService()

@bp.route('/notices', methods=['GET'])
def get_notices():
    user_id = request.args.get('user_id')
    category = request.args.get('category')
    tag = request.args.get('tag')
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 计算偏移量
    offset = (page - 1) * per_page
    
    # 构建标签列表
    tags = []
    if tag:
        tags.append(tag)
    
    # 获取通知
    notices = notice_service.get_notices(
        user_id=user_id,
        category=category,
        tags=tags,
        limit=per_page,
        offset=offset
    )
    
    # 构建响应格式
    total = len(notices)  # 实际应该从数据库获取总数
    pages = (total + per_page - 1) // per_page
    
    # 转换通知格式以匹配前端期望
    items = []
    for notice in notices:
        items.append({
            'title': notice['title'],
            'url': notice.get('url', ''),
            'date': datetime.fromtimestamp(notice['publishDate']).strftime('%Y-%m-%d'),
            'category': notice['category'],
            'tags': notice['tags'],
            'content': notice['content'],
            'publishDate': None,
            'department': notice.get('source', ''),
            'attachments': notice['attachments'],
            'sourceUrl': notice.get('sourceURL', '')
        })
    
    return jsonify({
        'total': total,
        'page': page,
        'perPage': per_page,
        'pages': pages,
        'items': items
    })

@bp.route('/notices/latest', methods=['GET'])
def get_latest_notices():
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 10, type=int)
    notices = notice_service.get_latest_notices(user_id=user_id, limit=limit)
    
    return jsonify({
        'status': 'success',
        'data': notices
    })

@bp.route('/notices/urgent', methods=['GET'])
def get_urgent_notices():
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 10, type=int)
    notices = notice_service.get_urgent_notices(user_id=user_id, limit=limit)
    
    return jsonify({
        'status': 'success',
        'data': notices
    })

@bp.route('/notices/<notice_id>', methods=['GET'])
def get_notice(notice_id):
    user_id = request.args.get('user_id')
    notice = notice_service.get_notice_by_id(notice_id, user_id=user_id)
    if not notice:
        return jsonify({
            'status': 'error',
            'message': '通知不存在'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': notice
    })

@bp.route('/notices', methods=['POST'])
def save_notice():
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': '请提供通知数据'
        }), 400
    
    user_id = data.get('user_id')
    result = notice_service.save_notice(data, user_id=user_id)
    return jsonify(result)

@bp.route('/categories', methods=['GET'])
def get_categories():
    user_id = request.args.get('user_id')
    categories = notice_service.get_categories(user_id=user_id)
    
    # 构建分类统计数据
    category_stats = []
    all_tags = set()
    total_notices = 0
    
    for category in categories:
        # 获取该分类的通知
        category_notices = notice_service.get_notices(user_id=user_id, category=category)
        count = len(category_notices)
        total_notices += count
        
        # 收集该分类的所有标签
        category_tags = set()
        for notice in category_notices:
            for tag in notice['tags']:
                category_tags.add(tag)
                all_tags.add(tag)
        
        category_stats.append({
            'name': category,
            'count': count,
            'tags': list(category_tags)
        })
    
    return jsonify({
        'categories': category_stats,
        'total_notices': total_notices,
        'all_tags': list(all_tags)
    })

@bp.route('/import', methods=['POST'])
def import_notices():
    json_path = request.args.get('path')
    user_id = request.args.get('user_id')
    if not json_path:
        return jsonify({
            'status': 'error',
            'message': '请提供 JSON 文件路径'
        }), 400
    
    try:
        notice_service.import_from_json(json_path, user_id=user_id)
        return jsonify({
            'status': 'success',
            'message': '通知导入成功'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'导入失败: {str(e)}'
        }), 500

@bp.route('/notices/add', methods=['POST'])
def add_notice():
    """教师发布通知"""
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': '请提供通知数据'
        }), 400
    
    # 解析标签
    if 'tags' in data and isinstance(data['tags'], str):
        data['tags'] = [tag.strip() for tag in data['tags'].split(',') if tag.strip()]
    
    user_id = data.get('user_id')
    result = notice_service.save_notice(data, user_id=user_id)
    return jsonify(result)

@bp.route('/crawl/trigger', methods=['POST'])
def trigger_crawl():
    """触发爬取通知"""
    user_id = request.args.get('user_id')
    try:
        # 爬取通知
        crawl_result = spider_service.crawl_notices(max_pages=3)
        
        if crawl_result['status'] == 'success':
            # 保存爬取到的通知到数据库
            notices = crawl_result['data']
            for notice in notices:
                # 转换分类名称
                category_map = {
                    '教务通知': 'academic',
                    '考试通知': 'exam',
                    '竞赛通知': 'competition',
                    '科研通知': 'research',
                    '生活通知': 'life',
                    '校企通知': 'enterprise',
                    '保卫通知': 'security',
                    '后勤通知': 'general',
                    '图书馆通知': 'library',
                    '综合通知': 'general'
                }
                notice['category'] = category_map.get(notice['category'], 'general')
                # 转换日期为时间戳
                if 'date' in notice and notice['date']:
                    try:
                        publish_date = datetime.strptime(notice['date'], '%Y-%m-%d')
                        notice['publishDate'] = int(publish_date.timestamp())
                    except:
                        notice['publishDate'] = int(datetime.now().timestamp())
                else:
                    notice['publishDate'] = int(datetime.now().timestamp())
                # 转换其他字段
                notice['source'] = notice.get('department', '')
                notice['sourceURL'] = notice.get('source_url', notice.get('url', ''))
                notice['attachments'] = notice.get('attachments', [])
                # 保存通知
                notice_service.save_notice(notice, user_id=user_id)
            
            return jsonify({
                'status': 'success',
                'message': f'爬取并保存成功，共获取 {len(notices)} 条通知'
            })
        else:
            return jsonify(crawl_result), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'爬取出错: {str(e)}'
        }), 500
