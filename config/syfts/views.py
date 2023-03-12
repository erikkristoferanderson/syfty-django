
from django.contrib.auth.decorators import login_required
from .models import Syft
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime


@login_required
def dashboard_view(request):
    current_user = request.user
    syfts = Syft.objects.filter(
        owner=current_user).all()
    for syft in syfts:
        syft.date_created_date_only = syft.date_created.date()

    context = {'user': request.user,
               'syfts': syfts, }
    return render(request, 'dashboard.html', context)


@login_required
def syft_detail_view(request, syft_id):
    try:
        syft = Syft.objects.filter(owner=request.user).get(id=syft_id)
    except Syft.DoesNotExist as e:
        return redirect("error")
    return render(request, 'syft_detail.html', {'syft': syft})


def error_view(request):
    return render(request, 'error.html')


@login_required
def create(request):
    if request.method == 'POST':
        syft = Syft(owner=request.user,
                    subreddit=request.POST['subreddit'],
                    search_term=request.POST['search_term'])
        syft.save()
        return redirect("dashboard")
    else:
        return render(request, 'create_syft.html')


@login_required
def update(request, syft_id):
    if request.method == 'POST':
        syft = get_object_or_404(Syft, pk=syft_id)
        syft.subreddit = request.POST['subreddit']
        syft.search_term = request.POST['search_term']
        syft.save()
        return HttpResponseRedirect(reverse('detail', args=(syft.id,)))
    else:
        try:
            syft = Syft.objects.filter(
                owner=request.user).get(id=syft_id)
        except Syft.DoesNotExist as e:
            return redirect("error")
        return render(request, 'update.html', {'syft': syft})


@login_required
def delete(request, syft_id):
    try:
        syft = Syft.objects.filter(
            owner=request.user).get(id=syft_id)
    except Syft.DoesNotExist as e:
        return redirect("error")

    if request.method == 'POST':
        syft.delete()
        return redirect('dashboard')
    else:
        return redirect("error")
