# Generated by Django 3.2.9 on 2022-03-25 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmessage',
            name='file',
        ),
    ]
