from django.core.management import BaseCommand
from blog.models import Blog


class Command(BaseCommand):
    def handle(self, *args, **options):
        blog = [
            {'title': 'Копирайтинг',
             'content': 'Полезная информация про копирайтинг',
             'preview': ''},
            {'title': 'Как правильно писать письма',
             'content': 'Полезная информация о том как правильно писать письма',
             'preview': ''},
            {'title': 'Как помогает рассылка писем',
             'content': 'Полезная информация о том как помогает рассылка писем',
             'preview': ''},
            {'title': 'Грамотность важна!',
             'content': 'Полезная информация про грамотность',
             'preview': ''}
        ]

        blog_list = []
        for item in blog:
            blog_list.append(Blog(**item))

        Blog.objects.bulk_create(blog_list)
