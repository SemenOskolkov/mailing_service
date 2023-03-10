from datetime import datetime, timedelta

from django.core.mail import send_mail
import django.conf
import pytz

from mailing.models import MailingSettings, MailingAttempt


def auto_mailing():
    for active_status in MailingSettings.objects.all():
        if active_status.status == MailingSettings.STATUS_LAUNCHED:
            obj = MailingAttempt.objects.filter(settings_pk=active_status.id).last()
            if obj is None:
                mailing_time = active_status.mailing_time.replace(second=0, microsecond=0)
                time_now = datetime.now().time().replace(second=0, microsecond=0)
                if mailing_time == time_now:
                    send_message(active_status)
            else:
                period = active_status.period
                send_time = obj.last_datetime
                if period == MailingSettings.PERIOD_DAY:
                    send_time += timedelta(days=1)
                elif period == MailingSettings.PERIOD_WEEK:
                    send_time += timedelta(days=7)
                elif period == MailingSettings.PERIOD_MONTH:
                    send_time += timedelta(days=30)
                send_time = send_time.replace(second=0, microsecond=0)
                time_now = datetime.now().replace(second=0, microsecond=0)
                if send_time == time_now:
                    send_message(active_status)


def send_message(active_status):
    status_list = []
    mail_list = active_status.clients.all()
    for item in mail_list:
        try:
            send_mail(
                subject=active_status.message.letter_subject,
                message=active_status.message.letter_body,
                from_email=django.conf.settings.EMAIL_HOST_USER,
                recipient_list=[item.email],
                fail_silently=False
            )
        except:
            server_response = {
                'sending_time': datetime.datetime.now().astimezone(pytz.timezone(django.conf.settings.TIME_ZONE)),
                'status': MailingAttempt.STATUS_NOT_DELIVERED,
                'server_response': item.email,
                'settings_pk': MailingSettings.objects.get(pk=active_status.id), }
            status_list.append(MailingAttempt(**server_response))
        else:
            server_response = {
                'sending_time': datetime.datetime.now().astimezone(pytz.timezone(django.conf.settings.TIME_ZONE)),
                'status': MailingAttempt.STATUS_DELIVERED,
                'server_response': item.email,
                'settings_pk': MailingSettings.objects.get(pk=active_status.id), }
            status_list.append(MailingAttempt(**server_response))
    MailingAttempt.objects.bulk_create(status_list)
