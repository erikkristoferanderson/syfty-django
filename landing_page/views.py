from django.shortcuts import render
import logging
# Create your views here.


def landing_page_view(request):
    logger = logging.getLogger('testlogger')
    logger.info('hello this is a simple log message')
    return render(request, 'landing_page.html')


def plans_view(request):
    return render(request, 'plans.html')


def about_view(request):
    return render(request, 'about_syfty.html')


def terms_view(request):
    return render(request, "terms_of_use.html")


def privacy_policy_view(request):
    return render(request, "privacy_policy.html")
