# Django Polls API 文档

> 本文档描述 Django 投票应用的 Web 端点。该应用使用模板渲染 HTML 页面，非 REST API。

## 基础信息

- **Base URL**: `http://127.0.0.1:8000`
- **内容类型**: `text/html`
- **认证方式**: 无（公开访问）

---

## 端点列表

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/polls/` | 投票问题列表 |
| GET | `/polls/<pk>/` | 问题详情页 |
| GET | `/polls/<pk>/results/` | 投票结果页 |
| POST | `/polls/<id>/vote/` | 提交投票 |

---

## GET /polls/

### 描述

显示最近 5 个已发布的投票问题列表，按发布时间降序排列。未发布的问题（未来日期）不会显示。

### 参数

无

### 响应

**200 成功**

返回 HTML 页面，包含问题列表：

```html
<ul>
  <li><a href="/polls/1/">问题文本 1</a></li>
  <li><a href="/polls/2/">问题文本 2</a></li>
  ...
</ul>
```

若无问题则显示：

```html
<p>No polls are available.</p>
```

### 示例

**cURL**
```bash
curl -X GET "http://127.0.0.1:8000/polls/"
```

**Python**
```python
import requests

response = requests.get('http://127.0.0.1:8000/polls/')
print(response.text)  # HTML 内容
```

---

## GET /polls/<pk>/

### 描述

显示单个问题的详情页，包含所有选项供用户投票。未发布的问题返回 404。

### 参数

| 名称 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pk | integer | 是 | 问题 ID |

### 响应

**200 成功**

返回 HTML 页面，包含投票表单：

```html
<h1>{{ question.question_text }}</h1>
<form action="/polls/{{ question.id }}/vote/" method="post">
  <input type="radio" name="choice" value="1"> 选项 1<br>
  <input type="radio" name="choice" value="2"> 选项 2<br>
  <button type="submit">投票</button>
</form>
```

**404 未找到**

问题不存在或未发布：

```html
<h1>Not Found</h1>
<p>Question does not exist in db.</p>
```

### 示例

**cURL**
```bash
curl -X GET "http://127.0.0.1:8000/polls/1/"
```

**Python**
```python
response = requests.get('http://127.0.0.1:8000/polls/1/')
if response.status_code == 200:
    print(response.text)
else:
    print("问题未找到")
```

---

## GET /polls/<pk>/results/

### 描述

显示单个问题的投票结果，包含各选项的票数统计。

### 参数

| 名称 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pk | integer | 是 | 问题 ID |

### 响应

**200 成功**

返回 HTML 页面，显示投票结果：

```html
<h2>{{ question.question_text }}</h2>
<ul>
  <li>选项 1 -- 15 votes</li>
  <li>选项 2 -- 8 votes</li>
  <li>选项 3 -- 23 votes</li>
</ul>
<a href="/polls/{{ question.id }}/">Vote again?</a>
```

**404 未找到**

问题不存在。

### 示例

**cURL**
```bash
curl -X GET "http://127.0.0.1:8000/polls/1/results/"
```

**Python**
```python
response = requests.get('http://127.0.0.1:8000/polls/1/results/')
print(response.text)
```

---

## POST /polls/<id>/vote/

### 描述

提交投票，将选中选项的票数加 1。成功后重定向到结果页。

### 参数

| 名称 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | integer | 是 | 问题 ID (URL 路径参数) |
| choice | integer | 是 | 选项 ID (表单参数) |

### 请求体

```
Content-Type: application/x-www-form-urlencoded

choice=1
```

### 响应

**302 重定向**

投票成功，重定向到结果页：

```
Location: /polls/<id>/results/
```

**200 成功（错误）**

未选择选项，返回详情页并显示错误：

```html
<p class="error">You didn't select a choice.</p>
```

**404 未找到**

问题不存在。

### 示例

**cURL**
```bash
curl -X POST "http://127.0.0.1:8000/polls/1/vote/" \
  -d "choice=1" \
  -L  # 跟随重定向
```

**Python**
```python
response = requests.post(
    'http://127.0.0.1:8000/polls/1/vote/',
    data={'choice': 1},
    allow_redirects=True
)
print(response.url)  # 重定向后的 URL
```

**JavaScript (Fetch)**
```javascript
const formData = new FormData();
formData.append('choice', '1');

const response = await fetch('/polls/1/vote/', {
  method: 'POST',
  body: formData
});

if (response.redirected) {
  window.location.href = response.url;
}
```

---

## 错误处理

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 302 | 重定向（POST 成功后） |
| 404 | 资源未找到（问题不存在或未发布） |

---

## 数据模型

### Question

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 主键 |
| question_text | string(200) | 问题文本 |
| pub_date | datetime | 发布时间 |

### Choice

| 字段 | 类型 | 说明 |
|------|------|------|
| id | integer | 主键 |
| question | ForeignKey | 关联问题 |
| choice_text | string(200) | 选项文本 |
| votes | integer | 票数，默认 0 |

---

## 注意事项

1. **时间过滤**: 所有公开视图都会过滤掉 `pub_date` 晚于当前时间的问题
2. **CSRF 保护**: POST 请求需要包含 CSRF token（Django 默认开启）
3. **原子操作**: 投票计数使用 `F()` 表达式实现原子递增，避免并发问题
