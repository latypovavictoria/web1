from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from random import shuffle
import time
from django.db.models import Sum, Count
class QuestionManager(models.Manager):
    def popular(self):
        return self.prefetch_related('likes', 'author').order_by('-rating')
    def tagq(self, str):
        return self.prefetch_related('likes', 'author').filter(tags__name=str)
class AnswerManager(models.Manager):
    def all_ans(self, pk):
        return self.prefetch_related('likes', 'author').filter(question__id=pk).annotate(like_sum=Sum('likes__like'))
class TagManager(models.Manager):
    def popular(self):
        return self.annotate(count=Count('questions')).order_by('-count')
class AuthorManager(models.Manager):
    def popular(self):
        return self.annotate(count=Count('answers')).order_by('-count')
class Author(models.Model):
    avatar=models.ImageField(upload_to='upload/', default='unnamed.jpg')
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    objects = AuthorManager()
    def __str__(self):
        return self.user.__str__()

class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField(default=datetime.now)
    rating = models.IntegerField(default=0, db_index=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)
    objects = QuestionManager()
    def __str__(self):
        return self.title
class Answer(models.Model):
    question=models.ForeignKey('Question',related_name='answers', on_delete=models.CASCADE)
    text=models.TextField()
    date=models.DateField(default=datetime.now)
    like=models.IntegerField(default=0,null=False)
    checked = models.BooleanField(default=False)
    author=models.ForeignKey('Author',related_name='answers', on_delete=models.CASCADE)
    objects = AnswerManager()
    def __str__(self):
        return self.text

    def __str__(self):
        return self.text

class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    objects = TagManager()
    def __str__(self):
        return self.name

class QuestionLike(models.Model):
    LIKES = (('LIKE', '1'), ('DISLIKE', '-1'))
    like = models.IntegerField(choices=LIKES, default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.like) + ' ' + self.question.__str__()


class AnswerLike(models.Model):
    LIKES = (('LIKE', '1'), ('DISLIKE', '-1'))
    like = models.IntegerField(choices=LIKES, default=0)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.like) + ' ' + self.answer.__str__()

