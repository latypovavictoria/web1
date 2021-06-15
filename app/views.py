from django.shortcuts import render
from django.db.models import Sum, Count
from django.db import models
from django.http import JsonResponse
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.views.decorators.http import require_POST
from django import conf
from django.contrib.auth.models import User
import time
from django.db.models.functions import Trunc
from django.db.models import DateField
import jwt
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from .models import *
from app.forms import LoginForm, QuestionForm, RegisterForm, SettingsForm
from random import shuffle
from django.db.models import F
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib import auth
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from app.models import QuestionManager, AuthorManager, AnswerManager, TagManager
authors = Author.objects.popular()[:5]
popular_tags = Tag.objects.popular()[:5]

def content_processor(request):
    return {
        'popular_tags': popular_tags,
        'authors': authors
    }
def index(request):
    question = Question.objects.order_by('-date')
    paginator = Paginator(question, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_number': page_number,'page_obj': page_obj})
def tag_question(request, str):
    question = Question.objects.tagq(str)
    paginator = Paginator(question, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tag_question.html', {'page_number': page_number,'page_obj': page_obj, 'type': 'tagq'})   
def one_question(request, pk):
    question = Question.objects.get(id=pk)
    answers_list = Answer.objects.all_ans(pk)
    paginator = Paginator(answers_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'question.html', {'page_number': page_number,'page_obj': page_obj, 'question': question})
def hot(request):
    question=Question.objects.order_by('-rating')
    paginator = Paginator(question, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hot.html', {'page_number': page_number,'page_obj': page_obj})
@login_required
def answer(request):
    id = request.POST.get('pk')
    answer = Answer.objects.create(author_id=request.user.author.id, question_id=id, date=date.today(), text=request.POST.get('text'))
    answer.save()
    return redirect(reverse('question', kwargs={'pk': id}))
@login_required
def ask(request):
    if request.method == 'GET':
        form = QuestionForm()
    else:
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.author
            question.date = date.today()
            question.save()
            for elem in form.cleaned_data['tags'].split(', '):
                tag = Tag.objects.filter(name=elem)
                if elem and not tag:
                    tag = Tag(name=elem)
                    tag.save()
                else:
                    tag = tag[0]
                question.tags.add(tag.id)
            question.save()
            return redirect(reverse('question', kwargs={'pk': question.id}))
    return render(request, 'ask.html', {'form': form })
@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm(initial={'username': request.user.username, 'email':  request.user.email,
                                     'avatar': request.user.author.avatar})
    else:
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.author.avatar = form.cleaned_data['avatar']
            user.author.save()
            user.save()
            form = SettingsForm(initial={'username': request.user.username, 'email': request.user.email,'avatar': request.user.author.avatar})
    return render(request, 'settings.html', {'form': form})
def login(request):
    form=LoginForm(data=request.POST)
    if form.is_valid():
        user=auth.authenticate(request, **form.cleaned_data)
        if user is not None:
            auth.login(request, user)
            request.session['Hello']='world'
            return redirect(reverse('index')) 
    return render(request, 'login.html',{'form':form})
def logout(request):
    print(request.session.pop('hello', 'nothing'))
    auth.logout(request)
    return redirect(reverse('index'))
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'], form.cleaned_data['password1'])
            authoreq = Author(avatar=form.cleaned_data['avatar'], user_id=user.id)
            authoreq.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            auth.login(request, user)
            return redirect('index')
    return render(request, 'register.html', {'form': form})
def choose(str):
    if str == 'like':
        return 1
    elif str == 'dislike':
        return -1

@login_required
@require_POST
@csrf_exempt
def qvote(request):
    data = request.POST
    inc = choose(data['action'])
    rating = 0
    error = ""

    question = Question.objects.get(id=data['qid'])
    like = QuestionLike.objects.filter(question_id=data['qid'], author_id=request.user.id)
    if question and not like:
        rating = question.rating + inc
        question.rating = F('rating') + inc
        question.save()
        QuestionLike.objects.create(question_id=question.id, author_id=request.user.author.id, like=str(inc))
    else:
        error = "None"

    return JsonResponse({'rating': rating})

@login_required
@require_POST
@csrf_exempt
def avote(request):
    data = request.POST
    inc = choose(data['action'])
    error = ""

    answer = Answer.objects.get(id=data['aid'])
    if answer and not AnswerLike.objects.filter(answer_id=data['aid'], author_id=request.user.id):
        AnswerLike.objects.create(answer_id=data['aid'], author_id=request.user.author.id,like=str(inc))
    else:
        error = "None"
    return JsonResponse({'rating': inc})

@login_required
@require_POST
@csrf_exempt
def check(request):
    data = request.POST
    error = ""
    answer = Answer.objects.get(id=data['aid'])
    value = True
    if answer and answer.question.author.id == request.user.author.id:
        if answer.checked:
            answer.checked = False
            answer.save()
            value = False
        else:
            answer.checked = True
            answer.save()
    else:
        error = "None"
    return JsonResponse({'value': value})

 
