from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker
fake = Faker()
class Command(BaseCommand):
    def answers(self, cnt):
        author_ids = list(Author.objects.values_list('id', flat=True))
        questions_ids = list(
            Question.objects.values_list('id', flat=True))
        answers = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            answers.append(Answer(
                text=' '.join(fake.sentences(fake.random_int(min=5, max=10))),
                author_id=choice(author_ids),
                question_id=question_id,
                date=Question.objects.get(id=question_id).date
            ))
        Answer.objects.bulk_create(answers)
    def handle(self, *args, **options):
        size = [20, 10001, 100001, 1000001]
        self.answers(size[2])
        