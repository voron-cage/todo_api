# Generated by Django 4.2.3 on 2023-07-27 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TODOList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('order', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TODO',
                'verbose_name_plural': 'TODO',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='TODOAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=2048, verbose_name='Действие')),
                ('is_done', models.BooleanField(default=False, verbose_name='Выполнено')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('expire_time', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_action', to='todo.todolist')),
            ],
            options={
                'verbose_name': 'TODO Action',
                'verbose_name_plural': 'TODO Action',
                'ordering': ['order'],
            },
        ),
    ]
