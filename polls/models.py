import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    # @装饰器：对应 admin 后台页显示 UI、以及排序
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    # 判断问题是否在一天内发布
    def was_published_recently(self):
        # bug: 如果是未来的时间也会判断是在最近发布，比如30天后的时间
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # fixed:
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
