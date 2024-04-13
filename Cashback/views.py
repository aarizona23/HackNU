from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, BankCardForm


# Create your views here.'
def run_page(request):
    print("hi")
    return render(request, 'main.html')

def register(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    bank_card_form = BankCardForm(request.POST)  # Create a BankCardForm instance
    if user_form.is_valid() and bank_card_form.is_valid():
      user = user_form.save()
      # Save the first bank card after creating the user
      bank_card_form.instance.user = user  # Set the user for the bank card
      bank_card_form.save()
      # Optionally handle additional bank cards using another BankCardForm instance
      # ... (see explanation below)
      return redirect('run_page')  # Redirect to success page
  else:
    user_form = UserRegistrationForm()
    bank_card_form = BankCardForm()  # Create an empty BankCardForm instance
  return render(request, 'register.html', {'user_form': user_form, 'bank_card_form': bank_card_form})
