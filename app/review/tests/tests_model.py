from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from job.models import Job

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

def sample_job(creator, executor):
    time_start, time_end = sample_time()
    job_kwargs = dict(
        creator=creator,
        executor=executor,
        start=time_start,
        end=time_end,
        type='turnover',
        price=30.05,
    )
    return Job.objects.create(**job_kwargs)


class ReviewModelTests(TestCase):

    def test_create_new_review_successful(self):
        """ Test to create a new review"""
        creator = sample_user()
        executor = sample_user(email='tito123@pluto.com')
        job = sample_job(creator, executor)

        review_kwargs = dict(
            creator= creator,
            executor = executor,
            job = job,
            rating = 5,
            note = "excellent!"
        )
        review = Review.objects.create(**review_kwargs)

        self.assertEqual(review.creator, review_kwargs['creator'])
        self.assertEqual(review.executor, review_kwargs['executor'])
        self.assertEqual(Review.objects.all().count(), 1)

    def test_review_job_details_concurrent(self):
        """ Test to make sure the review creator/executor match
        the job creator/executor
        """
        creator = sample_user()
        executor = sample_user(email='tito123@pluto.com')
        creator2 = sample_user(email='james@pluto.com')
        executor2 = sample_user(email='tim@pluto.com')

        job = sample_job(creator2, executor2)

        review_kwargs = dict(
            creator=creator,
            executor=executor,
            job=job,
            rating=5,
            note="excellent!"
        )

        with self.assertRaises(ValueError):
            review = Review.objects.create(**review_kwargs)
