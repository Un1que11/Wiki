from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("entry/add", views.add, name="add"),
    path("entry/<str:title>/update", views.update, name="update"),
    path("entry/random", views.random_entry, name="random"),
]
