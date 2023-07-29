from django.contrib import admin
from .models import Building, Elevator, Request

admin.site.register((Building, Elevator, Request))
