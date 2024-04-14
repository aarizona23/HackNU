from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponse
import requests
import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm, BankCardForm, CustomLoginForm, UserAdditionalInfoForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import BankCard, CashbackOffer, Criteria
from .parsing import parse_func
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import decimal as d

# Create your views here.'
@login_required
def main_page(request):
    if request.method == 'POST': 
        purchase_amount = request.POST.get('purchase_amount')
        category = request.POST.get('item_category')
        company_name = request.POST.get('company_name')
        return redirect('get_cashbacks', category=category, company_name=company_name, purchase_amount=purchase_amount)
    return render(request, 'cashbacks.html')

def registerUser(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def add_user_cards(request):
    if request.method == 'POST':
        form = BankCardForm(request.POST)
        if form.is_valid():
            card = form.save(user=request.user)
            card.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_user(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': 'Invalid credentials'}, status=400)

@login_required
def user_cards(request):
    user = request.user
    cards = user.bankcard_set.all()
    # Serialize cards if needed
    serialized_cards = [{'number': card.number, 'expiry_date': card.expiry_date} for card in cards]
    return JsonResponse({'cards': serialized_cards})

@login_required
def user_logout(request):
    logout(request)
    return JsonResponse({'success': True})

def register_user(request):
    if request.method == 'POST':
        if 'step' in request.POST:
            if request.POST['step'] == '1':
                main_form = CustomUserCreationForm(request.POST)
                if main_form.is_valid():
                    # Save the main form data to the session
                    request.session['main_form_data'] = main_form.cleaned_data
                    return JsonResponse({'success': True, 'step': 2})
                else:
                    return JsonResponse({'success': False, 'errors': main_form.errors}, status=400)
            elif request.POST['step'] == '2':
                extra_form = UserAdditionalInfoForm(request.POST)
                if extra_form.is_valid():
                    # Merge the main form data from the session with the extra form data
                    main_form_data = request.session.get('main_form_data', {})
                    main_form_data.update(extra_form.cleaned_data)
                    # Create a new user with the merged form data
                    user = CustomUserCreationForm(main_form_data).save()
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'errors': extra_form.errors}, status=400)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def add_cards(request):
    if request.method == 'POST':
        form = BankCardForm(request.POST)
        if form.is_valid():
            card = form.save(user=request.user)
            card.save()
            return redirect('my_cards')
        else:
            return render(request, 'add_cards.html', {'form': form})
    else:
        form = BankCardForm()
    return render(request, 'add_cards.html', {'form': form})

