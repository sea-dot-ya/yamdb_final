# Generated by Django 3.2 on 2023-01-30 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Польщователь'), ('moderator', 'Модератор'), ('admin', 'Админ')], max_length=10),
        ),
    ]