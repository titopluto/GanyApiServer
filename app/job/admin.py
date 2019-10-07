from django.contrib import admin
from .models import Job


# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'creator', 'executor', 'price',
        'type', 'duration', 'job_status',
        'payment_status'
    ]

    class meta:
        model = Job


admin.site.register(Job, JobAdmin)
