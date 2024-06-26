from django.db import models

# Create your models here.
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Using email instead of gmail for clarity
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    
class BankCard(models.Model):
    cardID = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=50)  # Debit, Credit, etc.
    card_number = models.CharField(max_length=16)  # Consider using a masked field for security
    expiry_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to User model
    
class CashbackOffer(models.Model):
    offerID = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Restaurants, Supermarkets, etc.
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # Cashback percentage
    criteria = models.ForeignKey('Criteria', on_delete=models.CASCADE, null=True, blank=True)  # Optional foreign key to Criteria model
    valid_from = models.DateField()  # Date when offer starts
    valid_to = models.DateField(null=True, blank=True)  # Optional end date for the offer
    limitations = models.ManyToManyField('Limitations', blank=True)  # ManyToMany relationship with Limitations model
    
class Criteria(models.Model):
    criteriaID = models.AutoField(primary_key=True)
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Minimum purchase amount for cashback
    # Add other criteria fields as needed (e.g., specific products, membership requirements)
    
class Limitations(models.Model):
    limitationID = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    # Add other fields as needed (e.g., maximum cashback amount, number of transactions)