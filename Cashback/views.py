from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, BankCardForm, CustomLoginForm
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# Create your views here.'
def run_page(request):
    print("hi")
    return render(request, 'main.html')

def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('registerCards')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_cards(request):
    if request.method == 'POST':
        form = BankCardForm(request.POST)
        if form.is_valid():
            card = form.save(user=request.user)
            card.save()
            return redirect('run_page')
        else:
            return render(request, 'register_cards.html', {'form': form})
    else:
        form = BankCardForm()
    return render(request, 'register_cards.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})
