from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker
fake = Faker()
class Command(BaseCommand):
    pic = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
    def authors(self, cnt):
        usernames = set()
        authors = []
        for i in range(cnt):
            username = fake.simple_profile().get('username')
            while username in usernames:
                username = fake.simple_profile().get('username')
            user = User.objects.create(username=username, password=fake.password(length=9, special_chars=True))
            authors.append(Author(user_id=user.id,avatar=choice(self.pic)))
            usernames.add(username)
        Author.objects.bulk_create(authors)
    def handle(self, *args, **options):
        size = [10001, 11000, 100001, 1000001, 900000, 1200000]
        self.authors(size[0])