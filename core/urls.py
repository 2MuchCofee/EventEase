from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('create-event/', views.create_event, name='create_event'),
    path('join-event/', views.join_event, name='join_event'),
    path('event/<str:event_id>/', views.event_dashboard, name='event_dashboard'),
    path('event/<str:event_id>/announcements/', views.announcement_channel, name='announcement_channel'),
    path('event/<str:event_id>/public/', views.public_channel, name='public_channel'),
    path('event/<str:event_id>/tickets/', views.ticket_channel, name='ticket_channel'),
    path('event/<str:event_id>/walkie/', views.walkie_talkie, name='walkie_talkie'),
    path('event/<str:event_id>/check-in/', views.check_in, name='check_in'),
    path('event/<str:event_id>/qr-checkin/', views.qr_check_in, name='qr_check_in'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
]