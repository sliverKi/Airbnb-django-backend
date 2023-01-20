from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "room",
        "kind",
        "guests",
        "experience",
        "check_in",
        "check_out",
        "experience_time",
    )
    list_filter = ("kind",)
