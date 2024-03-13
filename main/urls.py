from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("blog1/", views.blog, name="blog"),
    path("profile/", views.account, name="profile"),
]