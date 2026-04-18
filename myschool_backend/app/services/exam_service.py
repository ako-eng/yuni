import sqlite3
import os
import uuid

class ExamService:
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
            # 确保考试表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exams (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    course_name TEXT NOT NULL,
                    exam_date REAL NOT NULL,
                    location TEXT,
                    seat_number TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_exams(self, user_id):
        """获取用户的考试列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM exams WHERE user_id = ? ORDER BY exam_date ASC', (user_id,))
            exams = cursor.fetchall()
            
            result = []
            for exam in exams:
                result.append({
                    'id': exam[0],
                    'course_name': exam[2],
                    'exam_date': exam[3],
                    'location': exam[4],
                    'seat_number': exam[5]
                })
            
            return result
    
    def get_exam_by_id(self, exam_id, user_id):
        """根据 ID 获取考试"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM exams WHERE id = ? AND user_id = ?', (exam_id, user_id))
            exam = cursor.fetchone()
            
            if not exam:
                return None
            
            return {
                'id': exam[0],
                'course_name': exam[2],
                'exam_date': exam[3],
                'location': exam[4],
                'seat_number': exam[5]
            }
    
    def add_exam(self, exam_data, user_id):
        """添加考试"""
        exam_id = exam_data.get('id', str(uuid.uuid4()))
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否已存在
            cursor.execute('SELECT id FROM exams WHERE id = ? AND user_id = ?', (exam_id, user_id))
            if cursor.fetchone():
                return {'status': 'error', 'message': '考试已存在'}
            
            # 插入考试
            cursor.execute('''
                INSERT INTO exams 
                (id, user_id, course_name, exam_date, location, seat_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                exam_id,
                user_id,
                exam_data.get('course_name', ''),
                exam_data.get('exam_date', 0),
                exam_data.get('location', ''),
                exam_data.get('seat_number', '')
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '考试添加成功', 'data': {'exam_id': exam_id}}
    
    def update_exam(self, exam_id, exam_data, user_id):
        """更新考试"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM exams WHERE id = ? AND user_id = ?', (exam_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '考试不存在'}
            
            # 更新考试
            cursor.execute('''
                UPDATE exams SET 
                    course_name = ?, exam_date = ?, location = ?, seat_number = ?
                WHERE id = ? AND user_id = ?
            ''', (
                exam_data.get('course_name', ''),
                exam_data.get('exam_date', 0),
                exam_data.get('location', ''),
                exam_data.get('seat_number', ''),
                exam_id,
                user_id
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '考试更新成功'}
    
    def delete_exam(self, exam_id, user_id):
        """删除考试"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM exams WHERE id = ? AND user_id = ?', (exam_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '考试不存在'}
            
            # 删除考试
            cursor.execute('DELETE FROM exams WHERE id = ? AND user_id = ?', (exam_id, user_id))
            conn.commit()
            
            return {'status': 'success', 'message': '考试删除成功'}
