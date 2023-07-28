from django.contrib import admin
from .models import Building, Elevator, Floor, Request

admin.site.register((Building, Elevator, Floor, Request))
