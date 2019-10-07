import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from psycopg2.extras import DateTimeTZRange

from timeslot.models import TimeSlot

from utilities import samples
from utilities.Exceptions.timeslot import *


class TimeSheetModelTests(TestCase):

    def test_create_new_timeslot_successful(self):
        """ Test to create a new timeslot"""
        creator = samples.sample_user()
        time_start, time_end = samples.sample_time()
        period = DateTimeTZRange(time_start, time_end)

        timeslot_kwargs = dict(
            creator=creator,
            period=period,
            comment='i am available for good price'
        )

        timeslot = TimeSlot.objects.create(**timeslot_kwargs)

        self.assertEqual(timeslot.creator, timeslot_kwargs['creator'])
        self.assertEqual(timeslot.period, timeslot_kwargs['period'])
        self.assertEqual(TimeSlot.objects.all().count(), 1)

    def test_timeslot_start_greater_than_end(self):
        """ To check that a job start time is greater than
        its end time
        """
        start = samples.sample_time()[0]
        job_kwargs = dict(
            creator=samples.sample_user(),
            period=DateTimeTZRange(start, start)
        )
        with self.assertRaises(ValueError):
            TimeSlot.objects.create(**job_kwargs)

    def test_timeslots_dont_overlap(self):
        """ To check that two saved time slots do not
        overlap
        """
        creator = samples.sample_user()
        start1 = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        end1 = start1 + datetime.timedelta(hours=4)  # 16
        start2 = make_aware(datetime.datetime(2019, 12, 27, 14, 0))
        end2 = start2 + datetime.timedelta(hours=4)  # 18

        # create first time slot
        TimeSlot.objects.create(
            creator=creator,
            period=DateTimeTZRange(start1, end1)
        )

        # create second time slot and expert error
        with self.assertRaises(TimeSlotsOverlapError):
            TimeSlot.objects.create(
                creator=creator,
                period=DateTimeTZRange(start2, end2)
            )
