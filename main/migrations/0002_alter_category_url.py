# Generated by Django 3.2.9 on 2022-01-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.SlugField(unique=True),
        ),
    ]
