# Generated by Django 3.2.9 on 2022-03-22 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_auto_20220322_0938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdata',
            name='response_message',
        ),
    ]
