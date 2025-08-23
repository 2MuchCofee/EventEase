from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-event/', views.create_event, name='create_event'),
    path('join-event/', views.join_event, name='join_event'),
    path('event/<str:event_id>/', views.event_dashboard, name='event_dashboard'),
    path('event/<str:event_id>/announcements/', views.announcement_channel, name='announcement_channel'),
    path('event/<str:event_id>/public/', views.public_channel, name='public_channel'),
    path('event/<str:event_id>/tickets/', views.ticket_channel, name='ticket_channel'),
]