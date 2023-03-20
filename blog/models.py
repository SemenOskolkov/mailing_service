from django.db import models

from base.models import NULLABLE


class Blog(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUSES = (
        (STATUS_ACTIVE, 'опубликован'),
        (STATUS_INACTIVE, 'не опубликован')
    )

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog_record/', **NULLABLE, verbose_name='Изображение')
    number_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    date_of_creation = models.DateField(auto_now=False, auto_now_add=True, verbose_name='Дата создания')
    sign_publication = models.CharField(choices=STATUSES, default=STATUS_INACTIVE, max_length=10,
                                        verbose_name='Признак публикации')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return f'{self.id} {self.title}'
