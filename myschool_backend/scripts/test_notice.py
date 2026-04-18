import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services.notice_service import NoticeService

def test_import_notices():
    """测试导入通知数据"""
    notice_service = NoticeService()
    json_path = 'c:\\Users\\13420\\Desktop\\项目\\归档\\myschool_back\\gdut_notices.json'
    
    try:
        notice_service.import_from_json(json_path)
        print("通知导入成功！")
        
        # 测试获取最新通知
        latest_notices = notice_service.get_latest_notices(limit=5)
        print(f"\n最新5条通知：")
        for notice in latest_notices:
            print(f"- {notice['title']} ({notice['category']})")
        
        # 测试获取分类
        categories = notice_service.get_categories()
        print(f"\n通知分类：")
        for category in categories:
            print(f"- {category}")
        
        # 测试按分类获取通知
        if categories:
            category = categories[0]
            category_notices = notice_service.get_notices(category=category, limit=3)
            print(f"\n{category}分类的3条通知：")
            for notice in category_notices:
                print(f"- {notice['title']}")
        
        # 测试获取紧急通知
        urgent_notices = notice_service.get_urgent_notices(limit=3)
        print(f"\n紧急通知（前3条）：")
        if urgent_notices:
            for notice in urgent_notices:
                print(f"- {notice['title']}")
        else:
            print("暂无紧急通知")
            
    except Exception as e:
        print(f"导入失败: {str(e)}")

if __name__ == '__main__':
    test_import_notices()
