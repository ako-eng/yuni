import sqlite3
import os
import time

class SearchService:
    def __init__(self, db_path=None):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'notice.db')
        self._init_db()
    
    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 确保搜索历史表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    keyword TEXT NOT NULL,
                    search_time REAL NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            # 确保热门搜索表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hot_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL UNIQUE,
                    count INTEGER DEFAULT 1
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_search_history(self, user_id, limit=10):
        """获取用户的搜索历史"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT keyword, search_time FROM search_history 
                WHERE user_id = ? 
                ORDER BY search_time DESC 
                LIMIT ?
            ''', (user_id, limit))
            history = cursor.fetchall()
            
            result = []
            for item in history:
                result.append({
                    'keyword': item[0],
                    'search_time': item[1]
                })
            
            return result
    
    def add_search_history(self, user_id, keyword):
        """添加搜索历史"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 添加到搜索历史
            cursor.execute('''
                INSERT INTO search_history (user_id, keyword, search_time)
                VALUES (?, ?, ?)
            ''', (user_id, keyword, time.time()))
            
            # 更新热门搜索
            cursor.execute('''
                INSERT INTO hot_searches (keyword, count)
                VALUES (?, 1)
                ON CONFLICT(keyword) DO UPDATE SET count = count + 1
            ''', (keyword,))
            
            conn.commit()
            
            return {'status': 'success', 'message': '搜索历史添加成功'}
    
    def delete_search_history(self, user_id, keyword=None):
        """删除搜索历史"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if keyword:
                # 删除指定关键词的搜索历史
                cursor.execute('''
                    DELETE FROM search_history 
                    WHERE user_id = ? AND keyword = ?
                ''', (user_id, keyword))
            else:
                # 删除所有搜索历史
                cursor.execute('''
                    DELETE FROM search_history 
                    WHERE user_id = ?
                ''', (user_id,))
            
            conn.commit()
            
            return {'status': 'success', 'message': '搜索历史删除成功'}
    
    def get_hot_searches(self, limit=10):
        """获取热门搜索"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT keyword, count FROM hot_searches 
                ORDER BY count DESC 
                LIMIT ?
            ''', (limit,))
            hot_searches = cursor.fetchall()
            
            result = []
            for item in hot_searches:
                result.append({
                    'keyword': item[0],
                    'count': item[1]
                })
            
            return result
