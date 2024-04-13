from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    
class BankCard(models.Model):
    CARD_CHOICES = (
    ('VISA CLASSIC', 'Visa Classic'),
    ('VISA GOLD', 'Visa Gold'),
    ('VISA PLATINUM', 'Visa Platinum'),
    ('MASTERCARD STANDARD', 'Mastercard Standard'),
    ('MASTERCARD GOLD', 'Mastercard Gold'),
    ('MASTERCARD PLATINUM', 'Mastercard Platinum'),
)
    cardID = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=50, choices=CARD_CHOICES, blank=True)  # Debit, Credit, etc.
    card_number = models.CharField(max_length=16)  # Consider using a masked field for security
    expire_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User model
    
class CashbackOffer(models.Model):
    offerID = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Restaurants, Supermarkets, etc.
    company = models.CharField(max_length=100, null=True)  # Specific company or brand
    percentage = models.CharField(max_length=50, blank=True)  # Cashback percentage
    criteria = models.ForeignKey('Criteria', on_delete=models.CASCADE, null=True, blank=True)  # Optional foreign key to Criteria model
    valid_from = models.CharField(null=True)  # Date when offer starts
    valid_to = models.CharField(null=True, blank=True)  # Optional end date for the offer
    
class Criteria(models.Model):
    PAYMENT_METHOD_CHOICES = (
    ('APPLE_PAY', 'Apple Pay'),
    ('GOOGLE_PAY', 'Google Pay'),
    ('SAMSUNG_PAY', 'Samsung Pay')
)
    criteriaID = models.AutoField(primary_key=True)
    min_purchase_amount = models.CharField(max_length=50, null=True, blank=True)  # Minimum purchase amount for cashback
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)  # Payment method required for cashback
    days_of_week = models.CharField(max_length=50, null=True, blank=True)  # Days of the week when cashback is available
    bank_type = models.CharField(max_length=50, null=True, blank=True)  # Type of bank card required for cashback