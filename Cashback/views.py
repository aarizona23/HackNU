from django.shortcuts import render
import requests
import json
from django.http import JsonResponse


# Create your views here.'
def run_page(request):
    return render(request, 'main.html')
