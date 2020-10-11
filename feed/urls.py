from django.urls import path
from . import views


app_name='feed'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/update', views.update, name='update'),
    path('<int:article_pk>/delete', views.delete, name='delete'),
    path('<int:article_pk>/comments/', views.comments, name='comments'),
    path('<int:article_pk>/like/', views.like, name='like'),
]


from django.conf.urls.static import static

from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)