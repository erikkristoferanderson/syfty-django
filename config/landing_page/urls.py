from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),
    path('plans', views.plans_view, name='plans'),
    path('about', views.about_view, name='about'),
    path('terms_of_use', views.terms_view, name='terms_of_use'),
    path('privacy_policy', views.privacy_policy_view, name='privacy_policy')
    # ...other URL patterns...
]
