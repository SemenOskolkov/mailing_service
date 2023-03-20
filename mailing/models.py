from django.db import models


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    comment = models.TextField(verbose_name='Комментарий')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'


class MailingSettings(models.Model):
    PERIOD_DAY = 'day'
    PERIOD_WEEK = 'week'
    PERIOD_MONTH = 'month'

    PERIODS = (
        (PERIOD_DAY, 'день'),
        (PERIOD_WEEK, 'неделя'),
        (PERIOD_MONTH, 'месяц')
    )

    STATUS_COMPLETED = 'completed'
    STATUS_CREATED = 'created'
    STATUS_LAUNCHED = 'launched'

    STATUSES = (
        (STATUS_COMPLETED, 'завершена'),
        (STATUS_CREATED, 'создана'),
        (STATUS_LAUNCHED, 'запущена')
    )

    mailing_time = models.TimeField(verbose_name='время рассылки')
    period = models.CharField(max_length=15, choices=PERIODS, default=PERIOD_DAY, verbose_name='периодичность')
    mailing_status = models.CharField(max_length=15, choices=STATUSES, default=STATUS_CREATED, verbose_name='статус рассылки')

    message = models.ForeignKey('mailing.Message', on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField('mailing.Client', verbose_name='Клиенты')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'настройка'
        verbose_name_plural = 'настройки'

        permissions = [
            ('can_disable_mailings', 'Can disable mailings'),
        ]

    def __str__(self):
        return f'{self.mailing_time} {self.period} {self.mailing_status}'


class Message(models.Model):
    letter_subject = models.CharField(max_length=200, verbose_name='Тема письма')
    letter_body = models.TextField(verbose_name='Тело письма')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return f'{self.letter_subject} {self.letter_body}'


class MailingAttempt(models.Model):
    STATUS_DELIVERED = 'delivered'
    STATUS_NOT_DELIVERED = 'not_delivered'

    STATUSES = (
        ('delivered', 'доставлено'),
        ('not_delivered', 'не доставлено'),
    )

    last_datetime = models.DateTimeField(verbose_name='Дата и время рассылки')
    status = models.CharField(max_length=25, choices=STATUSES, default=STATUS_NOT_DELIVERED, verbose_name='статус')
    server_response = models.CharField(blank=True, max_length=150, verbose_name='ответ сервера')

    settings = models.ForeignKey('mailing.MailingSettings', on_delete=models.CASCADE, verbose_name='Настройки')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'

    def __str__(self):
        return f'{self.last_datetime} {self.status} {self.server_response}'