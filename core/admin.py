from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Specialty)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(MedicalCompany)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)