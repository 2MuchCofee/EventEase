from django.urls import path
from .views import home, create_event, join_event, event_dashboard, announcement_channel, public_channel, ticket_channel

urlpatterns = [
    path('', home, name='home'),
    path('create_event/', create_event, name='create_event'),
    path('join_event/', join_event, name='join_event'),
    path('event_dashboard/<str:event_id>/', event_dashboard, name='event_dashboard'),
    path('event_dashboard/<str:event_id>/announcement/', announcement_channel, name='announcement_channel'),
    path('event_dashboard/<str:event_id>/public/', public_channel, name='public_channel'),
    path('event_dashboard/<str:event_id>/tickets/', ticket_channel, name='ticket_channel'),
    path('event_dashboard/<str:event_id>/walkie_talkie/', walkie_talkie, name='walkie_talkie'),
]