from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    def fill_question_likes(self, cnt):
        LIKES = ['1', '-1']
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Author.objects.values_list(
                'id', flat=True
            )
        )
        question_likes = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            like = choice(LIKES)
            question_likes.append(QuestionLike(
                like=like,
                author_id=choice(author_ids),
                question_id=question_id
            ))
            Question.objects.filter(id=question_id).update(rating=F('rating') + like)

        QuestionLike.objects.bulk_create(question_likes)


    def fill_answer_likes(self, cnt):
        LIKES = ['5', '-7']
        answers_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Author.objects.values_list(
                'id', flat=True
            )
        )
        answers_likes = []
        for i in range(cnt):
            answers_likes.append(AnswerLike(
                like=choice(LIKES),
                author_id=choice(author_ids),
                answer_id=choice(answers_ids)
            ))
        AnswerLike.objects.bulk_create(answers_likes)

    
    def handle(self, *args, **options):
        size = [10001, 100001, 1000001, 900000]
        self.fill_question_likes(size[2])
        self.fill_answer_likes(size[2])
