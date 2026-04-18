import sqlite3
import os
import json

class CourseService:
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
            # 确保课程表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    teacher TEXT,
                    room TEXT,
                    day_of_week INTEGER NOT NULL,
                    start_period INTEGER NOT NULL,
                    end_period INTEGER NOT NULL,
                    color_index INTEGER DEFAULT 0,
                    weeks TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _serialize_list(self, data):
        return json.dumps(data) if data else '[]'
    
    def _deserialize_list(self, data):
        return json.loads(data) if data else []
    
    def get_courses(self, user_id):
        """获取用户的课程表"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE user_id = ? ORDER BY day_of_week, start_period', (user_id,))
            courses = cursor.fetchall()
            
            result = []
            for course in courses:
                result.append({
                    'id': course[0],
                    'name': course[2],
                    'teacher': course[3],
                    'room': course[4],
                    'day_of_week': course[5],
                    'start_period': course[6],
                    'end_period': course[7],
                    'color_index': course[8],
                    'weeks': self._deserialize_list(course[9])
                })
            
            return result
    
    def get_course_by_id(self, course_id, user_id):
        """根据 ID 获取课程"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM courses WHERE id = ? AND user_id = ?', (course_id, user_id))
            course = cursor.fetchone()
            
            if not course:
                return None
            
            return {
                'id': course[0],
                'name': course[2],
                'teacher': course[3],
                'room': course[4],
                'day_of_week': course[5],
                'start_period': course[6],
                'end_period': course[7],
                'color_index': course[8],
                'weeks': self._deserialize_list(course[9])
            }
    
    def add_course(self, course_data, user_id):
        """添加课程"""
        import uuid
        course_id = course_data.get('id', str(uuid.uuid4()))
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否已存在
            cursor.execute('SELECT id FROM courses WHERE id = ? AND user_id = ?', (course_id, user_id))
            if cursor.fetchone():
                return {'status': 'error', 'message': '课程已存在'}
            
            # 插入课程
            cursor.execute('''
                INSERT INTO courses 
                (id, user_id, name, teacher, room, day_of_week, start_period, end_period, color_index, weeks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_id,
                user_id,
                course_data.get('name', ''),
                course_data.get('teacher', ''),
                course_data.get('room', ''),
                course_data.get('day_of_week', 1),
                course_data.get('start_period', 1),
                course_data.get('end_period', 1),
                course_data.get('color_index', 0),
                self._serialize_list(course_data.get('weeks', []))
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '课程添加成功', 'data': {'course_id': course_id}}
    
    def update_course(self, course_id, course_data, user_id):
        """更新课程"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ? AND user_id = ?', (course_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '课程不存在'}
            
            # 更新课程
            cursor.execute('''
                UPDATE courses SET 
                    name = ?, teacher = ?, room = ?, day_of_week = ?, 
                    start_period = ?, end_period = ?, color_index = ?, weeks = ?
                WHERE id = ? AND user_id = ?
            ''', (
                course_data.get('name', ''),
                course_data.get('teacher', ''),
                course_data.get('room', ''),
                course_data.get('day_of_week', 1),
                course_data.get('start_period', 1),
                course_data.get('end_period', 1),
                course_data.get('color_index', 0),
                self._serialize_list(course_data.get('weeks', [])),
                course_id,
                user_id
            ))
            conn.commit()
            
            return {'status': 'success', 'message': '课程更新成功'}
    
    def delete_course(self, course_id, user_id):
        """删除课程"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 检查是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ? AND user_id = ?', (course_id, user_id))
            if not cursor.fetchone():
                return {'status': 'error', 'message': '课程不存在'}
            
            # 删除课程
            cursor.execute('DELETE FROM courses WHERE id = ? AND user_id = ?', (course_id, user_id))
            conn.commit()
            
            return {'status': 'success', 'message': '课程删除成功'}
