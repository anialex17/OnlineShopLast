# Generated by Django 3.2.9 on 2022-03-02 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_productitem_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productitem',
            name='comment',
        ),
    ]
