from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='index'),
    path("", views.UserLogoutView.as_view(), name="logout"),

    # New URLs for selecting signup/login roles
    path('signup/', views.SelectSignupView.as_view(), name='select_signup'),
    path('login/', views.SelectLoginView.as_view(), name='select_login'),

    path("patient-signup/", views.PatientSignUpView.as_view(), name="patient_signup"),
    path("doctor-signup/", views.DoctorSignUpView.as_view(), name="doctor_signup"),

    path("patient-login/", views.PatientLoginView.as_view(), name="patient_login"),
    path("doctor-login/", views.DoctorLoginView.as_view(), name="doctor_login"),

    path('patients/dashboard/', views.PatientDashboardView.as_view(), name='patient_dashboard'),
    path('doctors/dashboard/', views.DoctorDashboardView.as_view(), name='doctor_dashboard'),

    path('doctors/profile/', views.DoctorProfileView.as_view(), name='doctor_profile'),
    path('doctors/edit-profile/', views.DoctorEditProfileView.as_view(), name='doctor_edit_profile'),

    path("patient_home/", views.patient_home, name="patient_home"),
    path("doctor_home/", views.doctor_home, name="doctor_home"),
   

    path('all_doctors/', views.DoctorsListView.as_view(), name='doctors_list'),

    path('doctors/<int:doctor_id>/', views.DoctorDetailView.as_view(), name='doctor_detail'),

    path('doctors/<int:doctor_id>/schedule/', views.ScheduleAppointmentView.as_view(), name='schedule_appointment'),

    path('doctors/availability/', views.DoctorAvailabilityView.as_view(), name='doctor_availability'),

    path('payment/', views.PaymentView.as_view(), name='payment'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/remove/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

    path('doctor/patients/', views.DoctorPatientListView.as_view(), name='patient_list'),

    path('doctor/patient/<int:patient_id>/', views.PatientDetailView.as_view(), name='patient_detail'),  # Add this

    path('doctor/appointments/', views.DoctorAppointmentsView.as_view(), name='doctor_appointments'),
    path('doctor/payments/', views.DoctorPaymentsView.as_view(), name='doctor_payments'),

    path('patient/profile/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('patient/edit-profile/', views.PatientEditProfileView.as_view(), name='patient_edit_profile'),

    path('send-message-request/', views.SendMessageRequestView.as_view(), name='send_message_request'),
    # path('respond-message-request/', views.RespondMessageRequestView.as_view(), name='respond_message_request'),
    path('chat/<int:message_request_id>/', views.ChatView.as_view(), name='chat'),

    path("message_requests/", views.message_request, name="message_request"),

    path('respond-message-request/<int:message_request_id>/', views.RespondMessageRequestView.as_view(), name='respond_message_request'),

    path('doctor/appointment/<int:appointment_id>/add-link/', views.AddAppointmentLinkView.as_view(), name='add_appointment_link'),
    path('doctor/appointment/<int:appointment_id>/edit-link/', views.   EditAppointmentLinkView.as_view(), name='edit_appointment_link'),
]