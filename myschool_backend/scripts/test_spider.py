import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services.spider_service import SpiderService

def test_spider_service():
    """测试爬虫服务"""
    print("=== 测试爬虫服务 ===")
    
    # 创建爬虫服务实例
    spider_service = SpiderService()
    
    # 测试爬取通知
    print("\n1. 测试爬取通知:")
    try:
        result = spider_service.crawl_notices(max_pages=2)
        if result['status'] == 'success':
            notices = result['data']
            print(f"   成功爬取 {len(notices)} 条通知")
            for i, notice in enumerate(notices[:5]):
                print(f"   {i+1}. {notice['title']} ({notice['date']}) [{notice['category']}]")
        else:
            print(f"   失败: {result['message']}")
    except Exception as e:
        print(f"   失败: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_spider_service()
