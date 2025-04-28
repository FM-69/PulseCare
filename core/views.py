from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from core.forms import *
from django.views import View
from .models import Specialty, Doctor, UserProfile, DoctorAvailability, Appointment
import logging
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment
from django import forms

# Setup logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'index.html')

def patient_home(request):
    return render(request, "patient/home.html")

def patient_dashboard(request):
    return render(request, "patient/dashboard.html")

def doctor_dashboard(request):
    return render(request, "doctor/dashboard.html")

def doctor_home(request):
    return render(request, "doctor/home.html")

def message_request(request):
    return render(request, "doctor/respond_message_request.html")


#Prescription
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_text', 'recommended_tests']
        widgets = {
            'prescription_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter prescription details'}),
            'recommended_tests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter recommended tests (optional)'}),
        }

class AddPrescriptionView(View):
    def get(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        if hasattr(appointment, 'prescription'):
            messages.error(request, "A prescription has already been added for this appointment.")
            return redirect('core:doctor_appointments')

        form = PrescriptionForm()
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/add_prescription.html', context)

    def post(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        if hasattr(appointment, 'prescription'):
            messages.error(request, "A prescription has already been added for this appointment.")
            return redirect('core:doctor_appointments')

        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            messages.success(request, "Prescription added successfully.")
            return redirect('core:doctor_appointments')
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/add_prescription.html', context)
    
class FinishAppointmentView(View):
    def post(self, request, appointment_id):
        # Check if the user is the doctor or patient of the appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if not (hasattr(request.user, 'doctor') and request.user.doctor == appointment.doctor) and not (request.user == appointment.patient):
            messages.error(request, "You are not authorized to finish this appointment.")
            return redirect('core:index')

        # For doctors, ensure a prescription exists before finishing
        if hasattr(request.user, 'doctor'):
            if not hasattr(appointment, 'prescription'):
                messages.error(request, "You must add a prescription before finishing the appointment.")
                return redirect('core:doctor_appointments')

        # Check if a prescription exists before accessing its fields
        try:
            prescription = appointment.prescription
            prescription_text = prescription.prescription_text
            recommended_tests = prescription.recommended_tests if prescription.recommended_tests else ''
        except Appointment.prescription.RelatedObjectDoesNotExist:
            # If no prescription exists, show an error message
            messages.error(request, "No prescription found for this appointment. A prescription is required to finish the appointment.")
            if hasattr(request.user, 'doctor'):
                return redirect('core:doctor_appointments')
            return redirect('core:patient_dashboard')

        # Create a ServiceProvided record
        service = ServiceProvided(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment_type=appointment.appointment_type,
            date=appointment.date,
            time=appointment.time,
            prescription_text=prescription_text,
            recommended_tests=recommended_tests,
            consultation_link=appointment.consultation_link if appointment.consultation_link else ''
        )
        service.save()

        # Delete the appointment (this will also delete the prescription due to CASCADE)
        appointment.delete()

        messages.success(request, "Appointment finished successfully.")
        if hasattr(request.user, 'doctor'):
            return redirect('core:doctor_appointments')
        return redirect('core:patient_dashboard')

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['day_of_week', 'start_time', 'end_time', 'notes']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data

class DoctorSchedulesView(View):
    def get(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        doctor = request.user.doctor
        schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('day_of_week', 'start_time')
        form = DoctorScheduleForm()
        context = {
            'schedules': schedules,
            'form': form,
        }
        return render(request, 'doctor/schedules.html', context)

    def post(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        doctor = request.user.doctor
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.doctor = doctor
            schedule.save()
            messages.success(request, "Schedule added successfully.")
            return redirect('core:doctor_schedules')

        schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('day_of_week', 'start_time')
        context = {
            'schedules': schedules,
            'form': form,
        }
        return render(request, 'doctor/schedules.html', context)

class EditDoctorScheduleView(View):
    def get(self, request, schedule_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        schedule = get_object_or_404(DoctorSchedule, id=schedule_id, doctor=request.user.doctor)
        form = DoctorScheduleForm(instance=schedule)
        context = {
            'form': form,
            'schedule': schedule,
        }
        return render(request, 'doctor/edit_schedule.html', context)

    def post(self, request, schedule_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        schedule = get_object_or_404(DoctorSchedule, id=schedule_id, doctor=request.user.doctor)
        form = DoctorScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule updated successfully.")
            return redirect('core:doctor_schedules')
        context = {
            'form': form,
            'schedule': schedule,
        }
        return render(request, 'doctor/edit_schedule.html', context)

class DeleteDoctorScheduleView(View):
    def post(self, request, schedule_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        schedule = get_object_or_404(DoctorSchedule, id=schedule_id, doctor=request.user.doctor)
        schedule.delete()
        messages.success(request, "Schedule deleted successfully.")
        return redirect('core:doctor_schedules')



class ServiceProvidedView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        if hasattr(request.user, 'doctor'):
            services = ServiceProvided.objects.filter(doctor=request.user.doctor).order_by('-completed_at')
            template = 'doctor/service_provided.html'
        else:
            services = ServiceProvided.objects.filter(patient=request.user).order_by('-completed_at')
            template = 'patient/service_provided.html'

        context = {
            'services': services,
        }
        return render(request, template, context)

class SubmitReviewView(View):
    def post(self, request, service_id):
        if request.user.profile.role != 'PATIENT':
            messages.error(request, "You are not authorized to submit a review.")
            return redirect('core:index')

        service = get_object_or_404(ServiceProvided, id=service_id, patient=request.user)
        rating = request.POST.get('rating')
        review = request.POST.get('review')

        if rating and rating in [str(i) for i in range(1, 6)]:
            service.rating = int(rating)
        service.review = review
        service.save()

        messages.success(request, "Review submitted successfully.")
        return redirect('core:service_provided')

# Form for adding/editing the consultation link
class ConsultationLinkForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['consultation_link']
        widgets = {
            'consultation_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter meeting link (e.g., Zoom, Google Meet)'}),
        }

class AddAppointmentLinkView(View):
    def get(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        form = ConsultationLinkForm()
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/add_appointment_link.html', context)

    def post(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        form = ConsultationLinkForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultation link added successfully.")
            return redirect('core:doctor_appointments')
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/add_appointment_link.html', context)

class EditAppointmentLinkView(View):
    def get(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        form = ConsultationLinkForm(instance=appointment)
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/edit_appointment_link.html', context)

    def post(self, request, appointment_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor)
        form = ConsultationLinkForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Consultation link updated successfully.")
            return redirect('core:doctor_appointments')
        context = {
            'form': form,
            'appointment': appointment,
        }
        return render(request, 'doctor/edit_appointment_link.html', context)


class SelectSignupView(TemplateView):
    template_name = 'select_signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Signup Role'
        return context

class SelectLoginView(TemplateView):
    template_name = 'select_login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Login Role'
        return context

class PatientSignUpView(FormView):
    template_name = "core/patient_signup.html"
    form_class = PatientSignupForm
    success_url = reverse_lazy("core:patient_login")  # Redirect to patient login page

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, "You have successfully registered as a Patient. Please log in.")
            return super().form_valid(form)  # Redirect to patient login page
        except ValidationError as e:
            # If email is already in use, redirect to login page
            if "email is already in use" in str(e).lower():
                messages.error(self.request, "This email is already registered. Please log in instead.")
                return redirect('core:patient_login')
            # Other validation errors
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Handle form errors (e.g., email already in use, password mismatch)
        for field, errors in form.errors.items():
            for error in errors:
                if "email is already in use" in error.lower():
                    messages.error(self.request, "This email is already registered. Please log in instead.")
                    return redirect('core:patient_login')
                messages.error(self.request, error)
        return super().form_invalid(form)

class DoctorSignUpView(FormView):
    template_name = "core/doctor_signup.html"
    form_class = DoctorSignupForm
    success_url = reverse_lazy("core:doctor_login")  # Redirect to doctor login page

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, "You have successfully registered as a Doctor. Please log in.")
            return super().form_valid(form)  # Redirect to doctor login page
        except ValidationError as e:
            # If email is already in use, redirect to login page
            if "email is already in use" in str(e).lower():
                messages.error(self.request, "This email is already registered. Please log in instead.")
                return redirect('core:doctor_login')
            # Other validation errors
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Handle form errors (e.g., email already in use, password mismatch)
        for field, errors in form.errors.items():
            for error in errors:
                if "email is already in use" in error.lower():
                    messages.error(self.request, "This email is already registered. Please log in instead.")
                    return redirect('core:doctor_login')
                messages.error(self.request, error)
        return super().form_invalid(form)
    
class PatientLoginView(FormView):
    template_name = "core/patient_login.html"
    form_class = PatientLoginForm
    success_url = reverse_lazy("core:patient_home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user and user.is_active and hasattr(user, "profile") and user.profile.role == "PATIENT":
            login(self.request, user)
            messages.success(self.request, "You have logged in as a Patient.")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid credentials or not a patient.")
            return self.form_invalid(form)

class DoctorLoginView(FormView):
    template_name = "core/doctor_login.html"
    form_class = DoctorLoginForm
    success_url = reverse_lazy("core:doctor_dashboard")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user and user.is_active and hasattr(user, "profile") and user.profile.role == "DOCTOR":
            login(self.request, user)
            messages.success(self.request, "You have logged in as a Doctor.")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid credentials or not a doctor.")
            return self.form_invalid(form)

class PatientDashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated or request.user.profile.role != 'PATIENT':
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        # Fetch appointments for the patient
        appointments = Appointment.objects.filter(patient=request.user).select_related('doctor').order_by('-date', '-time')

        # Fetch payments for the patient
        payments = Payment.objects.filter(patient=request.user).select_related('appointment__doctor')

        # Fetch orders for the patient (if applicable)
        orders = Order.objects.filter(patient=request.user).prefetch_related('items__product')

        # Fetch doctors the patient has consulted with (based on appointments)
        doctors = Doctor.objects.filter(appointments__patient=request.user).distinct()

        # Check for pending or accepted message requests
        pending_request = MessageRequest.objects.filter(patient=request.user, status='PENDING').first()
        accepted_request = MessageRequest.objects.filter(patient=request.user, status='ACCEPTED').first()

        context = {
            'appointments': appointments,
            'payments': payments,
            'orders': orders,
            'doctors': doctors,
            'pending_request': pending_request,
            'accepted_request': accepted_request,
        }
        return render(request, 'patient/dashboard.html', context)

class DoctorDashboardView(View):
    def get(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        doctor = request.user.doctor
        # Fetch pending message requests
        message_requests = MessageRequest.objects.filter(
            doctor=doctor,
            status='PENDING'
        ).select_related('patient')

        # Fetch patients with appointments (past or upcoming)
        appointments = Appointment.objects.filter(
            doctor=doctor
        ).select_related('patient').distinct()

        # Extract unique patients from appointments
        patients = [appointment.patient for appointment in appointments]

        context = {
            'message_requests': message_requests,
            'patients': patients,  # Add patients to context
        }
        return render(request, 'doctor/dashboard.html', context)
    
class DoctorPatientListView(View):
    def get(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        doctor = request.user.doctor
        appointments = Appointment.objects.filter(doctor=doctor).select_related('patient').distinct()
        patients = list({appointment.patient.id: appointment.patient for appointment in appointments}.values())

        context = {
            'patients': patients,
        }
        return render(request, 'doctor/patient_list.html', context)
class DoctorProfileView(LoginRequiredMixin, TemplateView):
    template_name = "doctor/profile.html"

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "DOCTOR"):
            messages.error(request, "You are not authorized to access this page.")
            return redirect("core:doctor_login")
        try:
            doctor = request.user.doctor
            profile = request.user.profile
        except (AttributeError, Doctor.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "Doctor profile not found. Please complete your profile.")
            return redirect("core:doctor_edit_profile")
        context = {
            'doctor': doctor,
            'profile': profile,
        }
        return render(request, self.template_name, context)

    
class PatientProfileView(LoginRequiredMixin, TemplateView):
    template_name = "patient/profile.html"

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You are not authorized to access this page.")
            return redirect("core:patient_login")
        try:
            patient = request.user.patient
        except (AttributeError, Patient.DoesNotExist):
            messages.error(request, "Patient profile not found. Please complete your profile.")
            return redirect("core:patient_edit_profile")
        context = {
            'patient': patient,
        }
        return render(request, self.template_name, context)
    
class PatientEditProfileView(View):
    template_name = 'patient/edit_profile.html'

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You are not authorized to access this page.")
            return redirect("core:patient_login")
        
        try:
            patient = request.user.patient
        except (AttributeError, Patient.DoesNotExist):
            # If the patient profile doesn't exist, create one with minimal data
            patient = Patient(user=request.user, email=request.user.email, full_name=request.user.get_full_name() or request.user.username)
            patient.save()
        
        form = PatientEditProfileForm(instance=patient)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You are not authorized to access this page.")
            return redirect("core:patient_login")
        
        try:
            patient = request.user.patient
        except (AttributeError, Patient.DoesNotExist):
            patient = Patient(user=request.user, email=request.user.email, full_name=request.user.get_full_name() or request.user.username)
            patient.save()
        
        form = PatientEditProfileForm(request.POST, request.FILES, instance=patient)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('core:patient_profile')
        
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
  

class DoctorEditProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'full_name', 'designation', 'specialty', 'number', 'address',
            'details', 'qualification', 'consultation_fee', 'certificate_url', 'photo'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'form-control select2'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'certificate_url': forms.URLInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'custom-file-input', 'accept': 'image/*'}),
        }

class ExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}), required=False)

    class Meta:
        model = Experience
        fields = ['medical_company', 'designation', 'department', 'employment_status', 'start_date', 'end_date']
        widgets = {
            'medical_company': forms.Select(attrs={'class': 'form-control select2'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be earlier than start date.")
        return cleaned_data

ExperienceFormSet = inlineformset_factory(
    Doctor,
    Experience,
    form=ExperienceForm,
    extra=1,
    max_num=5,
    can_delete=True
)

class DoctorEditProfileView(View):
    template_name = 'doctor/edit-profile.html'

    def get(self, request):
        # Ensure the user is a doctor
        if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        doctor = request.user.doctor
        form = DoctorEditProfileForm(instance=doctor)
        formset = ExperienceFormSet(instance=doctor)
        context = {
            'form': form,
            'formset': formset,
            'max_experiences': 5,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Ensure the user is a doctor
        if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:home')

        doctor = request.user.doctor
        form = DoctorEditProfileForm(request.POST, request.FILES, instance=doctor)
        formset = ExperienceFormSet(request.POST, instance=doctor)

        # Validate the number of experiences
        existing_experiences = Experience.objects.filter(doctor=doctor).count()
        new_experiences = sum(1 for exp_form in formset if exp_form.is_valid() and exp_form.cleaned_data and not exp_form.cleaned_data.get('DELETE', False))
        if existing_experiences + new_experiences > 5:
            messages.error(request, "You cannot add more than 5 experiences.")
            context = {
                'form': form,
                'formset': formset,
                'max_experiences': 5,
            }
            return render(request, self.template_name, context)

        # Save the forms if valid
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('core:doctor_profile')

        # If validation fails, re-render the form with errors
        messages.error(request, "Please correct the errors below.")
        context = {
            'form': form,
            'formset': formset,
            'max_experiences': 5,
        }
        return render(request, self.template_name, context)
    
class DoctorsListView(TemplateView):
    template_name = "doctor/doctors_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_specialties = Specialty.objects.all()
        specialty_id = self.request.GET.get('specialty')
        
        if specialty_id:
            doctors = Doctor.objects.filter(specialty_id=specialty_id)
        else:
            doctors = Doctor.objects.all()
        
        logger.debug(f"Specialties found: {all_specialties.count()}")
        logger.debug(f"Selected specialty ID: {specialty_id}")
        logger.debug(f"Doctors found: {doctors.count()}")
        
        # Determine the base template based on user authentication and role
        if self.request.user.is_authenticated and hasattr(self.request.user, "profile") and self.request.user.profile.role == "PATIENT":
            base_template = "patient_base.html"
        else:
            base_template = "base.html"

        context['base_template'] = base_template
        context['all_specialties'] = all_specialties
        context['selected_specialty'] = specialty_id
        context['doctors'] = doctors
        return context

class DoctorAppointmentsView(View):
    def get(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        doctor = request.user.doctor
        appointments = Appointment.objects.filter(doctor=doctor).select_related('patient').order_by('-date', '-time')

        context = {
            'appointments': appointments,
        }
        return render(request, 'doctor/appointments.html', context)
    
class DoctorPaymentsView(View):
    def get(self, request):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        doctor = request.user.doctor
        payments = Payment.objects.filter(appointment__doctor=doctor).select_related('patient', 'appointment').order_by('-payment_date')

        context = {
            'payments': payments,
        }
        return render(request, 'doctor/payments.html', context)   
    
class DoctorDetailView(TemplateView):
    template_name = "patient/doctor_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor_id = kwargs.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)
        try:
            profile = doctor.user.profile
        except (AttributeError, UserProfile.DoesNotExist):
            profile = None
        
        logger.debug(f"Doctor ID: {doctor_id}, Name: {doctor.full_name}")
        
        context['doctor'] = doctor
        context['profile'] = profile
        return context

class PatientDetailView(View):
    def get(self, request, patient_id):
        if not hasattr(request.user, 'doctor'):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('core:index')

        patient = get_object_or_404(User, id=patient_id, profile__role='PATIENT')
        # Optionally, you can check if the patient has an appointment with the doctor
        appointments = Appointment.objects.filter(doctor=request.user.doctor, patient=patient)

        context = {
            'patient': patient,
            'appointments': appointments,
        }
        return render(request, 'doctor/patient_detail.html', context)

class ScheduleAppointmentView(View):
    template_name = 'patient/schedule_appointment.html'

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to schedule an appointment.")
            return redirect("core:patient_login")
        
        doctor_id = kwargs.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)
        
        if request.GET.get('ajax'):
            appointment_type = request.GET.get('appointment_type')
            date_str = request.GET.get('date')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'time_slots': []})
            
            availability = DoctorAvailability.objects.filter(
                doctor=doctor,
                date=date,
                appointment_type=appointment_type
            ).first()
            
            time_slots = []
            if availability:
                start = datetime.combine(date, availability.start_time)
                end = datetime.combine(date, availability.end_time)
                current = start
                booked_slots = Appointment.objects.filter(
                    doctor=doctor,
                    date=date,
                    appointment_type=appointment_type
                ).values_list('time', flat=True)
                
                while current <= end:
                    slot_time = current.time()
                    if slot_time not in booked_slots:
                        time_slots.append({
                            'value': slot_time.strftime('%H:%M:%S'),
                            'display': slot_time.strftime('%I:%M %p')
                        })
                    current += timedelta(minutes=30)
            
            return JsonResponse({'time_slots': time_slots})
        
        form = ScheduleAppointmentForm(doctor=doctor)
        context = {
            'form': form,
            'doctor': doctor,
        }
        return render(request, self.template_name, context)

class PaymentView(View):
    template_name = 'patient/payment.html'

    # Define AppointmentType choices directly in the view
    class AppointmentType:
        ONLINE = 'ONLINE', 'Online'
        IN_PERSON = 'IN_PERSON', 'In-Person'
        choices = [ONLINE, IN_PERSON]

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to make a payment.")
            return redirect("core:patient_login")

        doctor_id = request.GET.get('doctor_id')
        appointment_type = request.GET.get('appointment_type')
        date_str = request.GET.get('date')
        time_str = request.GET.get('time')

        if not (doctor_id and appointment_type and date_str and time_str):
            messages.error(request, "Invalid appointment details. Please select an appointment again.")
            return redirect("core:doctors_list")

        doctor = get_object_or_404(Doctor, id=doctor_id)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect("core:doctors_list")

        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=time_obj,
            end_time__gte=time_obj,
            appointment_type=appointment_type
        ).exists()
        if not availability:
            messages.error(request, "The selected time slot is not available.")
            return redirect("core:doctors_list")

        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time_obj,
            appointment_type=appointment_type
        ).exists():
            messages.error(request, "This time slot is already booked.")
            return redirect("core:doctors_list")

        # Use the defined AppointmentType choices to get the display value
        appointment_type_display = dict(self.AppointmentType.choices).get(appointment_type, appointment_type)

        context = {
            'doctor': doctor,
            'appointment_type': appointment_type,
            'appointment_type_display': appointment_type_display,
            'date': date_str,
            'time': time_str,
            'time_display': datetime.strptime(time_str, '%H:%M:%S').strftime('%I:%M %p'),
            'amount': 100.00,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to make a payment.")
            return redirect("core:patient_login")

        doctor_id = request.POST.get('doctor_id')
        appointment_type = request.POST.get('appointment_type')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        payment_method = request.POST.get('payment_method')

        if not (doctor_id and appointment_type and date_str and time_str and payment_method):
            messages.error(request, "Missing required payment details.")
            return redirect("core:doctors_list")

        doctor = get_object_or_404(Doctor, id=doctor_id)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
        except ValueError:
            messages.error(request, "Invalid date or time format.")
            return redirect("core:doctors_list")

        availability = DoctorAvailability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=time_obj,
            end_time__gte=time_obj,
            appointment_type=appointment_type
        ).exists()
        if not availability:
            messages.error(request, "The selected time slot is no longer available.")
            return redirect("core:doctors_list")

        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time_obj,
            appointment_type=appointment_type
        ).exists():
            messages.error(request, "This time slot is already booked.")
            return redirect("core:doctors_list")

        appointment = Appointment(
            patient=request.user,
            doctor=doctor,
            appointment_type=appointment_type,
            date=date,
            time=time_obj
        )
        appointment.save()

        payment = Payment(
            patient=request.user,
            appointment=appointment,
            amount=100.00,
            payment_method=payment_method,
            status='SUCCESS'
        )
        payment.save()

        logger.info(f"Payment of {payment.amount} by {request.user.email} for appointment with {doctor.full_name} on {date} at {time_obj}.")

        messages.success(request, "Payment successful! Your appointment has been booked.")
        return redirect('core:patient_dashboard')
    
class DoctorAvailabilityView(View):
    template_name = 'doctor/availability.html'

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "DOCTOR"):
            messages.error(request, "You must be logged in as a doctor to manage availability.")
            return redirect("core:doctor_login")
        
        doctor = get_object_or_404(Doctor, user=request.user)
        form = DoctorAvailabilityForm()
        availabilities = DoctorAvailability.objects.filter(doctor=doctor).order_by('date', 'start_time')
        
        context = {
            'form': form,
            'availabilities': availabilities,
            'doctor': doctor,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "DOCTOR"):
            messages.error(request, "You must be logged in as a doctor to manage availability.")
            return redirect("core:doctor_login")
        
        doctor = get_object_or_404(Doctor, user=request.user)
        
        if 'delete' in request.POST:
            availability_id = request.POST.get('availability_id')
            availability = get_object_or_404(DoctorAvailability, id=availability_id, doctor=doctor)
            availability.delete()
            messages.success(request, "Availability deleted successfully.")
            return redirect('core:doctor_availability')
        
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            messages.success(request, "Availability added successfully.")
            return redirect('core:doctor_availability')
        
        availabilities = DoctorAvailability.objects.filter(doctor=doctor).order_by('date', 'start_time')
        context = {
            'form': form,
            'availabilities': availabilities,
            'doctor': doctor,
        }
        return render(request, self.template_name, context)
  
