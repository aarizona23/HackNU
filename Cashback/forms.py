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
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'telephone', 'address']
    def save(self, commit=True):
        # Get the instance without saving it to the database
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password1'])
        instance.email = self.cleaned_data['email']
        instance.username = self.cleaned_data['email']
        
        # Save the instance to the database if commit is True
        if commit:
            instance.save()

        return instance

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
        
