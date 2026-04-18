import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services.notice_service import NoticeService

def import_notices():
    """导入通知数据"""
    notice_service = NoticeService()
    json_path = 'c:\\Users\\13420\\Desktop\\项目\\归档\\myschool_back\\gdut_notices.json'
    
    try:
        notice_service.import_from_json(json_path)
        print("通知导入成功！")
        
        # 验证导入结果
        latest_notices = notice_service.get_latest_notices(limit=5)
        print(f"\n最新5条通知：")
        for notice in latest_notices:
            print(f"- {notice['title']} ({notice['category']})")
        
        # 获取分类统计
        categories = notice_service.get_categories()
        print(f"\n通知分类：")
        for category in categories:
            category_notices = notice_service.get_notices(category=category)
            print(f"- {category}: {len(category_notices)}条")
            
    except Exception as e:
        print(f"导入失败: {str(e)}")

if __name__ == '__main__':
    import_notices()
