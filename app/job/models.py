import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models

from utilities.time import timeslot_continuity_check
from utilities.Exceptions.job import *
from utilities.Exceptions.timeslot import *
from .constants import RECESS_HOUR

from psycopg2.extras import DateTimeTZRange


class JobManager(models.Manager):

    def _create_new_job(self, creator, executor,
                        price, duration, **extra_fields):
        """helper to create a new job model"""
        if creator == executor:
            raise ValueError("You cannot assign a job to yourself")
        if duration.lower >= duration.upper:
            raise ValueError(
                "The End time should be greater than the Start time")

        #check if executor has existing job
        jobs_qs = self.model.objects.filter(duration__overlap=duration)
        recess_qs = self.model.objects.filter(recess__overlap=duration)

        if recess_qs:
            raise JobOnRecessError(jobs_qs,
                                  duration,
                                  "You cannot create a job on Executor's recess time")

        if jobs_qs.exists():
            raise JobOverlapError(jobs_qs,
                                  duration,
                                  "Executor has a job that overlaps this duration")

        # Check if executor has a time slot in the range of start and end
        time_slots = executor.timesheet.all()
        time_slots_count = time_slots.count()

        if extra_fields.get('type', None) == 'test':
            print(executor.timesheet.filter(period__contains=duration))
            print(duration)
            print(executor.timesheet.all())

        if time_slots_count == 0:
            raise TimeSlotsNotFound(time_slots_count,
                                    "Executor has no time slots available")

        timeslot_qs = executor.timesheet.filter(period__overlap=duration)
        if timeslot_qs.count() == 1:
            timeslot_qs_c = executor.timesheet.filter(period__contains=duration)
            if timeslot_qs_c.exists():
                job = self.model(
                    creator=creator,
                    executor=executor,
                    price=price,
                    duration=duration,
                    **extra_fields
                )
                job.save(using=self._db)
                return job
            else:
                raise TimeSlotsJobMatchError(timeslot_qs,
                                             "Executor has no time slots that matches the "
                                             "requested job")
        elif timeslot_qs.count() > 1:
            continuity_check = timeslot_continuity_check(timeslot_qs)
            if continuity_check:
                job = self.model(
                    creator=creator,
                    executor=executor,
                    price=price,
                    duration=duration,
                    **extra_fields
                )
                job.save(using=self._db)
                return job
            else:
                raise TimeSlotsNotContinuousError(timeslot_qs,
                                             "Executor has timeslots that is not continuous")
        else:
            raise TimeSlotsJobMatchError(timeslot_qs,
                                         "Executor has no time slots that matches the "
                                         "requested job")

    def create(self, creator, executor,
               price, duration, **extra_fields):
        """ creates a new job"""
        return self._create_new_job(creator, executor,
                                    price, duration,
                                    **extra_fields)


class Job(models.Model):

    creator = models.ForeignKey(get_user_model(),
                                related_name='creator',
                                on_delete=models.CASCADE)
    executor = models.ForeignKey(get_user_model(),
                                 related_name='executor',
                                 on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=20)
    duration = DateTimeRangeField(unique=True)
    recess = DateTimeRangeField(blank=True)
    comment = models.TextField(null=True, blank=True)
    job_status = models.CharField(max_length=20, default="incomplete")
    payment_status = models.CharField(max_length=20, default="pending")

    objects = JobManager()

    def save(self, *args, **kwargs):

        recess_lower = self.duration.upper
        recess_upper = self.duration.upper + datetime.timedelta(hours=RECESS_HOUR)
        recess_range = DateTimeTZRange(recess_lower, recess_upper)
        self.recess = recess_range

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Job for {self.creator} @ {self.duration}'
