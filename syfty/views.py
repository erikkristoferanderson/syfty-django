from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from .models import Search
import logging


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'welcome.html')
    current_user = request.user
    searches = Search.objects.filter(
        owner=current_user).all()
    context = {
        'searches': searches,
    }
    return render(request, 'index.html', context)


def detail(request, search_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        search = Search.objects.filter(owner=request.user).get(id=search_id)
    except Search.DoesNotExist as e:
        return redirect("login")
    # print(search)
    return render(request, 'detail.html', {'search': search})


def create(request):
    if request.method == 'POST':
        search = Search(owner=request.user,
                        subreddit=request.POST['subreddit'],
                        search_term=request.POST['search_term'])
        search.save()
        return redirect("../")
    else:
        return render(request, 'create.html')


def update(request, search_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        search = get_object_or_404(Search, pk=search_id)
        search.subreddit = request.POST['subreddit']
        search.search_term = request.POST['search_term']
        search.save()
        return HttpResponseRedirect(reverse('detail', args=(search.id,)))
    else:
        try:
            search = Search.objects.filter(
                owner=request.user).get(id=search_id)
        except Search.DoesNotExist as e:
            return redirect("login")
        return render(request, 'update.html', {'search': search})


def delete(request, search_id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        search = Search.objects.filter(
            owner=request.user).get(id=search_id)
    except Search.DoesNotExist as e:
        return redirect("login")

    if request.method == 'POST':
        search.delete()
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
