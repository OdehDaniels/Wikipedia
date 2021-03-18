from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit")
]
