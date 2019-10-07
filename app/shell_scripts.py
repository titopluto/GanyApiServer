import datetime
import collections
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from psycopg2.extras import DateTimeTZRange
from timeslot.models import TimeSlot


def sample_time(start=None):
    if not start:
        start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
    end = start + datetime.timedelta(hours=4)
    return (start, end)


def sample_duration(start=None):
    """ creates a start-time and end-time with a difference
        of 4 hours
    :return a tuple
    """
    if not start:
        start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
    end = start + datetime.timedelta(hours=4)  # 16
    return DateTimeTZRange(start, end)


def sample_user(email='tito@pluto.com'):
    '''helper to create a sample user'''
    user = get_user_model().objects.create_user(
        email=email,
        password='testpass'
    )
    return user


# creator = sample_user()
User = get_user_model()
tito = User.objects.get(email='tito@pluto.com')
time_start, time_end = sample_time()
duration = DateTimeTZRange(time_start, time_end)

timeslot_kwargs = dict(
    creator=tito,
    duration=duration,
    comment='i am available for good price'
)

timeslot = TimeSlot.objects.create(**timeslot_kwargs)


def sequence_continuity(seq):
    """ To check if a  sequence of a 2 tuple item is continuous"""
    if not isinstance(seq, collections.abc.Iterable):
        raise ValueError("Argument must be an Iterable")
    cue = seq[0][0]
    for item in seq:
        if cue == item[0]:
            cue = item[1]
            continue
        else:
            return False
    return True


def timeslot_continuity_check(seq):
    """ To check if a  sequence of a 2 tuple item is continuous"""
    if not isinstance(seq, collections.abc.Iterable):
        raise ValueError("Argument must be an Iterable")
    cue = seq[0].period.lower
    for item in seq:
        if cue == item.period.lower:
            cue = item.period.upper
            continue
        else:
            return False
    return True
