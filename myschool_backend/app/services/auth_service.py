import sqlite3
import os
import time
import hashlib

class AuthService:
    def __init__(self, db_path=None):
        """初始化认证服务"""
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'notice.db')
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT,
                    department TEXT,
                    major TEXT,
                    grade TEXT,
                    avatar_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def _get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def _hash_password(self, password):
        """对密码进行哈希处理"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, student_id, password, name=None, department=None, major=None, grade=None, avatar_name=None):
        """注册新用户"""
        # 检查用户是否已存在
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE student_id = ?', (student_id,))
            if cursor.fetchone():
                raise Exception('学号已被注册')
            
            # 注册新用户
            hashed_password = self._hash_password(password)
            cursor.execute('''
                INSERT INTO users (student_id, password, name, department, major, grade, avatar_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, hashed_password, name, department, major, grade, avatar_name))
            conn.commit()
            user_id = cursor.lastrowid
        
        # 生成 token
        token = f"token_{student_id}_{int(time.time())}"
        
        return {
            'status': 'success',
            'message': '注册成功',
            'data': {
                'student_id': student_id,
                'user_id': user_id,
                'name': name,
                'department': department,
                'major': major,
                'grade': grade,
                'avatar_name': avatar_name,
                'token': token
            }
        }
    
    def login(self, student_id, password):
        """用户登录"""
        # 检查用户是否存在
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, password, name, department, major, grade, avatar_name 
                FROM users WHERE student_id = ?
            ''', (student_id,))
            user = cursor.fetchone()
            
            if not user:
                raise Exception('学号或密码错误')
            
            # 验证密码
            user_id, stored_password, name, department, major, grade, avatar_name = user
            hashed_password = self._hash_password(password)
            if hashed_password != stored_password:
                raise Exception('学号或密码错误')
        
        # 生成 token
        token = f"token_{student_id}_{int(time.time())}"
        
        return {
            'status': 'success',
            'message': '登录成功',
            'data': {
                'student_id': student_id,
                'user_id': user_id,
                'name': name,
                'department': department,
                'major': major,
                'grade': grade,
                'avatar_name': avatar_name,
                'token': token
            }
        }
    
    def check_user_exists(self, student_id):
        """检查用户是否存在"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE student_id = ?', (student_id,))
            return cursor.fetchone() is not None
    
    def get_user_info(self, user_id):
        """获取用户信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, student_id, name, department, major, grade, avatar_name 
                FROM users WHERE id = ?
            ''', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise Exception('用户不存在')
            
            return {
                'id': user[0],
                'student_id': user[1],
                'name': user[2],
                'department': user[3],
                'major': user[4],
                'grade': user[5],
                'avatar_name': user[6]
            }
    
    def update_user_info(self, user_id, name=None, department=None, major=None, grade=None, avatar_name=None):
        """更新用户信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建更新语句
            update_fields = []
            params = []
            
            if name is not None:
                update_fields.append('name = ?')
                params.append(name)
            if department is not None:
                update_fields.append('department = ?')
                params.append(department)
            if major is not None:
                update_fields.append('major = ?')
                params.append(major)
            if grade is not None:
                update_fields.append('grade = ?')
                params.append(grade)
            if avatar_name is not None:
                update_fields.append('avatar_name = ?')
                params.append(avatar_name)
            
            if not update_fields:
                return {'status': 'success', 'message': '无更新内容'}
            
            # 执行更新
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            
            return {'status': 'success', 'message': '用户信息更新成功'}
