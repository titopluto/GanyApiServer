import datetime

from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

from psycopg2.extras import DateTimeTZRange

from job.models import Job
from timeslot.models import TimeSlot


def sample_user(email='tito@pluto.com'):
    '''helper to create a sample user'''
    user = get_user_model().objects.create_user(
        email=email,
        password='testpass'
    )
    return user


def sample_time(start=datetime.datetime(2019, 12, 27, 12, 0), delta=4):
    """ creates a start-time and end-time with a difference
        of 4 hours
    :return a tuple
    """
    start = make_aware(start)
    end = start + datetime.timedelta(hours=delta)
    return (start, end)


def sample_duration(start=datetime.datetime(2019, 12, 27, 12, 0), delta=4):
    """ creates a start-time and end-time with a difference
        of 4 hours
    :return a tuple
    """
    start = make_aware(start)
    end = start + datetime.timedelta(hours=delta)  # 16
    return DateTimeTZRange(start, end)


def sample_timeslot(creator, start=None, end=None, period=None):
    """ helper to create a new time slot with in a period"""
    if not start and not end and not period:
        time_start, time_end = sample_time()
        period = DateTimeTZRange(time_start, time_end)
    if start and end and not period:
        period = DateTimeTZRange(make_aware(start), make_aware(end))

    timeslot_kwargs = dict(
        creator=creator,
        period=period,
        comment='i am available for good price'
    )
    return TimeSlot.objects.create(**timeslot_kwargs)


def sample_job(creator, executor):
    """creates a sample job instance"""
    duration = sample_duration()
    sample_timeslot(executor, period=duration)
    job_kwargs = dict(
        creator=creator,
        executor=executor,
        duration=duration,
        type='turnover',
        price=30.05,
    )
    return Job.objects.create(**job_kwargs)
