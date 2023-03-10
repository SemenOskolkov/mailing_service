# Generated by Django 4.1.7 on 2023-03-05 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('first_name', models.CharField(max_length=150, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter_subject', models.CharField(max_length=200, verbose_name='Тема письма')),
                ('letter_body', models.TextField(verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(verbose_name='время рассылки')),
                ('period', models.CharField(choices=[('day', 'день'), ('week', 'неделя'), ('month', 'месяц')], default='day', max_length=15, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('completed', 'завершена'), ('created', 'создана'), ('launched', 'запущена')], default='created', max_length=15, verbose_name='статус рассылки')),
                ('clients', models.ManyToManyField(to='mailing.client', verbose_name='Клиенты')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'настройка',
                'verbose_name_plural': 'настройки',
            },
        ),
        migrations.CreateModel(
            name='MailingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_datetime', models.DateTimeField(verbose_name='Дата и время рассылки')),
                ('status', models.CharField(choices=[('delivered', 'доставлено'), ('not_delivered', 'не доставлено')], default='not_delivered', max_length=25, verbose_name='статус')),
                ('server_response', models.CharField(blank=True, max_length=150, verbose_name='ответ сервера')),
                ('settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailingsettings', verbose_name='Настройки')),
            ],
            options={
                'verbose_name': 'попытка рассылки',
                'verbose_name_plural': 'попытки рассылки',
            },
        ),
    ]
