from django.db import models
from django.conf import settings

class TimeSlotManager(models.Manager):
    def _create_new_slot(self, creator, start, end, **extra_fields):
        """helper to create a new time slot"""

        slot = self.model(
            creator=creator,
            start=start,
            end=end,
            **extra_fields
        )
        slot.save(using=self._db)
        return slot

    def create(self, creator, start, end, **extra_fields):
        """ creates a new job"""
        return self._create_new_slot(creator,start, end, **extra_fields)


class TimeSlot(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='timeslots', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    comment = models.TextField(blank=True)

    objects = TimeSlotManager()
