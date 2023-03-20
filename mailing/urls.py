from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import *

app_name = MailingConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing_settings_list/', MailingSettingsListView.as_view(), name='mailing_settings_list'),
    path('mailing_settings_create/', MailingSettingsCreateView.as_view(), name='mailing_settings_create'),
    path('mailing_settings_update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailing_settings_update'),
    path('mailing_settings_detail/<int:pk>/', MailingSettingsDetailView.as_view(), name='mailing_settings_detail'),
    path('mailing_settings_delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_settings_delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailing_attempt_list/', MailingAttemptListView.as_view(), name='mailing_attempt_list'),
    path('mailing_attempt_detail/<int:pk>/', MailingAttemptDetailView.as_view(), name='mailing_attempt_detail'),
    path('mailing_attempt_delete/<int:pk>/', MailingAttemptDeleteView.as_view(), name='mailing_attempt_delete'),

    path('change_status_settings/<int:pk>/', change_status_settings, name='change_status_settings'),

]