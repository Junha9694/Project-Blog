from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.blog_list, name="blog_list"),
    path("<int:pk>/", views.blog_detail, name="blog_detail"),
    path("create/", views.blog_create, name="blog_create"),
    path("<int:pk>/update/", views.blog_update, name="blog_update"),
    path("<int:pk>/delete/", views.blog_delete, name="blog_delete"),
    path("tag/<str:tag>/", views.blog_tag, name="blog_tag"),
    # comment 삭제 url 추가
    path("<int:pk>/comment_delete/", views.blog_comment_delete, name="blog_comment_delete"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)