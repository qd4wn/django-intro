from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404

from .models import Question

def index(request):
    # return HttpResponse("Hello, world. You are at the polls index.")

    # -pub_date 按发布时间降序
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = "<br>".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    
    # template = loader.get_template("polls/index.html")
    # 将模板对应变量映射为 Python 对象
    context = {"latest_question_list": latest_question_list}
    # return HttpResponse(template.render(context, request))
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    # return HttpResponse(f"You're looking at question {question_id}.")

    try:
        question = Question.objects.get(pk=question_id)
        # question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist in db.")
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")