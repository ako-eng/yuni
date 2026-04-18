import sqlite3
import os
import uuid

class GradeService:
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
            # 确保成绩表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    course_name TEXT NOT NULL,
                    credit REAL NOT NULL,
                    score INTEGER NOT NULL,
                    grade_point REAL NOT NULL,
                    semester TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_grades(self, user_id):
        """获取用户的成绩列表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM grades WHERE user_id = ? ORDER BY semester DESC', (user_id,))
            grades = cursor.fetchall()
            
            result = []
            for grade in grades:
                result.append({
                    'id': grade[0],
                    'course_name': grade[2],
                    'credit': grade[3],
                    'score': grade[4],
                    'grade_point': grade[5],
                    'semester': grade[6]
                })
            
            return result
    
    def get_grade_by_id(self, grade_id, user_id):
        """根据 ID 获取成绩"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM grades WHERE id = ? AND user_id = ?', (grade_id, user_id))
            grade = cursor.fetchone()
            
            if not grade:
                return None
            
            return {
                'id': grade[0],
                'course_name': grade[2],
                'credit': grade[3],
                'score': grade[4],
                'grade_point': grade[5],
                'semester': grade[6]
            }
    
    def add_grade(self, grade_data, user_id):
        """添加成绩"""
        grade_id = grade_data.get('id', str(uuid.uuid4()))
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否已存在
            cursor.execute('SELECT id FROM grades WHERE id = ? AND user_id = ?', (grade_id, user_id))
            if cursor.fetchone():
                return {'status': 'error', 'message': '成绩已存在'}
            
            # 插入成绩
            cursor.execute('''
                INSERT INTO grades 
                (id, user_id, course_name, credit, score, grade_point, semester)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                grade_id,
                user_id,
                grade_data.get('course_name', ''),
                grade_data.get('credit', 0.0),
                grade_data.get('score', 0),
                grade_data.get('grade_point', 0.0),
                grade_data.get('semester', '')
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '成绩添加成功', 'data': {'grade_id': grade_id}}
    
    def update_grade(self, grade_id, grade_data, user_id):
        """更新成绩"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM grades WHERE id = ? AND user_id = ?', (grade_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '成绩不存在'}
            
            # 更新成绩
            cursor.execute('''
                UPDATE grades SET 
                    course_name = ?, credit = ?, score = ?, grade_point = ?, semester = ?
                WHERE id = ? AND user_id = ?
            ''', (
                grade_data.get('course_name', ''),
                grade_data.get('credit', 0.0),
                grade_data.get('score', 0),
                grade_data.get('grade_point', 0.0),
                grade_data.get('semester', ''),
                grade_id,
                user_id
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '成绩更新成功'}
    
    def delete_grade(self, grade_id, user_id):
        """删除成绩"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM grades WHERE id = ? AND user_id = ?', (grade_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '成绩不存在'}
            
            # 删除成绩
            cursor.execute('DELETE FROM grades WHERE id = ? AND user_id = ?', (grade_id, user_id))
            conn.commit()
            
            return {'status': 'success', 'message': '成绩删除成功'}
