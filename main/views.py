from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from .models import Question, Answer
from .forms import AnswerForm, QuestionForm

# Create your views here.
def index(req):

    question_list = Question.objects.order_by('-question_date')

    return render(req, 'main/index.html', { 'question_list':question_list })

def question(req, q_id):

    question = get_object_or_404(Question, id=q_id)

    if req.method == "POST":
        print(req.POST)
        form = req.POST
        if form.get('answer'):
            temp = form['answer']
            answer = get_object_or_404(Answer, id=int(temp))
            answer.answer_likes += 1
            answer.save()
            form = AnswerForm(data=req.POST)

        elif form.get('question'):
            question.question_likes += 1
            question.save()
            form = AnswerForm(data=req.POST)

        else:
            form = AnswerForm(data=req.POST)
            if form.is_valid():
                new_ans = form.save(commit=False)
                new_ans.answer_question = question
                new_ans.save()

    else:
        form = AnswerForm()

    answer_list = question.question_answer.order_by('-answer_likes')
    return render(req, 'main/question.html', { 'question':question, 'answer_list':answer_list, 'form':form })

def question_submit(req):
    
    if req.method == "POST":
        form = QuestionForm(req.POST)
        if form.is_valid():
            question = form.save()
            return HttpResponseRedirect(reverse('main:question', kwargs={'q_id':question.id}))
    else:
        form = QuestionForm()

    return render(req, 'main/submit.html', { 'form':form })

