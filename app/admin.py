from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from app.models import Author
from app.models import Question
from app.models import Answer
from app.models import Tag
from app.models import QuestionLike
from app.models import AnswerLike
admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(QuestionLike)
admin.site.register(AnswerLike)