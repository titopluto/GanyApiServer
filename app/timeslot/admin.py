from django.contrib import admin
from .models import TimeSlot


# Register your models here.
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['creator', 'period', 'comment']

    class meta:
        model = TimeSlot


admin.site.register(TimeSlot, TimeSlotAdmin)
