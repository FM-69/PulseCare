from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("Username"), max_length=150, unique=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

class Role(models.TextChoices):
    MEMBER = 'MEMBER', 'Member'
    DOCTOR = 'DOCTOR', 'Doctor'
    PATIENT = 'PATIENT', 'Patient'
    ADMIN = 'ADMIN', 'Admin'

class Gender(models.TextChoices):
    MALE = 'MALE', _('Male')
    FEMALE = 'FEMALE', _('Female')
    OTHER = 'OTHER', _('Other')

class Specialty(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:specialty_detail", args=[self.slug])

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    dob = models.DateField()
    address = models.TextField(max_length=550, null=True, blank=True)
    photo = models.FileField(
        upload_to="myimage", default="myimage/blank.png", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    designation = models.CharField(max_length=100)
    full_name = models.CharField(max_length=255)
    number = models.CharField(max_length=20, null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    address = models.TextField(max_length=550, null=True, blank=True)
    details = models.TextField()
    photo = models.FileField(
        upload_to="myimage", default="myimage/blank.png", blank=True
    )
    qualification = models.CharField(max_length=255)
    consultation_fee = models.FloatField()
    certificate_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.full_name}"
    
class MedicalCompany(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class EmploymentStatus(models.TextChoices):
    FULL_TIME = 'FULL_TIME', 'Full-Time'
    PART_TIME = 'PART_TIME', 'Part-Time'
    CONTRACT = 'CONTRACT', 'Contract'
    RETIRED = 'RETIRED', 'Retired'

class Experience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='experiences')
    medical_company = models.ForeignKey(MedicalCompany, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    employment_status = models.CharField(max_length=20, choices=EmploymentStatus.choices)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation} at {self.medical_company.name}"

    @property
    def period(self):
        if self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        return f"{self.start_date.strftime('%b %Y')} - Present"

    @property
    def total_years(self):
        from datetime import date
        end = self.end_date or date.today()
        delta = end - self.start_date
        years = delta.days / 365.25
        return round(years, 1)
    

class AppointmentType(models.TextChoices):
    ONLINE = 'ONLINE', 'Online'
    IN_CHAMBER = 'IN_CHAMBER', 'In-Chamber'

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor.full_name} - {self.date} {self.start_time}-{self.end_time} ({self.appointment_type})"

class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=20, choices=AppointmentType.choices)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    consultation_link = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.full_name} on {self.date} at {self.time} ({self.appointment_type})"
class Payment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('SUCCESS', 'Success'),
            ('FAILED', 'Failed'),
            ('PENDING', 'Pending'),
        ],
        default='SUCCESS'
    )

    def __str__(self):
        return f"Payment of {self.amount} by {self.patient.email} on {self.payment_date}"

class Product(models.Model):
    class Category(models.TextChoices):
        LAB_TEST = "LAB_TEST", "Lab Test"
        PROCEDURE = "PROCEDURE", "Procedure"
        MEDICINE = "MEDICINE", "Medicine"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"

class Cart(models.Model):
    patient = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart for {self.patient.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('DELIVERED', 'Delivered'),
        ],
        default='PENDING'
    )

    def __str__(self):
        return f"Order by {self.patient.email} on {self.payment_date}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order"
    

class MessageRequest(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='message_requests_sent')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='message_requests_received')
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('ACCEPTED', 'Accepted'),
            ('REJECTED', 'Rejected'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient'],
                condition=models.Q(status='PENDING'),
                name='unique_pending_message_request_per_patient'
            )
        ]

    def __str__(self):
        return f"Message request from {self.patient.email} to {self.doctor.full_name} - {self.status}"

class ChatMessage(models.Model):
    message_request = models.ForeignKey(MessageRequest, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.timestamp}"
    

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    prescription_text = models.TextField()
    recommended_tests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment}"
    

class ServiceProvided(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='services_received')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='services_provided')
    appointment_type = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    prescription_text = models.TextField()
    recommended_tests = models.TextField(blank=True, null=True)
    consultation_link = models.URLField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)  # 1 to 5 stars
    review = models.TextField(blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Service for {self.patient.username} by {self.doctor.full_name} on {self.date} at {self.time}"
    
class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('MONDAY', 'Monday'),
            ('TUESDAY', 'Tuesday'),
            ('WEDNESDAY', 'Wednesday'),
            ('THURSDAY', 'Thursday'),
            ('FRIDAY', 'Friday'),
            ('SATURDAY', 'Saturday'),
            ('SUNDAY', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doctor.full_name} - {self.day_of_week} from {self.start_time} to {self.end_time}"