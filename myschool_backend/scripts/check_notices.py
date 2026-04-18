import os
import sys
import sqlite3

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def check_notices():
    """检查数据库文件中的通知数据"""
    # 定义路径
    project_root = os.path.dirname(os.path.dirname(__file__))
    notice_db_path = os.path.join(project_root, 'data', 'notice.db')
    
    # 检查数据库文件是否存在
    if not os.path.exists(notice_db_path):
        print(f"数据库文件不存在: {notice_db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(notice_db_path)
        cursor = conn.cursor()
        
        # 检查通知表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notices';")
        if not cursor.fetchone():
            print("通知表不存在")
            conn.close()
            return False
        
        # 统计通知数量
        cursor.execute("SELECT COUNT(*) FROM notices;")
        count = cursor.fetchone()[0]
        print(f"数据库中共有 {count} 条通知")
        
        # 查看前5条通知
        if count > 0:
            print("\n前5条通知：")
            cursor.execute("SELECT id, title, category, publish_date FROM notices ORDER BY publish_date DESC LIMIT 5;")
            notices = cursor.fetchall()
            for notice in notices:
                id, title, category, publish_date = notice
                print(f"- {id}: {title} ({category})")
        
        # 查看分类统计
        print("\n分类统计：")
        cursor.execute("SELECT category, COUNT(*) FROM notices GROUP BY category;")
        categories = cursor.fetchall()
        for category, cat_count in categories:
            print(f"- {category}: {cat_count}条")
        
        # 关闭连接
        conn.close()
        
    except Exception as e:
        print(f"检查失败: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    success = check_notices()
    if success:
        print("\n数据库检查完成！")
    else:
        print("\n数据库检查失败！")
        sys.exit(1)
