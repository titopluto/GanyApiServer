from django.db import models
from django.contrib.postgres.fields import DateTimeRangeField
from django.conf import settings

from utilities.Exceptions.timeslot import *


class TimeSlotManager(models.Manager):

    def _create_new_slot(self, creator, period, **extra_fields):
        """helper to create a new time slot"""

        # check if overlap exist with existing time slot
        timeslot_qs = self.model.objects.filter(period__overlap=period)
        if timeslot_qs.exists():
            raise TimeSlotsOverlapError(timeslot_qs,
                                        "The time slot overlaps with an existing "
                                        "time slot")

        # check if start time is greater than end time
        if period.lower >= period.upper:
            raise ValueError(
                "The End time should be greater than the Start time"
            )
        slot = self.model(
            creator=creator,
            period=period,
            **extra_fields
        )
        slot.save(using=self._db)
        return slot

    def create(self, creator, period, **extra_fields):
        """ creates a new time slot"""
        slot = self._create_new_slot(creator, period, **extra_fields)
        creator.timesheet.add(slot)
        return slot


class TimeSlot(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                related_name='timeslots',
                                on_delete=models.CASCADE)
    period = DateTimeRangeField(unique=True)
    comment = models.TextField(blank=True)

    objects = TimeSlotManager()

    def __str__(self):
        return f'{self.creator} @ {self.period}'
