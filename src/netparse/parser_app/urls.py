from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Main page for the app
    path("parse/", views.parse_command, name="parse_command"),  # Endpoint for parsing
]
