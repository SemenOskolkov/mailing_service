import os
from django.conf import settings
from django.core.management import BaseCommand
from blog.models import Blog
from django.core.files import File


class Command(BaseCommand):
    def handle(self, *args, **options):
        blog_data = [
            {'title': 'Копирайтинг',
             'content': 'Полезная информация про копирайтинг',
             'preview': 'media/kopirayting.jpeg'},
            {'title': 'Как правильно писать письма',
             'content': 'Полезная информация о том как правильно писать письма',
             'preview': 'media/letters.jpeg'},
            {'title': 'Как помогает рассылка писем',
             'content': 'Полезная информация о том как помогает рассылка писем',
             'preview': 'media/mailing.png'},
            {'title': 'Грамотность важна!',
             'content': 'Полезная информация про грамотность',
             'preview': 'media/full_size_1635576888-8afbe5fe7471980ff999fff29828a375.jpg'}
        ]

        blog_list = []
        for item in blog_data:
            preview_path = item.pop('preview')  # Удаление 'preview' из словаря
            blog_obj = Blog(**item)
            
            # Добавление изображения
            if preview_path:
                image_path = os.path.join(settings.MEDIA_ROOT, preview_path)
                with open(image_path, 'rb') as f:
                    django_file = File(f)
                    blog_obj.preview.save(os.path.basename(image_path), django_file, save=True)
            
            blog_list.append(blog_obj)

        Blog.objects.bulk_create(blog_list)
