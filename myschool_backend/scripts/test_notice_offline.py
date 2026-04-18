import os
import sys
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services.notice_service import NoticeService

def test_notice_service():
    """在不启动服务的情况下测试通知服务"""
    print("=== 测试通知服务 ===")
    
    # 创建通知服务实例
    notice_service = NoticeService()
    
    # 测试1: 获取最新通知
    print("\n1. 测试获取最新通知:")
    try:
        latest_notices = notice_service.get_latest_notices(limit=5)
        print(f"   成功获取 {len(latest_notices)} 条最新通知")
        for i, notice in enumerate(latest_notices):
            print(f"   {i+1}. {notice['title']} ({notice['category']})")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    # 测试2: 获取分类
    print("\n2. 测试获取分类:")
    try:
        categories = notice_service.get_categories()
        print(f"   成功获取 {len(categories)} 个分类")
        for category in categories:
            print(f"   - {category}")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    # 测试3: 按分类获取通知
    print("\n3. 测试按分类获取通知:")
    try:
        categories = notice_service.get_categories()
        if categories:
            category = categories[0]
            category_notices = notice_service.get_notices(category=category, limit=3)
            print(f"   成功获取 {category} 分类的 {len(category_notices)} 条通知")
            for i, notice in enumerate(category_notices):
                print(f"   {i+1}. {notice['title']}")
        else:
            print("   没有分类可供测试")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    # 测试4: 获取通知详情
    print("\n4. 测试获取通知详情:")
    try:
        latest_notices = notice_service.get_latest_notices(limit=1)
        if latest_notices:
            notice_id = latest_notices[0]['id']
            notice = notice_service.get_notice_by_id(notice_id)
            print(f"   成功获取通知详情: {notice['title']}")
        else:
            print("   没有通知可供测试")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    # 测试5: 保存通知
    print("\n5. 测试保存通知:")
    try:
        test_notice = {
            'title': '测试通知',
            'content': '这是一条测试通知',
            'category': 'general',
            'source': '测试部门',
            'tags': ['测试', '通知']
        }
        result = notice_service.save_notice(test_notice)
        print(f"   成功保存通知: {result['message']}")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    # 测试6: 统计通知数量
    print("\n6. 测试统计通知数量:")
    try:
        all_notices = notice_service.get_notices(limit=1000)
        print(f"   数据库中共有 {len(all_notices)} 条通知")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_notice_service()