class ProductListView(View):
    template_name = "patient/product_list.html"

    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        if category:
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all()

        if request.user.is_authenticated and hasattr(request.user, "profile") and request.user.profile.role == "PATIENT":
            base_template = "patient_base.html"
        else:
            base_template = "base.html"

        context = {
            'base_template': base_template,
            'products': products,
            'selected_category': category,
            'categories': Product.Category.choices,
        }
        return render(request, self.template_name, context)

class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to add items to the cart.")
            return redirect("core:patient_login")

        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        # Get or create the patient's cart
        cart, created = Cart.objects.get_or_create(patient=request.user)

        # Check if the product is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"{product.name} has been added to your cart.")
        return redirect('core:cart')

class CartView(View):
    template_name = "patient/cart.html"

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to view the cart.")
            return redirect("core:patient_login")

        try:
            cart = Cart.objects.get(patient=request.user)
            cart_items = cart.items.all()
            total = sum(item.total_price for item in cart_items)
        except Cart.DoesNotExist:
            cart_items = []
            total = 0

        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, self.template_name, context)

class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to remove items from the cart.")
            return redirect("core:patient_login")

        cart_item_id = request.POST.get('cart_item_id')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__patient=request.user)
        product_name = cart_item.product.name
        cart_item.delete()

        messages.success(request, f"{product_name} has been removed from your cart.")
        return redirect('core:cart')

