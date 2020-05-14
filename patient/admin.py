from django.contrib import admin
from .models import Patient, Appointment, Chat, Chatdb
# Register your models here.

admin.site.register(Patient)

admin.site.register(Appointment)

admin.site.register(Chat)

admin.site.register(Chatdb)
