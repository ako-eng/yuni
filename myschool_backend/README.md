# Myschool Backend

校园通知系统后端服务，提供用户认证和通知管理功能。

## 功能特性

- **用户认证**：支持学号登录/注册，密码验证
- **通知管理**：获取通知列表，添加通知，分类统计
- **健康检查**：服务状态监控

## 技术栈

- **框架**：Flask
- **数据库**：SQLite
- **认证**：基于密码的认证机制，密码使用 SHA256 哈希存储

## 目录结构

```
myschool_backend/
├── app/                    # 应用主目录
│   ├── api/                # API 路由模块
│   │   ├── __init__.py     # 初始化蓝图
│   │   ├── auth.py         # 认证相关接口
│   │   └── health.py       # 健康检查接口
│   ├── services/           # 业务逻辑层
│   │   ├── __init__.py
│   │   └── auth_service.py # 认证服务
│   └── __init__.py         # 应用工厂函数
├── data/                   # 数据存储目录
│   └── auth.db             # SQLite 数据库文件
├── requirements.txt        # 依赖包
├── README.md               # 项目说明
└── wsgi.py                 # WSGI 入口
```

## 快速开始

### 安装依赖

```bash
cd myschool_backend
pip install -r requirements.txt
```

### 运行服务

```bash
# 默认端口 5000
python wsgi.py

# 自定义端口
PORT=5001 python wsgi.py
```

### API 接口

#### 1. 健康检查
- **路径**：`GET /api/health`
- **响应**：`{"status": "ok"}`

#### 2. 检查用户是否存在
- **路径**：`POST /api/auth/check`
- **请求体**：`{"student_id": "12345678"}`
- **响应**：`{"status": "success", "data": {"exists": true}}`

#### 3. 用户注册
- **路径**：`POST /api/auth/register`
- **请求体**：`{"student_id": "12345678", "password": "123456"}`
- **响应**：`{"status": "success", "message": "注册成功", "data": {...}}`

#### 4. 用户登录
- **路径**：`POST /api/auth/login`
- **请求体**：`{"student_id": "12345678", "password": "123456"}`
- **响应**：`{"status": "success", "message": "登录成功", "data": {...}}`

## 注意事项

- 密码长度至少为 6 位
- 未注册的学号会自动创建账户
- 数据库文件会自动创建在 `data/auth.db` 中
- 生产环境建议使用 JWT 进行认证

## 部署

可以使用 Gunicorn 作为 WSGI 服务器进行部署：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```
