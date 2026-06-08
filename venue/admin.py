from django.contrib import admin
from .models import Booking, UserProfile, ContactMessage
# Register your models here.


admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(ContactMessage)