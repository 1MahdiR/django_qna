from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from .models import Question, Answer
from .forms import AnswerForm, QuestionForm, LoginForm, RegistrationForm

def index(req):

    question_list = Question.objects.order_by('-question_date')

    return render(req, 'main/index.html', { 'question_list':question_list })

def question(req, q_id):

    question = get_object_or_404(Question, id=q_id)

    if req.method == "POST" and req.user.is_authenticated:
        form = req.POST
        if form.get('answer_like'):
            temp = form['answer_like']
            answer = get_object_or_404(Answer, id=int(temp))
            if req.user in answer.answer_likes.all():
                answer.answer_likes.remove(req.user)
            else:
                answer.answer_likes.add(req.user)
            answer.save()
            form = AnswerForm(data=req.POST)

        elif form.get('answer_dislike'):
            temp = form['answer_dislike']
            answer = get_object_or_404(Answer, id=int(temp))
            if req.user in answer.answer_dislikes.all():
                answer.answer_dislikes.remove(req.user)
            else:
                answer.answer_dislikes.add(req.user)
            answer.save()
            form = AnswerForm(data=req.POST)

        elif form.get('question_like'):
            if req.user in question.question_likes.all():
                question.question_likes.remove(req.user)
            else:
                question.question_likes.add(req.user)
            question.save()
            form = AnswerForm(data=req.POST)

        elif form.get('question_dislike'):
            if req.user in question.question_dislikes.all():
                question.question_dislikes.remove(req.user)
            else:
                question.question_dislikes.add(req.user)
            question.save()
            form = AnswerForm(data=req.POST)

        elif form.get('question_delete'):
            if question.question_user == req.user:
            	question.delete()
            	return HttpResponseRedirect(reverse('main:index'))

        elif form.get('answer_delete'):
            temp = form['answer_delete']
            answer = get_object_or_404(Answer, id=int(temp))
            print(answer.answer_user == req.user)
            print(form)
            if answer.answer_user == req.user:
            	answer.delete()
            	return HttpResponseRedirect(reverse('main:question', kwargs={'q_id':question.id}))

        else:
            form = AnswerForm(data=req.POST)
            if form.is_valid():
                new_ans = form.save(commit=False)
                new_ans.answer_question = question
                new_ans.answer_user = req.user
                new_ans.save()

    else:
        form = AnswerForm()

    answer_list = question.question_answer.order_by('-answer_likes')
    return render(req, 'main/question.html', { 'question':question, 'answer_list':answer_list, 'form':form })

@login_required
def question_submit(req):

    if req.method == "POST":
        form = QuestionForm(req.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.question_user = req.user
            question.save()
            return HttpResponseRedirect(reverse('main:question', kwargs={'q_id':question.id}))
    else:
        form = QuestionForm()

    return render(req, 'main/submit.html', { 'form':form })

def register(req):
	if req.method == "POST":
		form = RegistrationForm(req.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data['password'])
			new_user.save()
			login(req, new_user)
			return HttpResponseRedirect(reverse('main:index'))
	else:
		form = RegistrationForm()
	return render(req, 'main/regist.html', { 'form':form })

def login_view(req):

	if req.method == "POST":
		form = LoginForm(req.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(req, username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					login(req, user)
					return HttpResponseRedirect(reverse('main:index'))
				else:
					return HttpResponse("Disabled account!")
			else:
				return HttpResponse("Invalid login!")
	else:
		form = LoginForm()

	return render(req, 'main/login.html', { 'form':form })

def logout_view(req):
	logout(req)
	return HttpResponseRedirect(reverse('main:index'))