class CheckoutView(View):
    template_name = "patient/checkout.html"

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to checkout.")
            return redirect("core:patient_login")

        try:
            cart = Cart.objects.get(patient=request.user)
            cart_items = cart.items.all()
            if not cart_items:
                messages.error(request, "Your cart is empty.")
                return redirect('core:cart')
            total = sum(item.total_price for item in cart_items)
        except Cart.DoesNotExist:
            messages.error(request, "Your cart is empty.")
            return redirect('core:product_list')

        context = {
            'cart_items': cart_items,
            'total': total,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to checkout.")
            return redirect("core:patient_login")

        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('core:checkout')

        try:
            cart = Cart.objects.get(patient=request.user)
            cart_items = cart.items.all()
            if not cart_items:
                messages.error(request, "Your cart is empty.")
                return redirect('core:product_list')
            total = sum(item.total_price for item in cart_items)
        except Cart.DoesNotExist:
            messages.error(request, "Your cart is empty.")
            return redirect('core:product_list')

        # Calculate delivery date (e.g., 3 days from today)
        delivery_date = date.today() + timedelta(days=3)

        # Create the order
        order = Order(
            patient=request.user,
            total_amount=total,
            payment_method=payment_method,
            delivery_date=delivery_date,
            status='PENDING'
        )
        order.save()

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear the cart
        cart_items.delete()

        logger.info(f"Order placed by {request.user.email} for {total} with delivery on {delivery_date}.")

        messages.success(request, f"Payment successful! Your order will be delivered on {delivery_date.strftime('%Y-%m-%d')}.")
        return redirect('core:patient_dashboard')


class SendMessageRequestView(View):
    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "PATIENT"):
            messages.error(request, "You must be logged in as a patient to send a message request.")
            return redirect("core:patient_login")

        doctor_id = request.POST.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)

        # Check if the patient already has a pending message request
        if MessageRequest.objects.filter(patient=request.user, status='PENDING').exists():
            messages.error(request, "You already have a pending message request. Please wait for the doctor to respond.")
            return redirect('core:doctor_detail', doctor_id=doctor.id)

        # Create the message request
        message_request = MessageRequest(
            patient=request.user,
            doctor=doctor,
            status='PENDING'
        )
        message_request.save()

        logger.info(f"Message request sent by {request.user.email} to {doctor.full_name}.")
        messages.success(request, f"Message request sent to {doctor.full_name}. You will be notified once they respond.")
        return redirect('core:patient_dashboard')

