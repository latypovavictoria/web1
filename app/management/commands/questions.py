from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker
fake = Faker()
class Command(BaseCommand):
    def questions(self, cnt):
        author_ids = list(Author.objects.values_list('id', flat=True))
        tags_ids = list(Tag.objects.values_list('id', flat=True))
        questions = []
        for i in range(cnt):
            questions.append(Question(
                author_id=choice(author_ids),
                text=' '.join(fake.sentences(fake.random_int(min=5, max=15))),
                title=fake.sentence()[:-1] + '?',
                date=fake.date_between(start_date='-1y', end_date='today'),
            ))
        Question.objects.bulk_create(questions)
        for q in Question.objects.all():
            tag1 = Tag.objects.get(id=choice(tags_ids))
            tag2 = Tag.objects.get(id=choice(tags_ids))
            if tag1 != tag2:
                q.tags.add(tag1, tag2)
            else:
                q.tags.add(tag1)
    def handle(self, *args, **options):
        size = [10001, 100001, 1000001]
        self.questions(size[1])
