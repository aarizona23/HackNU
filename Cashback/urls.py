from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... other URL patterns ...
    path('', views.main_page, name='main_page'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.logining, name='login'),
    path('add_cards/', views.add_cards, name='add_cards'),
    path('my_cards/', views.my_cards, name='my_cards'),
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('add_user_cards/', views.add_user_cards, name='add_user_cards'),
    path('user_cards/', views.user_cards, name='user_cards'),
    path('get_cashbacks/<str:category>/<str:company_name>/<int:purchase_amount>/', views.get_cashbacks, name='get_cashbacks'),
    path('logout/', views.logout, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)