from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from .models import Syft
import logging


def index(request):
    logger = logging.getLogger()
    logger.info("Home page was loaded, hello 8592837")
    if not request.user.is_authenticated:
        return render(request, 'welcome.html')
    current_user = request.user
    syfts = Syft.objects.filter(
        owner=current_user).all()
    context = {
        'syfts': syfts,
    }
    return render(request, 'index.html', context)


def detail(request, syft_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        syft = Syft.objects.filter(owner=request.user).get(id=syft_id)
    except Syft.DoesNotExist as e:
        return redirect("login")
    return render(request, 'detail.html', {'syft': syft})


def create(request):
    if request.method == 'POST':
        syft = Syft(owner=request.user,
                    subreddit=request.POST['subreddit'],
                    search_term=request.POST['search_term'])
        syft.save()
        return redirect("../")
    else:
        return render(request, 'create.html')


def update(request, syft_id):
    if not request.user.is_authenticated:
        return redirect('login')
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
            return redirect("login")
        return render(request, 'update.html', {'syft': syft})


def delete(request, syft_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        syft = Syft.objects.filter(
            owner=request.user).get(id=syft_id)
    except Syft.DoesNotExist as e:
        return redirect("login")

    if request.method == 'POST':
        syft.delete()
        return redirect('index')
    else:
        return redirect("login")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
