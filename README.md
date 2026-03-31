# Django Intro Polls

Django 官方教程对应的入门项目，实现了一个简单的投票系统。

## 项目概述

- 基于 Django 6.0.3
- 使用 SQLite 作为默认数据库
- 提供投票列表、详情、投票结果页面
- 使用类视图过滤未来发布时间的问题
- 提供后台管理页面，可在 Admin 中维护问题和选项
- 提供 `seed.py` 脚本用于快速生成示例投票数据
- 包含基础单元测试示例

## 项目结构

```text
.
├── manage.py
├── mysite/                 # 项目配置
├── polls/                  # 投票应用
├── templates/              # 全局模板覆盖（如 admin）
├── seed.py                 # 初始化示例数据脚本
└── db.sqlite3              # 本地 SQLite 数据库（开发环境），执行 runserver 会自动生成
```

## 环境要求

- Python 3.12+
- pip

## 安装依赖

建议先创建虚拟环境：

```bash
python -m venv .django-intro
source .django-intro/bin/activate
pip install -r requirements.txt
```

## 初始化项目

执行数据库迁移：

```bash
cd django-intro
python manage.py migrate
```

如需创建管理员账号（可选，用于后台页面登入）：

```bash
python manage.py createsuperuser
```

如需填充示例数据（建议）：

```bash
python seed.py
```

## 运行项目

启动开发服务器：

```bash
python manage.py runserver
```

启动后可访问：

- 投票首页: `http://127.0.0.1:8000/polls/`
- 管理后台: `http://127.0.0.1:8000/admin/`
- Debug Toolbar: 开发模式下自动注入到页面中

## 运行测试

```bash
python manage.py test
```

## 说明

- 项目时区配置为 `Asia/Shanghai`
- 默认开启 `DEBUG = True`，仅适用于本地开发
- `polls` 应用中过滤了未来发布时间的问题，避免未发布内容提前展示

## 依赖说明

当前仓库代码中能明确确认的运行依赖如下：

- Django 6.0.3
- django-debug-toolbar
