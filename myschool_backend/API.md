# Myschool Backend — API 文档

## 基础信息

| 项 | 说明 |
|----|------|
| 协议 | HTTP |
| 数据格式 | JSON，`UTF-8`，中文不转义为 `\uXXXX` |
| 跨域 | 已启用 CORS，浏览器前端可直接调用 |
| 默认监听 | **`0.0.0.0`**（所有网卡），端口默认 `5000` |

服务绑定在 **`0.0.0.0`**，不是只监听 `127.0.0.1`，因此：

- 本机访问：`http://127.0.0.1:<端口>` 或 `http://localhost:<端口>`
- 同一局域网内其它设备：`http://<这台电脑的局域网IP>:<端口>`（如 `http://192.168.1.10:5000`）

## 接口列表

### 1. 健康检查

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/health` |
| **说明** | 判断服务是否存活 |

**响应 200**

```json
{ "status": "ok" }
```

### 2. 检查用户是否存在

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/auth/check` |
| **说明** | 检查学号是否已注册 |

**请求体 JSON**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `student_id` | string | 是 | 学号，长度至少 8 位 |

**响应 200**

```json
{
  "status": "success",
  "data": {
    "exists": true
  }
}
```

**响应 400**

```json
{ "status": "error", "message": "学号不能为空" }
```

### 3. 用户注册

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/auth/register` |
| **说明** | 注册新用户 |

**请求体 JSON**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `student_id` | string | 是 | 学号，长度至少 8 位 |
| `password` | string | 是 | 密码，长度至少 6 位 |

**响应 201**

```json
{
  "status": "success",
  "message": "注册成功",
  "data": {
    "student_id": "12345678",
    "user_id": 1,
    "token": "token_12345678_1234567890"
  }
}
```

**响应 400**

```json
{ "status": "error", "message": "学号和密码不能为空" }
```

**响应 500**

```json
{ "status": "error", "message": "学号已被注册" }
```

### 4. 用户登录

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/auth/login` |
| **说明** | 用户登录 |

**请求体 JSON**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `student_id` | string | 是 | 学号，长度至少 8 位 |
| `password` | string | 是 | 密码，长度至少 6 位 |

**响应 200**

```json
{
  "status": "success",
  "message": "登录成功",
  "data": {
    "student_id": "12345678",
    "user_id": 1,
    "token": "token_12345678_1234567890"
  }
}
```

**响应 400**

```json
{ "status": "error", "message": "学号和密码不能为空" }
```

**响应 500**

```json
{ "status": "error", "message": "学号或密码错误" }
```

### 5. 获取通知列表

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/notices` |
| **说明** | 获取通知列表，支持分页、分类和标签筛选 |

**查询参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | integer | 否 | 页码，默认 1 |
| `per_page` | integer | 否 | 每页数量，默认 10 |
| `category` | string | 否 | 分类名称 |
| `tag` | string | 否 | 标签名称 |
| `keyword` | string | 否 | 关键词搜索 |

**响应 200**

```json
{
  "total": 32,
  "page": 1,
  "perPage": 10,
  "pages": 4,
  "items": [
    {
      "title": "关于做好2026年清明节假期学生教育管理工作的通知",
      "url": "",
      "date": "2026-04-01",
      "category": "general",
      "tags": ["假期", "教育管理"],
      "content": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
      "publishDate": null,
      "department": "学生处",
      "attachments": [],
      "sourceUrl": ""
    }
  ]
}
```

### 6. 获取最新通知

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/notices/latest` |
| **说明** | 获取最新通知 |

**查询参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | integer | 否 | 数量限制，默认 10 |

**响应 200**

```json
{
  "status": "success",
  "data": [
    {
      "id": "n001",
      "title": "关于做好2026年清明节假期学生教育管理工作的通知",
      "summary": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
      "content": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
      "category": "general",
      "source": "学生处",
      "publishDate": 1743561600,
      "isRead": false,
      "isImportant": false,
      "isUrgent": false,
      "attachments": [],
      "url": "",
      "sourceURL": "",
      "tags": ["假期", "教育管理"]
    }
  ]
}
```

### 7. 获取紧急通知

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/notices/urgent` |
| **说明** | 获取紧急通知 |

**查询参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `limit` | integer | 否 | 数量限制，默认 10 |

**响应 200**

```json
{
  "status": "success",
  "data": [
    {
      "id": "n001",
      "title": "关于做好2026年清明节假期学生教育管理工作的通知",
      "summary": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
      "content": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
      "category": "general",
      "source": "学生处",
      "publishDate": 1743561600,
      "isRead": false,
      "isImportant": false,
      "isUrgent": true,
      "attachments": [],
      "url": "",
      "sourceURL": "",
      "tags": ["假期", "教育管理"]
    }
  ]
}
```

### 8. 获取通知详情

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/notices/{notice_id}` |
| **说明** | 获取通知详情 |

