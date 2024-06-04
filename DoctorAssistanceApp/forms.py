from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
import datetime


class UserForm(forms.ModelForm):
    is_active =  forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get('contact')
        email = cleaned_data.get('email')

        # Check for uniqueness of contact
        if User.objects.filter(contact=contact).exclude(pk=self.instance.pk).exists():
            self.add_error('contact', 'This contact number is already exist.')

        # Check for uniqueness of email
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', 'This email address is already exist.')
            
        return cleaned_data


class DoctorForm(forms.ModelForm):
    is_active =  forms.IntegerField(required=False)

    class Meta:
        model = Doctor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get('contact')
        email = cleaned_data.get('email')

        # Check for uniqueness of contact
        if Doctor.objects.filter(contact=contact).exclude(pk=self.instance.pk).exists():
            self.add_error('contact', 'This contact number is already exist.')

        # Check for uniqueness of email
        if Doctor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error('email', 'This email address is already exist.')
            
        return cleaned_data