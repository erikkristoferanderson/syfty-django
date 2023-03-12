from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Syft


@login_required
def dashboard_view(request):
    current_user = request.user
    syfts = Syft.objects.filter(
        owner=current_user).all()
    context = {'user': request.user,
               'syfts': syfts}
    return render(request, 'dashboard.html', context)
