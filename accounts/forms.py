from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        # Custom password validation
        if len(password) < 12:
            raise forms.ValidationError(
                "Password must be at least 12 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()_-+={}[]|:;<>,.?/~`" for char in password):
            raise forms.ValidationError(
                "Password must contain at least one special character.")

        # Django's built-in validators
        validate_password(password)

        return password
