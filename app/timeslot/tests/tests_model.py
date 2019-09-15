from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from timeslot.models import TimeSlot

from review.models import Review

def sample_user(email='tito@pluto.com'):
    '''helper to create a sample user'''
    user = get_user_model().objects.create_user(
        email=email,
        password='testpass'
    )
    return user

def sample_time():
    """ creates a start-time and end-time with a difference
        of 4 hours
    :return a tuple
    """
    start = timezone.now()
    time_delta = timezone.timedelta(hours=2)
    end = start + time_delta

    return (start, end)



class TimeSheetModelTests(TestCase):

    def test_create_new_timesheet_successful(self):
        """ Test to create a new review"""
        creator = sample_user()
        time_start, time_end = sample_time()

        timeslot_kwargs = dict(
            creator=creator,
            start=time_start,
            end=time_end,
            comment = 'i am available for good price'
        )
        timeslot = TimeSlot.objects.create(**timeslot_kwargs)

        self.assertEqual(timeslot.creator, timeslot_kwargs['creator'])
        self.assertEqual(TimeSlot.objects.all().count(), 1)
