# Generated by Django 2.1.15 on 2021-06-11 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210611_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='rating',
            new_name='like',
        ),
    ]