class RespondMessageRequestView(View):
    template_name = 'doctor/respond_message_request.html'

    def get(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "DOCTOR"):
            messages.error(request, "You must be logged in as a doctor to respond to message requests.")
            return redirect("core:doctor_login")

        message_request_id = kwargs.get('message_request_id')
        if not message_request_id:
            messages.warning(request, "Please select a message request to respond to.")
            return redirect("core:doctor_dashboard")

        message_request = get_object_or_404(MessageRequest, id=message_request_id, doctor__user=request.user, status='PENDING')

        context = {
            'message_request': message_request,
            'patient': message_request.patient,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not (hasattr(request.user, "profile") and request.user.profile.role == "DOCTOR"):
            messages.error(request, "You must be logged in as a doctor to respond to message requests.")
            return redirect("core:doctor_login")

        message_request_id = request.POST.get('message_request_id')
        action = request.POST.get('action')  # 'accept' or 'reject'
        message_request = get_object_or_404(MessageRequest, id=message_request_id, doctor__user=request.user)

        if action == 'accept':
            message_request.status = 'ACCEPTED'
            message_request.save()
            messages.success(request, f"Message request from {message_request.patient.email} accepted. You can now chat with them.")
            return redirect('core:chat', message_request_id=message_request.id)
        elif action == 'reject':
            patient_email = message_request.patient.email
            message_request.delete()
            messages.success(request, f"Message request from {patient_email} rejected and deleted.")
            return redirect('core:doctor_dashboard')
        else:
            messages.error(request, "Invalid action.")
            return redirect('core:doctor_dashboard')
        
class ChatView(View):
    def get_template_name(self, user):
        if hasattr(user, 'profile') and user.profile.role == 'DOCTOR':
            return 'doctor/doctor_chat.html'  # Updated path
        elif user == user:  # For patients, user is the patient
            return 'patient/patient_chat.html'  # Updated path
        return 'core/chat.html'  # Fallback, though this shouldn't happen

    def get(self, request, *args, **kwargs):
        message_request_id = kwargs.get('message_request_id')
        message_request = get_object_or_404(MessageRequest, id=message_request_id, status='ACCEPTED')

        # Check if the user is part of the chat (either patient or doctor)
        if not (
            (request.user == message_request.patient) or 
            (hasattr(request.user, 'doctor') and request.user.doctor == message_request.doctor)
        ):
            messages.error(request, "You are not authorized to access this chat.")
            return redirect('core:index')

        messages = ChatMessage.objects.filter(message_request=message_request).order_by('timestamp')

        context = {
            'message_request': message_request,
            'messages': messages,
            'other_party': message_request.doctor.full_name if request.user == message_request.patient else message_request.patient.email,
        }
        return render(request, self.get_template_name(request.user), context)

    def post(self, request, *args, **kwargs):
        message_request_id = kwargs.get('message_request_id')
        message_request = get_object_or_404(MessageRequest, id=message_request_id, status='ACCEPTED')

        # Check if the user is part of the chat (either patient or doctor)
        if not (
            (request.user == message_request.patient) or 
            (hasattr(request.user, 'doctor') and request.user.doctor == message_request.doctor)
        ):
            messages.error(request, "You are not authorized to access this chat.")
            return redirect('core:index')

        message_content = request.POST.get('message')
        if not message_content:
            messages.error(request, "Message cannot be empty.")
            return redirect('core:chat', message_request_id=message_request.id)

        # Save the chat message
        chat_message = ChatMessage(
            message_request=message_request,
            sender=request.user,
            message=message_content
        )
        chat_message.save()

        logger.info(f"Chat message sent by {request.user.email} in chat {message_request.id}.")
        return redirect('core:chat', message_request_id=message_request.id)

class UserLogoutView(View):
    success_url = reverse_lazy("core:index")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You are not logged in.")
            return redirect(self.success_url)

        # Log the logout action
        role = request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown'
        logger.info(f"User {request.user.username} (Role: {role}) logged out at {datetime.now()}.")

        # Perform logout
        self.logout_user(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You are not logged in.")
            return redirect(self.success_url)

        # Log the logout action
        role = request.user.profile.role if hasattr(request.user, 'profile') else 'Unknown'
        logger.info(f"User {request.user.username} (Role: {role}) logged out at {datetime.now()}.")

        # Perform logout
        self.logout_user(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect(self.success_url)

    def logout_user(self, request):
        """
        Helper method to handle the logout process.
        """
        from django.contrib.auth import logout
        logout(request)
        # Clear session data
        request.session.flush()