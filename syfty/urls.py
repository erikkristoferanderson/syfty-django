from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:search_id>/', views.detail, name='detail'),
    path('create', views.create, name='create'),
    path('<int:search_id>/update', views.update, name='update'),
    path('<int:search_id>/delete', views.delete, name='delete'),
    path('signup/', views.signup, name='signup'),

]
