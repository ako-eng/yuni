import sqlite3
import json
from datetime import datetime
import os

class NoticeService:
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
                    avatar_name TEXT
                )
            ''')
            
            # 创建通知表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notices (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    summary TEXT,
                    content TEXT NOT NULL,
                    category TEXT NOT NULL,
                    source TEXT,
                    publish_date REAL NOT NULL,
                    is_read INTEGER DEFAULT 0,
                    is_important INTEGER DEFAULT 0,
                    is_urgent INTEGER DEFAULT 0,
                    attachments TEXT,
                    url TEXT,
                    source_url TEXT,
                    tags TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # 创建课程表
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
            
            # 创建成绩表
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
            
            # 创建考试表
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
            
            # 创建获奖表
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
            
            # 创建搜索历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    keyword TEXT NOT NULL,
                    search_time REAL NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # 创建热门搜索表
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
    
    def _date_to_timestamp(self, date_str):
        if not date_str:
            return datetime.now().timestamp()
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').timestamp()
        except ValueError:
            return datetime.now().timestamp()
    
    def _timestamp_to_date(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    
    def _serialize_list(self, data):
        return json.dumps(data) if data else '[]'
    
    def _deserialize_list(self, data):
        return json.loads(data) if data else []
    
    def import_from_json(self, json_path, user_id=None):
        with open(json_path, 'r', encoding='utf-8') as f:
            notices = json.load(f)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for i, notice in enumerate(notices):
                notice_id = f"n{i+1:03d}"
                
                # 检查是否已存在
                if user_id:
                    cursor.execute('SELECT id FROM notices WHERE id = ? AND user_id = ?', (notice_id, user_id))
                else:
                    cursor.execute('SELECT id FROM notices WHERE id = ?', (notice_id,))
                if cursor.fetchone():
                    continue
                
                # 处理分类映射
                category = notice.get('category', '综合通知')
                if '教务' in category:
                    category = 'academic'
                elif '考试' in category:
                    category = 'exam'
                elif '竞赛' in category:
                    category = 'competition'
                elif '科研' in category:
                    category = 'research'
                elif '生活' in category:
                    category = 'life'
                elif '校企' in category:
                    category = 'enterprise'
                elif '保卫' in category:
                    category = 'security'
                elif '后勤' in category:
                    category = 'logistics'
                elif '图书馆' in category:
                    category = 'library'
                else:
                    category = 'general'
                
                # 处理数据
                title = notice.get('title', '')
                content = notice.get('content', '')
                summary = content[:100] + '...' if len(content) > 100 else content
                source = notice.get('department', notice.get('source', '未知'))
                publish_date = self._date_to_timestamp(notice.get('date', ''))
                attachments = self._serialize_list(notice.get('attachments', []))
                url = notice.get('url', '')
                source_url = notice.get('source_url', '')
                tags = self._serialize_list(notice.get('tags', []))
                
                # 插入数据
                if user_id:
                    cursor.execute('''
                        INSERT INTO notices 
                        (id, user_id, title, summary, content, category, source, publish_date, 
                         is_read, is_important, is_urgent, attachments, url, source_url, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?, ?)
                    ''', (notice_id, user_id, title, summary, content, category, source, publish_date, 
                          attachments, url, source_url, tags))
                else:
                    cursor.execute('''
                        INSERT INTO notices 
                        (id, title, summary, content, category, source, publish_date, 
                         is_read, is_important, is_urgent, attachments, url, source_url, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?, ?)
                    ''', (notice_id, title, summary, content, category, source, publish_date, 
                          attachments, url, source_url, tags))
            conn.commit()
    
    def get_notices(self, user_id=None, category=None, tags=None, is_urgent=None, limit=20, offset=0):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM notices WHERE 1=1'
            params = []
            
            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)
            
            if category:
                query += ' AND category = ?'
                params.append(category)
            
            if tags:
                for tag in tags:
                    query += ' AND tags LIKE ?'
                    params.append(f'%{tag}%')
            
            if is_urgent is not None:
                query += ' AND is_urgent = ?'
                params.append(1 if is_urgent else 0)
            
            query += ' ORDER BY publish_date DESC LIMIT ? OFFSET ?'
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            notices = cursor.fetchall()
            
            result = []
            for notice in notices:
                result.append({
                    'id': notice[0],
                    'title': notice[2],
                    'summary': notice[3],
                    'content': notice[4],
                    'category': notice[5],
                    'source': notice[6],
                    'publishDate': notice[7],
                    'isRead': bool(notice[8]),
                    'isImportant': bool(notice[9]),
                    'isUrgent': bool(notice[10]),
                    'attachments': self._deserialize_list(notice[11]),
                    'url': notice[12],
                    'sourceURL': notice[13],
                    'tags': self._deserialize_list(notice[14])
                })
            
            return result
    
    def get_latest_notices(self, user_id=None, limit=10):
        return self.get_notices(user_id=user_id, limit=limit)
    
    def get_urgent_notices(self, user_id=None, limit=10):
        return self.get_notices(user_id=user_id, is_urgent=True, limit=limit)
    
    def get_notice_by_id(self, notice_id, user_id=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute('SELECT * FROM notices WHERE id = ? AND user_id = ?', (notice_id, user_id))
            else:
                cursor.execute('SELECT * FROM notices WHERE id = ?', (notice_id,))
            notice = cursor.fetchone()
            
            if not notice:
                return None
            
            return {
                'id': notice[0],
                'title': notice[2],
                'summary': notice[3],
                'content': notice[4],
                'category': notice[5],
                'source': notice[6],
                'publishDate': notice[7],
                'isRead': bool(notice[8]),
                'isImportant': bool(notice[9]),
                'isUrgent': bool(notice[10]),
                'attachments': self._deserialize_list(notice[11]),
                'url': notice[12],
                'sourceURL': notice[13],
                'tags': self._deserialize_list(notice[14])
            }
    
    def save_notice(self, notice_data, user_id=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            notice_id = notice_data.get('id', f"n{int(datetime.now().timestamp())}")
            
            # 检查是否已存在
            if user_id:
                cursor.execute('SELECT id FROM notices WHERE id = ? AND user_id = ?', (notice_id, user_id))
            else:
                cursor.execute('SELECT id FROM notices WHERE id = ?', (notice_id,))
            if cursor.fetchone():
                # 更新现有通知
                if user_id:
                    cursor.execute('''
                        UPDATE notices SET 
                            title = ?, summary = ?, content = ?, category = ?, source = ?, 
                            publish_date = ?, is_read = ?, is_important = ?, is_urgent = ?, 
                            attachments = ?, url = ?, source_url = ?, tags = ?
                        WHERE id = ? AND user_id = ?
                    ''', (
                        notice_data.get('title', ''),
                        notice_data.get('summary', ''),
                        notice_data.get('content', ''),
                        notice_data.get('category', 'general'),
                        notice_data.get('source', ''),
                        notice_data.get('publishDate', datetime.now().timestamp()),
                        1 if notice_data.get('isRead', False) else 0,
                        1 if notice_data.get('isImportant', False) else 0,
                        1 if notice_data.get('isUrgent', False) else 0,
                        self._serialize_list(notice_data.get('attachments', [])),
                        notice_data.get('url', ''),
                        notice_data.get('sourceURL', ''),
                        self._serialize_list(notice_data.get('tags', [])),
                        notice_id,
                        user_id
                    ))
                else:
                    cursor.execute('''
                        UPDATE notices SET 
                            title = ?, summary = ?, content = ?, category = ?, source = ?, 
                            publish_date = ?, is_read = ?, is_important = ?, is_urgent = ?, 
                            attachments = ?, url = ?, source_url = ?, tags = ?
                        WHERE id = ?
                    ''', (
                        notice_data.get('title', ''),
                        notice_data.get('summary', ''),
                        notice_data.get('content', ''),
                        notice_data.get('category', 'general'),
                        notice_data.get('source', ''),
                        notice_data.get('publishDate', datetime.now().timestamp()),
                        1 if notice_data.get('isRead', False) else 0,
                        1 if notice_data.get('isImportant', False) else 0,
                        1 if notice_data.get('isUrgent', False) else 0,
                        self._serialize_list(notice_data.get('attachments', [])),
                        notice_data.get('url', ''),
                        notice_data.get('sourceURL', ''),
                        self._serialize_list(notice_data.get('tags', [])),
                        notice_id
                    ))
            else:
                # 插入新通知
                if user_id:
                    cursor.execute('''
                        INSERT INTO notices 
                        (id, user_id, title, summary, content, category, source, publish_date, 
                         is_read, is_important, is_urgent, attachments, url, source_url, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        notice_id,
                        user_id,
                        notice_data.get('title', ''),
                        notice_data.get('summary', ''),
                        notice_data.get('content', ''),
                        notice_data.get('category', 'general'),
                        notice_data.get('source', ''),
                        notice_data.get('publishDate', datetime.now().timestamp()),
                        1 if notice_data.get('isRead', False) else 0,
                        1 if notice_data.get('isImportant', False) else 0,
                        1 if notice_data.get('isUrgent', False) else 0,
                        self._serialize_list(notice_data.get('attachments', [])),
                        notice_data.get('url', ''),
                        notice_data.get('sourceURL', ''),
                        self._serialize_list(notice_data.get('tags', []))
                    ))
                else:
                    cursor.execute('''
                        INSERT INTO notices 
                        (id, title, summary, content, category, source, publish_date, 
                         is_read, is_important, is_urgent, attachments, url, source_url, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        notice_id,
                        notice_data.get('title', ''),
                        notice_data.get('summary', ''),
                        notice_data.get('content', ''),
                        notice_data.get('category', 'general'),
                        notice_data.get('source', ''),
                        notice_data.get('publishDate', datetime.now().timestamp()),
                        1 if notice_data.get('isRead', False) else 0,
                        1 if notice_data.get('isImportant', False) else 0,
                        1 if notice_data.get('isUrgent', False) else 0,
                        self._serialize_list(notice_data.get('attachments', [])),
                        notice_data.get('url', ''),
                        notice_data.get('sourceURL', ''),
                        self._serialize_list(notice_data.get('tags', []))
                    ))
            
            conn.commit()
            return {'status': 'success', 'message': '通知保存成功'}
    
    def get_categories(self, user_id=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute('SELECT DISTINCT category FROM notices WHERE user_id = ?', (user_id,))
            else:
                cursor.execute('SELECT DISTINCT category FROM notices')
            categories = cursor.fetchall()
            return [cat[0] for cat in categories]
