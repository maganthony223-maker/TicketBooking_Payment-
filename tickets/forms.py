from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Match, Profile


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=150, label="Full Name")
    email = forms.EmailField()
    contact = forms.CharField(max_length=30)
    location = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username", "name", "email", "contact", "location", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["name"]  # Assuming last name is the same as full name
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                contact=self.cleaned_data["contact"],
                location=self.cleaned_data["location"],
            )
        return user


class BookingForm(forms.ModelForm):
    tickets = forms.IntegerField(min_value=1, max_value=10, label="Number of Tickets")

    class Meta:
        model = Booking
        fields = ("match", "tickets", "seat", "ticket_type", "payment_method")
        labels = {"match": "Select Match", "seat": "Seat Preference", "payment_method": "Payment Method"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only matches that haven't happened yet
        self.fields["match"].queryset = Match.objects.filter(date__gte=date.today())
