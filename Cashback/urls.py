from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... other URL patterns ...
    path('', views.run_page, name='run_page'),
]