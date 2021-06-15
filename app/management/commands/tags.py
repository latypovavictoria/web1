from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker
fake = Faker()
class Command(BaseCommand):
    def tags(self, cnt):
        tags = set()
        tags_list = []
        for i in range(cnt):
            tag = fake.word()
            while tag in tags:
                tag += '_' + fake.word()
                if len(tag) > 20:
                    tag = fake.pystr(min_chars=2, max_chars=15)
            tags_list.append(Tag(
                name=tag,))
            tags.add(tag)
        Tag.objects.bulk_create(tags_list)
    def handle(self, *args, **options):
        size = [10001, 100001, 1000001]
        self.tags(size[1])

