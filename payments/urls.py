# payments/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('payment', views.HomePageView.as_view(), name='payment'),
    path('payment/config/', views.stripe_config),
    path('payment/create-checkout-session/',
         views.create_checkout_session),
    path('payment/success/', views.SuccessView.as_view()),
    path('payment/cancelled/', views.CancelledView.as_view()),
    path('payment/webhook/', views.stripe_webhook),
]
