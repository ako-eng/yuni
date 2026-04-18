import os
import sys
import shutil

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.services.notice_service import NoticeService

def migrate_notices():
    """将旧的 JSON 数据导入到新的数据库文件中"""
    # 定义路径
    project_root = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(project_root, 'data')
    notice_db_path = os.path.join(data_dir, 'notice.db')
    json_path = os.path.join(os.path.dirname(project_root), 'myschool_back', 'gdut_notices.json')
    
    # 确保数据目录存在
    os.makedirs(data_dir, exist_ok=True)
    
    # 清除现有的数据库文件（如果存在）
    if os.path.exists(notice_db_path):
        print(f"现有数据库文件存在: {notice_db_path}")
        # 尝试重命名而不是删除，避免文件占用问题
        backup_path = notice_db_path + '.bak'
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(notice_db_path, backup_path)
        print(f"已将现有数据库文件备份为: {backup_path}")
    
    # 创建通知服务实例
    notice_service = NoticeService(db_path=notice_db_path)
    
    try:
        # 导入数据
        print(f"从 {json_path} 导入通知数据...")
        notice_service.import_from_json(json_path)
        print("通知数据导入成功！")
        
        # 验证导入结果
        print("\n验证导入结果：")
        
        # 获取最新通知
        latest_notices = notice_service.get_latest_notices(limit=5)
        print(f"最新5条通知：")
        for notice in latest_notices:
            print(f"- {notice['title']} ({notice['category']})")
        
        # 获取分类统计
        categories = notice_service.get_categories()
        print(f"\n通知分类统计：")
        total_notices = 0
        for category in categories:
            category_notices = notice_service.get_notices(category=category)
            count = len(category_notices)
            total_notices += count
            print(f"- {category}: {count}条")
        
        print(f"\n总计导入 {total_notices} 条通知")
        print(f"数据库文件已创建：{notice_db_path}")
        
    except Exception as e:
        print(f"导入失败: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    success = migrate_notices()
    if success:
        print("\n数据迁移完成！")
    else:
        print("\n数据迁移失败！")
        sys.exit(1)
