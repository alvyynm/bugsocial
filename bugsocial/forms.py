from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import get_user_model

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']

    def clean_password_confirmation(self):
        """Compare passwords and raise validation error if they don't match

        Raises:
            forms.ValidationError: Passwords do not match

        Returns:
            string: password_confirmation field data
        """
        data = self.cleaned_data

        if data['password'] != data['password_confirmation']:
            raise forms.ValidationError("Passwords do not match")
        return data['password_confirmation']

    def clean_email(self):
        """Prevent the user from using an existing email

        Raises:
            forms.ValidationError: Invalid email address

        Returns:
            str: email address
        """
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Invalid email address')

        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        """Prevent the user from changing their email address to an email address of an existing user

        Raises:
            forms.ValidationError: Invalid email address

        Returns:
            str: email address
        """
        data = self.cleaned_data['email']

        query = User.objects.exclude(id=self.instance.id).filter(email=data)

        if query.exists():
            raise forms.ValidationError('Invalid email address')

        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