def logining(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def my_cards(request):
    user = request.user
    cards = user.bankcard_set.all()
    return render(request, 'my_cards.html', {'cards': cards})

@login_required
def logout(request):
    logout(request)
    return redirect('login')

class Cashback:
    def __init__(self, bank_name, category, percentage, valid_from, valid_to, company_name, criteria, purchase_amount, payment_method, days_of_week):
        self.bank_name = bank_name
        self.category = category
        self.percentage = percentage
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.company_name = company_name
        self.min_purchase_amount = 0
        self.payment_method = payment_method
        self.days_of_week = days_of_week

    def __str__(self):
        return f"Bank: {self.bank_name}, Category: {self.category}, Percentage: {self.percentage}, Valid From: {self.valid_from}, Valid To: {self.valid_to}, Company Name: {self.company_name}, Minimum Purchase Amount: {self.min_purchase_amount}, Payment Method: {self.payment_method}, Days of Week: {self.days_of_week}"

def dictionary_of_categories(request):
    category_names = dict()
    product_names = ('супермаркеты', 'продукты', 'продуктовые магазины', 'продуктовые')
    food_names = ('рестораны', 'фастфуд', 'кафе', 'ресторан', 'фудкорты', 'фудкорт', 'фудкорта')
    entertainment_names = ('кинотеатры', 'развлечения', 'развлекательные центры', 'развлекательные', 'кино', 'кинотеатр', 'кино и музыка онлайн', 'досуг и книги')
    tech_names = ('электроника', 'техника', 'техники', 'технические магазины', 'технические')
    telephony_names = ('телефоны', 'мобильная связь', 'мобильные операторы', 'мобильные', 'наушники', 'гарнитуры')
    transport_names = ('транспорт', 'такси', 'транспортные компании', 'транспортные')
    beauty_names = ('косметика', 'парфюмерия', 'косметические магазины', 'косметические')
    clothes_names = ('одежда', 'мода', 'модные магазины', 'модные')
    home_names = ('дом', 'домашние магазины', 'домашние', 'домашний текстиль', 'постельное белье')
    auto_names = ('авто', 'автомобили', 'автомобильные магазины', 'автомобильные', 'автозапчасти', 'автосервисы', 'автосервис', 'автомобильные заправочные станции', 'автомобильные заправочные')
    computer_names = ('компьютеры', 'ноутбуки', 'компьютерные магазины', 'компьютерные')
    kids_names = ('дети', 'детские магазины', 'детские', 'детские товары', 'детские игрушки')
    sport_names = ('спорт', 'спортивные магазины', 'спортивные', 'спортивные товары', 'спортивные товары', 'спорт и туризм')
    health_names = ('здоровье', 'аптеки', 'медицинские магазины', 'медицинские', 'медицинские товары', 'медицинские товары')
    jewelry_names = ('ювелирные магазины', 'ювелирные', 'ювелирные изделия', 'ювелирные изделия')
    furniture_names = ('мебельные магазины', 'мебельные', 'мебельные товары', 'мебельные товары')
    building_names = ('строительные магазины', 'строительные', 'строительные товары', 'строительные товары')
    chancery_names = ('канцелярские магазины', 'канцелярские', 'канцелярские товары', 'канцелярские товары')
    animals_names = ('зоомагазины', 'зоомагазины', 'зоотовары', 'зоотовары', 'товары для животных')
    shoes_names = ('обувные магазины', 'обувные', 'обувные товары', 'обувные товары', 'обувь')
    accessories_names = ('аксессуары', 'аксессуары', 'аксессуары для телефонов', 'аксессуары для телефонов', 'аксессуары для компьютеров', 'аксессуары для компьютеров')
    travel_names = ('туризм', 'туристические агентства', 'туристические', 'туристические товары', 'туристические товары')
    celebration_names = ('праздники', 'праздничные товары', 'праздничные', 'праздничные товары')
    other_names = ('другое', 'другие товары', 'другие')
    
    category_names['products'] = product_names
    category_names['food'] = food_names
    category_names['entertainment'] = entertainment_names
    category_names['tech'] = tech_names
    category_names['telephony'] = telephony_names
    category_names['transport'] = transport_names
    category_names['beauty'] = beauty_names
    category_names['clothes'] = clothes_names
    category_names['home'] = home_names
    category_names['auto'] = auto_names
    category_names['computer'] = computer_names
    category_names['kids'] = kids_names
    category_names['sport'] = sport_names
    category_names['health'] = health_names
    category_names['jewelry'] = jewelry_names
    category_names['furniture'] = furniture_names
    category_names['building'] = building_names
    category_names['chancery'] = chancery_names
    category_names['animals'] = animals_names
    category_names['shoes'] = shoes_names
    category_names['accessories'] = accessories_names
    category_names['travel'] = travel_names
    category_names['celebration'] = celebration_names
    category_names['other'] = other_names
    return category_names

def get_category(request, category):
    category_names = dictionary_of_categories(request)
    for key, value in category_names.items():
        if category in value:
            return key
    return None

def save_cashbacks(request):
    cashbacks = parse_func()
    
    for cashback in cashbacks:
        try:
            # Check if the CashbackOffer already exists with the same details
            cat = get_category(request, cashback['category'])
            offer = CashbackOffer.objects.get(
                bank_name=cashback['bank_name'],
                category=cat,
                company=cashback['company'],
                percentage=cashback['percentage'],
                valid_from=cashback['valid_from'],
                valid_to=cashback['valid_to'],
            )
            print("Offer already exists:", offer)
        except ObjectDoesNotExist:
            # Create new Criteria object
            criteria = Criteria.objects.create(
                min_purchase_amount=cashback['min_purchase_amount'],
                payment_method=cashback['payment_method'],
                days_of_week=cashback['days_of_week'],
                bank_type=cashback['bank_type']
            )
            
            # Create new CashbackOffer object
            cat = get_category(request, cashback['category'])
            offer = CashbackOffer.objects.create(
                bank_name=cashback['bank_name'],
                category=cat,
                company=cashback['company'],
                percentage=cashback['percentage'],
                valid_from=cashback['valid_from'],
                valid_to=cashback['valid_to'],
                criteria=criteria
            )
            print("New offer created:", offer)

        
@login_required        
def get_cashbacks(request, category, company_name, purchase_amount):
    user = request.user
    cards = BankCard.objects.filter(user=user)
    bank_names = [card.bank_name for card in cards]
    optimals = []
    cashbacks = CashbackOffer.objects.filter(category=category, company=company_name)
    for cashback in cashbacks:
        if cashback.bank_name in bank_names:
            card_type = BankCard.objects.get(bank_name=cashback.bank_name).card_type
            if (((cashback.criteria.min_purchase_amount is not None and 
    int(cashback.criteria.min_purchase_amount) <= purchase_amount) or \
   (cashback.criteria.min_purchase_amount is None)) and 
    (cashback.criteria.bank_type is None or cashback.criteria.bank_type == card_type)):
                optimals.append(cashback)
    return render(request, 'optimal_cashbacks.html', {'cashbacks': optimals})

@login_required
def cashback_form(request):
    if request.method == 'POST':
        purchase_amount = request.POST.get('purchase_amount')
        category = request.POST.get('item_category')
        company_name = request.POST.get('company_name')
        return redirect('get_cashbacks', category=category, company_name=company_name, purchase_amount=purchase_amount)
    return JsonResponse({'message': 'Welcome to the main page'})

@login_required
def get_card_cashbacks(request, category, company_name, purchase_amount):
    user = request.user
    cards = BankCard.objects.filter(user=user)
    bank_names = [card.bank_name for card in cards]
    optimals = []
    cashbacks = CashbackOffer.objects.filter(category=category, company=company_name)
    for cashback in cashbacks:
        if cashback.bank_name in bank_names:
            card_type = BankCard.objects.get(bank_name=cashback.bank_name).card_type
            if ((cashback.criteria.min_purchase_amount is None or int(cashback.criteria.min_purchase_amount) <= purchase_amount) and
                    (cashback.criteria.bank_type is None or cashback.criteria.bank_type == card_type)):
                optimals.append({
                    'bank_name': cashback.bank_name,
                    'category': cashback.category,
                    'percentage': str(cashback.percentage),
                    'valid_from': cashback.valid_from.strftime('%Y-%m-%d') if cashback.valid_from else None,
                    'valid_to': cashback.valid_to.strftime('%Y-%m-%d') if cashback.valid_to else None,
                    'company': cashback.company,
                    'min_purchase_amount': str(cashback.criteria.min_purchase_amount) if cashback.criteria.min_purchase_amount else None,
                    'payment_method': cashback.criteria.payment_method,
                    'days_of_week': cashback.criteria.days_of_week,
                    'bank_type': cashback.criteria.bank_type
                })
    for cashback in optimals:
        if 'percentage' in cashback:
            cashback['percentage'] = float(cashback['percentage'])
    optimals.sort(key=lambda x: x.get('percentage', 0), reverse=True)

    return JsonResponse({'cashbacks': optimals})

        
