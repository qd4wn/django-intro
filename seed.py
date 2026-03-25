# seed.py
# 用于数据库中记录的批量生成程序（清除旧数据）

import os
import django
import datetime
import random

# 初始化 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Question, Choice
from django.utils import timezone

# 清楚旧的数据
Question.objects.all().delete()

questions_text = [
    "What is your favorite programming language?",
    "Which code editor do you use most often?",
    "What is your primary operating system?",
    "Do you prefer frontend or backend development?",
    "How many hours do you code daily?",
    "Which database do you use most?",
    "What is your favorite web framework?",
    "Which version control system do you use?",
    "Do you prefer tabs or spaces?",
    "What is your favorite programming paradigm?"
]

choices_pool = [
    ["Python", "C++", "Java", "Go"],
    ["VS Code", "Vim", "PyCharm", "Neovim"],
    ["Linux", "Windows", "macOS"],
    ["Frontend", "Backend", "Fullstack"],
    ["<1 hour", "1-3 hours", "3-6 hours", "6+ hours"],
    ["MySQL", "PostgreSQL", "SQLite", "MongoDB"],
    ["Django", "Flask", "Spring", "Express"],
    ["Git", "SVN", "Mercurial"],
    ["Tabs", "Spaces"],
    ["OOP", "Functional", "Procedural"]
]

# 迭代生成对应的数据记录填入表
for i in range(len(questions_text)):
    q = Question.objects.create(
        question_text=questions_text[i],
        pub_date=timezone.now() - datetime.timedelta(days=random.randint(0, 5))
    )

    for choice_text in choices_pool[i]:
        Choice.objects.create(
            question=q,
            choice_text=choice_text,
            votes=random.randint(0, 100)
        )

print(f"Data generation completed! Questions count: {Question.objects.count()}")