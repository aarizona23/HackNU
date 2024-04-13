from django import forms
from .models import BankCard, User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'surname', 'email', 'telephone', 'address', 'password1', 'password2')
    def save(self, commit=True):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()

        return instance
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['name'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['surname'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['telephone'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'class' : 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs = {'class' : 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs = {'class' : 'form-control'})

class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ('bank_name', 'card_type', 'card_number', 'expiry_date')

    def save(self, commit=True, user=None):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        
        # Set the 'type' field to 'Vehicle'
        instance.user = user
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()

        return instance
    
    def __init__(self, *args, **kwargs):
        super(BankCardForm, self).__init__(*args, **kwargs)

        self.fields['bank_name'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['card_type'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['card_number'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['expiry_date'].widget = forms.DateInput(attrs = {'class' : 'form-control'})
        
