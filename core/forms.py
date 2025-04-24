from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import *
from datetime import datetime,date
from django.contrib.auth import get_user_model
from enum import Enum

User = get_user_model()


class PatientSignupForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username", max_length=150)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    dob = forms.DateField(label="Date of Birth", widget=forms.TextInput(attrs={'id': 'dob-picker', 'autocomplete': 'off'}))

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    class Meta:
        model = Patient
        fields = ['email', 'username', 'password1', 'password2', 'full_name', 'number', 'gender', 'dob', 'address']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        patient = super().save(commit=False)
        user = CustomUser(email=self.cleaned_data["email"], username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=Role.PATIENT)
            patient.user = user
            patient.email = self.cleaned_data["email"]
            patient.username = self.cleaned_data["username"]
            patient.save()
        return user

class DoctorSignupForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username", max_length=150)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    consultation_fee = forms.DecimalField(label="Consultation Fee", widget=forms.NumberInput(attrs={'min': '1', 'step': '0.5'}))

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    class Meta:
        model = Doctor
        fields = [
            'email', 'username', 'full_name', 'designation' ,'specialty',
            'details', 'qualification','photo','consultation_fee','password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already in use.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_consultation_fee(self):
        consultation_fee = self.cleaned_data.get("consultation_fee")
        if consultation_fee is not None and consultation_fee <= 0:
            raise ValidationError("Consultation fee must be greater than 0.")
        return consultation_fee

    def save(self, commit=True):
        doctor = super().save(commit=False)
        user = CustomUser(email=self.cleaned_data["email"], username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role=Role.DOCTOR)
            doctor.user = user
            doctor.email = self.cleaned_data["email"]
            doctor.username = self.cleaned_data["username"]
            doctor.save()
        return user

class PatientLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

class DoctorLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Please enter a correct email and password. Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

class DoctorEditProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Gender.choices, required=False)
    dob = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}), required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    consultation_fee = forms.DecimalField(widget=forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}))

    class Meta:
        model = Doctor
        fields = [
            'full_name', 'designation', 'specialty', 'number', 'address', 'details',
            'qualification', 'consultation_fee', 'certificate_url', 'photo'
        ]
        widgets = {
            'details': forms.Textarea(attrs={'rows': 2}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_consultation_fee(self):
        consultation_fee = self.cleaned_data.get("consultation_fee")
        if consultation_fee <= 0:
            raise ValidationError("Consultation fee must be greater than 0.")
        return consultation_fee

class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}), required=False)

    class Meta:
        model = Experience
        fields = ['medical_company', 'designation', 'department', 'employment_status', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be earlier than start date.")

        if start_date:
            end_date = end_date or datetime.now().date()
            delta = (end_date - start_date).days / 365.25
            cleaned_data['total_years'] = round(delta, 1)
            cleaned_data['period'] = f"{start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y') if end_date != datetime.now().date() else 'Present'}"
        return cleaned_data

# ExperienceFormSet = inlineformset_factory(
#     Doctor, Experience, form=ExperienceForm, extra=1, can_delete=True
# )    

ExperienceFormSet = inlineformset_factory(
    Doctor,
    Experience,
    fields=('medical_company', 'designation', 'department', 'employment_status', 'start_date', 'end_date'),
    extra=1,
    can_delete=True
)

class ScheduleAppointmentForm(forms.ModelForm):
    appointment_type = forms.ChoiceField(choices=AppointmentType.choices, widget=forms.Select(attrs={'id': 'appointment-type'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'id': 'appointment-date'}), initial=date.today)
    time = forms.TimeField(widget=forms.Select(attrs={'id': 'appointment-time'}))

    class Meta:
        model = Appointment
        fields = ['appointment_type', 'date', 'time']

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)
        self.fields['time'].choices = []

    def clean(self):
        cleaned_data = super().clean()
        appointment_type = cleaned_data.get('appointment_type')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if appointment_type and date and time and self.doctor:
            # Check if the time slot is available
            availability = self.doctor.availabilities.filter(
                date=date,
                start_time__lte=time,
                end_time__gte=time,
                appointment_type=appointment_type
            ).exists()
            if not availability:
                raise forms.ValidationError("This time slot is not available for the selected appointment type.")

            # Check if the time slot is already booked
            if Appointment.objects.filter(
                doctor=self.doctor,
                date=date,
                time=time,
                appointment_type=appointment_type
            ).exists():
                raise forms.ValidationError("This time slot is already booked.")
        return cleaned_data
    

class DoctorAvailabilityForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), initial=date.today)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}))
    appointment_type = forms.ChoiceField(choices=AppointmentType.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = DoctorAvailability
        fields = ['date', 'start_time', 'end_time', 'appointment_type']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError("End time must be after start time.")
        
        if date and date < date.today():
            raise forms.ValidationError("Availability date cannot be in the past.")

        return cleaned_data
    

class PatientEditProfileForm(forms.ModelForm):
    # gender = forms.ChoiceField(choices=Patient.Gender.choices, required=True)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Patient
        fields = ['full_name', 'number', 'dob', 'address', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False