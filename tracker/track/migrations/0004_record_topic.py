# Generated by Django 3.1.5 on 2021-07-01 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_delete_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='topic',
            field=models.CharField(default='blank', max_length=100),
        ),
    ]