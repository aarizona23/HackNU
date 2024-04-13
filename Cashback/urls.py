from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... other URL patterns ...
    path('', views.run_page, name='run_page'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.login, name='login'),
    path('add_cards/', views.add_cards, name='add_cards'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)