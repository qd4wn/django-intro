# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 常用命令

```bash
# 激活虚拟环境
source .django-intro/bin/activate

# 启动开发服务器
python manage.py runserver

# 运行测试
python manage.py test

# 运行指定测试模块
python manage.py test polls.tests

# 运行指定测试类
python manage.py test polls.tests.QuestionModelTests

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 生成示例数据
python seed.py
```

## 架构概述

基于 Django 6.0.3 的投票应用，遵循官方教程模式。

### 数据模型

```
Question ──< Choice (ForeignKey, on_delete=CASCADE)
```

- `Question`: question_text, pub_date
- `Choice`: question (外键), choice_text, votes

### 视图

列表页和详情页使用类视图：
- `IndexView` (ListView): 显示最近 5 个已发布问题，过滤掉未来日期的
- `DetailView` (DetailView): 单个问题详情，过滤掉未来日期的
- `ResultsView` (DetailView): 投票结果页
- `vote()` (函数视图): 处理投票 POST 请求

### URL 结构

```
/polls/              → IndexView
/polls/<pk>/         → DetailView
/polls/<pk>/results/ → ResultsView
/polls/<id>/vote/    → vote (POST)
/admin/              → Django admin
```

### 关键模式

- `pub_date__lte=timezone.now()` 过滤掉未来发布的问题
- `F("votes") + 1` 用于投票计数器的原子递增
- 模板位于 `polls/templates/polls/`
- 项目时区: `Asia/Shanghai`

## 依赖

- Django 6.0.3
- django-debug-toolbar (开发环境启用)