**路径参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notice_id` | string | 是 | 通知 ID |

**响应 200**

```json
{
  "status": "success",
  "data": {
    "id": "n001",
    "title": "关于做好2026年清明节假期学生教育管理工作的通知",
    "summary": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
    "content": "各学院：根据学校《关于2026年部分节假日安排的通知》...",
    "category": "general",
    "source": "学生处",
    "publishDate": 1743561600,
    "isRead": false,
    "isImportant": false,
    "isUrgent": false,
    "attachments": [],
    "url": "",
    "sourceURL": "",
    "tags": ["假期", "教育管理"]
  }
}
```

**响应 404**

```json
{ "status": "error", "message": "通知不存在" }
```

### 9. 保存通知

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/notices` |
| **说明** | 保存通知（前端暂时不使用） |

**请求体 JSON**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 通知标题 |
| `content` | string | 是 | 通知内容 |
| `category` | string | 是 | 分类名称 |
| `source` | string | 否 | 发布来源 |
| `publishDate` | number | 否 | 发布时间戳 |
| `isRead` | boolean | 否 | 是否已读 |
| `isImportant` | boolean | 否 | 是否重要 |
| `isUrgent` | boolean | 否 | 是否紧急 |
| `attachments` | array | 否 | 附件列表 |
| `url` | string | 否 | 通知链接 |
| `sourceURL` | string | 否 | 来源链接 |
| `tags` | array | 否 | 标签列表 |

**响应 200**

```json
{ "status": "success", "message": "通知保存成功" }
```

**响应 400**

```json
{ "status": "error", "message": "请提供通知数据" }
```

### 10. 获取分类统计

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `GET /api/categories` |
| **说明** | 获取分类统计信息 |

**响应 200**

```json
{
  "categories": [
    {
      "name": "academic",
      "count": 3,
      "tags": ["教学", "课程", "考试"]
    },
    {
      "name": "general",
      "count": 3,
      "tags": ["假期", "教育管理", "通知"]
    }
  ],
  "total_notices": 32,
  "all_tags": ["假期", "教育管理", "教学", "课程", "考试"]
}
```

### 11. 导入通知数据

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/import` |
| **说明** | 导入通知数据 |

**查询参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `path` | string | 是 | JSON 文件路径 |

**响应 200**

```json
{ "status": "success", "message": "通知导入成功" }
```

**响应 400**

```json
{ "status": "error", "message": "请提供 JSON 文件路径" }
```

**响应 500**

```json
{ "status": "error", "message": "导入失败: 错误信息" }
```

### 12. 教师发布通知

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/notices/add` |
| **说明** | 教师发布通知 |

**请求体 JSON**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 通知标题 |
| `content` | string | 是 | 通知内容 |
| `category` | string | 是 | 分类名称 |
| `tags` | string | 否 | 标签，英文逗号分隔 |
| `department` | string | 否 | 发布部门 |

**响应 200**

```json
{ "status": "success", "message": "通知保存成功" }
```

**响应 400**

```json
{ "status": "error", "message": "请提供通知数据" }
```

### 13. 触发爬虫

| 项 | 内容 |
|----|------|
| **方法 / 路径** | `POST /api/crawl/trigger` |
| **说明** | 触发爬取通知并保存到数据库 |

**响应 200**

```json
{ "status": "success", "message": "爬取并保存成功，共获取 15 条通知" }
```

**响应 500**

```json
{ "status": "error", "message": "爬取出错: 错误信息" }
```

## 数据结构

### 用户数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `student_id` | string | 学号 |
| `user_id` | integer | 用户 ID |
| `token` | string | 认证令牌 |

### 通知数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 通知 ID |
| `title` | string | 通知标题 |
| `summary` | string | 通知摘要 |
| `content` | string | 通知内容 |
| `category` | string | 分类名称 |
| `source` | string | 发布来源 |
| `publishDate` | number | 发布时间戳 |
| `isRead` | boolean | 是否已读 |
| `isImportant` | boolean | 是否重要 |
| `isUrgent` | boolean | 是否紧急 |
| `attachments` | array | 附件列表 |
| `url` | string | 通知链接 |
| `sourceURL` | string | 来源链接 |
| `tags` | array | 标签列表 |

### 分类统计数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 分类名称 |
| `count` | integer | 通知数量 |
| `tags` | array | 标签列表 |

## 错误处理

所有错误响应格式统一为：

```json
{ "status": "error", "message": "错误信息" }
```

常见错误信息：
- `学号不能为空`：请求缺少学号参数
- `密码不能为空`：请求缺少密码参数
- `学号或密码错误`：登录时学号或密码不正确
- `学号已被注册`：注册时学号已存在
- `网络错误`：网络连接问题
- `服务器错误`：服务器内部错误

## 示例请求

### 检查用户是否存在

```bash
curl -X POST http://localhost:5000/api/auth/check \
  -H "Content-Type: application/json" \
  -d '{"student_id": "12345678"}'
```

### 用户注册

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"student_id": "12345678", "password": "123456"}'
```

### 用户登录

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"student_id": "12345678", "password": "123456"}'
```

## 注意事项

- 密码长度至少为 6 位
- 学号长度至少为 8 位
- 未注册的学号会自动创建账户
- 密码使用 SHA256 哈希存储，保证安全性
- 生产环境建议使用 JWT 进行认证
