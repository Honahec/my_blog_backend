# Blog Backend

基于 Django 和 Django REST Framework 构建的博客后端 API。

## 技术栈

- Python 3.10
- Django 4.x
- Django REST Framework
- SQLite (开发环境)

## 功能特性

- 文章管理
  - 创建、读取、更新、删除（CRUD）操作
  - 支持草稿和发布状态
  - 自动生成 URL 友好的 slug（支持中英文）
  - 标签系统
  - 文章摘要
  - 特色图片

- 用户认证
  - Token 认证
  - 用户注册和登录
  - 权限控制

- API 功能
  - 文章列表和详情
  - 按标题搜索
  - 按标签筛选
  - 按日期范围筛选
  - 排序功能

## 开发环境设置

1. 创建虚拟环境：
```bash
python -m venv .venv
```

2. 激活虚拟环境：
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 运行数据库迁移：
```bash
python manage.py migrate
```

5. 创建超级用户：
```bash
python manage.py createsuperuser
```

6. 启动开发服务器：
```bash
python manage.py runserver
```

## API 端点

### 认证相关

- `POST /api/auth/register/`: 用户注册
- `POST /api/auth/login/`: 用户登录
- `POST /api/auth/logout/`: 用户登出
- `GET /api/auth/user/`: 获取当前用户信息

### 文章相关

- `GET /api/posts/`: 获取文章列表
- `POST /api/posts/`: 创建新文章
- `GET /api/posts/<slug>/`: 获取文章详情
- `PUT /api/posts/<slug>/`: 更新文章
- `DELETE /api/posts/<slug>/`: 删除文章
- `GET /api/posts/published/`: 获取已发布文章
- `GET /api/posts/drafts/`: 获取草稿（需要管理员权限）
- `GET /api/posts/tags/`: 获取所有标签列表

### 查询参数

文章列表支持以下查询参数：

- `search`: 搜索标题、内容和摘要
- `tags`: 按标签筛选（逗号分隔）
- `start_date`: 开始日期
- `end_date`: 结束日期
- `ordering`: 排序字段（created_at、-created_at、title、-title）

## 部署注意事项

1. 更新 `settings.py` 中的配置：
   - 设置 `SECRET_KEY`
   - 配置 `ALLOWED_HOSTS`
   - 配置数据库连接
   - 配置静态文件存储

2. 收集静态文件：
```bash
python manage.py collectstatic
```

3. 配置生产环境 Web 服务器（如 Nginx + Gunicorn）

4. 设置 SSL 证书

## 开发规范

1. 代码风格遵循 PEP 8
2. 使用 Django 的 ORM 进行数据库操作
3. 使用 Django REST Framework 的序列化器处理数据验证
4. 适当使用缓存提高性能
5. 编写测试用例确保代码质量 