from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegistrationForm(UserCreationForm):
    license_number = forms.CharField(required=False)
    store_name = forms.CharField(required=False)
    contact_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "role", "license_number", "password1", "password2")
        widgets = {
            'role': forms.RadioSelect(choices=User.ROLE_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Exclude admin from choices
        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES if choice[0] != User.ADMIN
        ]

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    store_name = forms.CharField(required=False)
    contact_number = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data