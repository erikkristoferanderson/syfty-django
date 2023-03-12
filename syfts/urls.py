from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('syft/<int:syft_id>/', views.syft_detail_view, name='syft'),
    path('error', views.error_view, name='error'),
    path('create', views.create, name='create'),
    path('syft/<int:syft_id>/update', views.update, name='update'),
    path('syft/<int:syft_id>/delete', views.delete, name='delete'),
]
