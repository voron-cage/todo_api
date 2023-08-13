from django.db import models
from django.contrib.auth.models import User


class TODOList(models.Model):
    title = models.CharField('Наименование', max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todolist')
    slug = models.SlugField('slug', max_length=255, unique=True, db_index=True)
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = 'TODO'
        ordering = ['order']


class TODOAction(models.Model):
    todo = models.ForeignKey(TODOList, on_delete=models.CASCADE, related_name='todo_action')
    title = models.CharField('Действие', max_length=2048)
    is_done = models.BooleanField('Выполнено', default=False)
    slug = models.SlugField('slug', max_length=255, db_index=True)
    expire_time = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('todo', 'slug')
        verbose_name = verbose_name_plural = 'TODO Action'
        ordering = ['order']
