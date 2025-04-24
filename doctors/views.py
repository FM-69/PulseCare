from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Role
# # from .models import BookingRequest, Availability
# from django.utils import timezone

# @login_required
# def doctor_dashboard(request):
#     if request.user.profile.role != Role.DOCTOR:
#         return redirect('login')
#     bookings = BookingRequest.objects.filter(doctor=request.user.doctor)
#     availabilities = Availability.objects.filter(doctor=request.user.doctor, end_time__gte=timezone.now())
#     return render(request, 'doctors/dashboard.html', {
#         'bookings': bookings,
#         'availabilities': availabilities
#     })

# @login_required
# def manage_availability(request):
#     if request.user.profile.role != Role.DOCTOR:
#         return redirect('login')
#     if request.method == 'POST':
#         start_time = request.POST.get('start_time')
#         end_time = request.POST.get('end_time')
#         Availability.objects.create(
#             doctor=request.user.doctor,
#             start_time=start_time,
#             end_time=end_time
#         )
#         return redirect('doctor_dashboard')
#     return render(request, 'doctors/manage_availability.html')