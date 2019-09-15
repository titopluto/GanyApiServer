from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from job.models import Job



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

def sample_job():
    """creates a sample job instance"""
    job_kwargs = dict(
        creator=sample_user(),
        executor=sample_user(email='tito123@pluto.com'),
        start=sample_time()[0],
        end=sample_time()[1],
        type='turnover',
        price=30.05,
    )
    return Job.objects.create(**job_kwargs)


class JobModelTests(TestCase):

    def test_create_new_job_successful(self):
        """ Test to create a new job"""
        time_start, time_end = sample_time()
        job_kwargs = dict(
            creator=sample_user(),
            executor = sample_user(email='tito123@pluto.com'),
            start = time_start,
            end = time_end,
            type = 'turnover',
            price = 30.05,
        )
        job = Job.objects.create(**job_kwargs)

        self.assertEqual(job.creator, job_kwargs['creator'])
        self.assertEqual(job.executor, job_kwargs['executor'])
        self.assertEqual(Job.objects.all().count(), 1)

    def test_job_creator_assigner_not_equal(self):
        """ Test to check that the creator and assigner
        of a job entry is not eqaul to the same user
        """
        creator = sample_user()
        job_kwargs = dict(
            creator=creator,
            executor=creator,
            start=sample_time()[0],
            end=sample_time()[1],
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(ValueError):
            Job.objects.create(**job_kwargs)

        self.assertEqual(Job.objects.all().count(), 0)

    def test_job_start_greater_than_end(self):
        """ To check that a job start time is greater than
        its end time
        """
        start = sample_time()[0]
        job_kwargs = dict(
            creator=sample_user(),
            executor=sample_user(email='tito123@pluto.com'),
            start=start,
            end=start,
            type='turnover',
            price=30.05,
        )

        with self.assertRaises(ValueError):
            Job.objects.create(**job_kwargs)