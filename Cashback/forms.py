from django import forms
from .models import BankCard, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('Invalid username or password.')

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs = {'class' : 'form-control'})

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone', 'address', 'password1', 'password2')
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
        self.fields['first_name'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['telephone'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs = {'class' : 'form-control'})
        self.fields['address'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs = {'class' : 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs = {'class' : 'form-control'})

class BankCardForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ('bank_name', 'card_type', 'card_number', 'expire_date')

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
        self.fields['card_type'].widget = forms.Select(attrs={'class': 'form-control'}, choices = BankCard.CARD_CHOICES)  # Add the Select widget with 'form-control' class
        self.fields['card_number'].widget = forms.TextInput(attrs = {'class' : 'form-control'})
        self.fields['expire_date'].widget = forms.DateInput(attrs = {'class' : 'form-control'}, format='%m/%d/%Y')
        
