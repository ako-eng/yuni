import sqlite3
import os
import uuid

class AwardService:
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
            # 确保获奖表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS awards (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    level TEXT NOT NULL,
                    date REAL NOT NULL,
                    category TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_awards(self, user_id):
        """获取用户的获奖列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM awards WHERE user_id = ? ORDER BY date DESC', (user_id,))
            awards = cursor.fetchall()
            
            result = []
            for award in awards:
                result.append({
                    'id': award[0],
                    'name': award[2],
                    'level': award[3],
                    'date': award[4],
                    'category': award[5]
                })
            
            return result
    
    def get_award_by_id(self, award_id, user_id):
        """根据 ID 获取获奖"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM awards WHERE id = ? AND user_id = ?', (award_id, user_id))
            award = cursor.fetchone()
            
            if not award:
                return None
            
            return {
                'id': award[0],
                'name': award[2],
                'level': award[3],
                'date': award[4],
                'category': award[5]
            }
    
    def add_award(self, award_data, user_id):
        """添加获奖"""
        award_id = award_data.get('id', str(uuid.uuid4()))
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否已存在
            cursor.execute('SELECT id FROM awards WHERE id = ? AND user_id = ?', (award_id, user_id))
            if cursor.fetchone():
                return {'status': 'error', 'message': '获奖记录已存在'}
            
            # 插入获奖
            cursor.execute('''
                INSERT INTO awards 
                (id, user_id, name, level, date, category)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                award_id,
                user_id,
                award_data.get('name', ''),
                award_data.get('level', ''),
                award_data.get('date', 0),
                award_data.get('category', '')
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '获奖记录添加成功', 'data': {'award_id': award_id}}
    
    def update_award(self, award_id, award_data, user_id):
        """更新获奖"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM awards WHERE id = ? AND user_id = ?', (award_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '获奖记录不存在'}
            
            # 更新获奖
            cursor.execute('''
                UPDATE awards SET 
                    name = ?, level = ?, date = ?, category = ?
                WHERE id = ? AND user_id = ?
            ''', (
                award_data.get('name', ''),
                award_data.get('level', ''),
                award_data.get('date', 0),
                award_data.get('category', ''),
                award_id,
                user_id
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '获奖记录更新成功'}
    
    def delete_award(self, award_id, user_id):
        """删除获奖"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM awards WHERE id = ? AND user_id = ?', (award_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '获奖记录不存在'}
            
            # 删除获奖
            cursor.execute('DELETE FROM awards WHERE id = ? AND user_id = ?', (award_id, user_id))
            conn.commit()
            
            return {'status': 'success', 'message': '获奖记录删除成功'}
