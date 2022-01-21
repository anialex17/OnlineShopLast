# Generated by Django 3.2.9 on 2022-01-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220120_1148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='buying_type',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('TYPE_PAYMENT_CASH', 'Կանխիկ'), ('TYPE_PAYMENT_NON_CASH', 'Անկանխիկ')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('STATUS_NEW', 'Նոր պատվեր'), ('STATUS_READY', 'Պատվերը պատրաստ է'), ('STATUS_COMPLETED', 'Պատվերը առաքված է')], default='STATUS_NEW', max_length=100),
        ),
    ]
