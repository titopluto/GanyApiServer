import datetime

from django.test import TestCase
from django.utils.timezone import make_aware

from psycopg2.extras import DateTimeTZRange

from job.models import Job

from utilities import samples
from utilities.Exceptions.job import *
from utilities.Exceptions.timeslot import *


class JobModelTests(TestCase):

    # Job Tests

    def test_executor_with_job_in_range_cannot_create(self):
        """ To check that an executor that has a job already in the
        new job range cannot create a new job in that range
        e.g ==> Existing job: 12-16
                Recess time: 16-15
                New job request: 12-13
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        # create time slot and  sample job at
        #  ==> 2019, 12, 27, 12, 0
        samples.sample_job(creator, executor)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        job_end = job_start + datetime.timedelta(hours=2)  # 14
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(JobOverlapError):
            Job.objects.create(**job_kwargs)

    def test_executor_cannot_create_job_in_recess(self):
        """ To check that an executor cannot create a new job in
        a recess time period
        e.g ==> Existing job: 12-16
                Recess time: 16-15
                New job request: 16-18
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        # create time slot and  sample job at
        #  ==> 2019, 12, 27, 12, 0
        time_start= datetime.datetime(2019, 12, 27, 12, 0)
        time_end = time_start + datetime.timedelta(hours=6)  # 18
        t = samples.sample_timeslot(executor, time_start, time_end)

        # create job on timeslot
        job_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        job_end = job_start + datetime.timedelta(hours=4)  # 16
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        Job.objects.create(**job_kwargs)

        #create new job on a recess time
        job_start = make_aware(datetime.datetime(2019, 12, 27, 16, 0))
        job_end = job_start + datetime.timedelta(hours=2)  # 17
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='test',
            price=30.05,
        )
        with self.assertRaises(JobOnRecessError):
            Job.objects.create(**job_kwargs)

    # Timeslot Tests
    def test_executor_with_no_timeslot_cannot_create_job(self):
        """ To check that the executor of job has a
        timeslot valid before job is created
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        job_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        job_end = job_start + datetime.timedelta(hours=3)  # 15
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        # expect an error
        with self.assertRaises(TimeSlotsNotFound):
            Job.objects.create(**job_kwargs)

    def test_create_job_user_with_invalid_timeslot_not_successful(self):
        """ Test to create a new job  in which  user has
         DOES NOT have a valid timeslot that matches the
        duration of the job
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        timeslot_end = timeslot_start + datetime.timedelta(hours=4)  # 16
        timeslot_period = DateTimeTZRange(timeslot_start, timeslot_end)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 10, 0))
        job_end = job_start + datetime.timedelta(hours=2)  # 12
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a time slot for the executor
        samples.sample_timeslot(executor, period=timeslot_period)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(TimeSlotsJobMatchError):
            Job.objects.create(**job_kwargs)

    def test_job_creator_executor_not_equal(self):
        """ Test to check that the creator and executor
        of a job entry is not equal to the same user
        """
        creator = samples.sample_user()
        job_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        job_end = job_start + datetime.timedelta(hours=3)  # 15
        job_duration = DateTimeTZRange(job_start, job_end)

        job_kwargs = dict(
            creator=creator,
            executor=creator,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(ValueError):
            Job.objects.create(**job_kwargs)

    def test_job_duration_check(self):
        """ To check that a job start time is greater than
        its end time
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')
        start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        end = make_aware(datetime.datetime(2019, 12, 27, 11, 0))  # -1
        duration = DateTimeTZRange(start, end)

        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=duration,
            type='turnover',
            price=30.05,
        )

        with self.assertRaises(ValueError):
            Job.objects.create(**job_kwargs)

    def test_create_new_job_successful(self):
        """ Test to create a new job  in which  user has
         a valid timeslot that matches the
        duration of the job
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        timeslot_end = timeslot_start + datetime.timedelta(hours=4)
        timeslot_period = DateTimeTZRange(timeslot_start, timeslot_end)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        job_end = job_start + datetime.timedelta(hours=3)
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a time slot for the executor
        samples.sample_timeslot(executor, period=timeslot_period)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        job = Job.objects.create(**job_kwargs)

        self.assertEqual(job.creator, job_kwargs['creator'])
        self.assertEqual(job.executor, job_kwargs['executor'])
        self.assertEqual(job.duration, job_kwargs['duration'])
        self.assertEqual(Job.objects.all().count(), 1)

    def test_create_new_job_successful2(self):
        """ Test to create a new job  in which  user has
           valid timeslots in different time ranges
          e.g ==> 12-16 and 19-23
          Job duration ==> 13-16
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start1 = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        timeslot_end1 = timeslot_start1 + datetime.timedelta(hours=4)  # 16
        timeslot_period1 = DateTimeTZRange(timeslot_start1, timeslot_end1)

        timeslot_start2 = make_aware(datetime.datetime(2019, 12, 27, 19, 0))
        timeslot_end2 = timeslot_start2 + datetime.timedelta(hours=4)  # 23
        timeslot_period2 = DateTimeTZRange(timeslot_start2, timeslot_end2)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 13, 0))
        job_end = job_start + datetime.timedelta(hours=3)
        job_duration = DateTimeTZRange(job_start, job_end)

        # create a time slot for the executor
        samples.sample_timeslot(executor, period=timeslot_period1)
        samples.sample_timeslot(executor, period=timeslot_period2)

        # create a job within the duration
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        job = Job.objects.create(**job_kwargs)

        self.assertEqual(job.creator, job_kwargs['creator'])
        self.assertEqual(job.executor, job_kwargs['executor'])
        self.assertEqual(job.duration, job_kwargs['duration'])
        self.assertEqual(Job.objects.all().count(), 1)

    def test_create_new_job_successful3(self):
        """ Test to create a new job  in which  user has
          have a valid timeslots that are continuous
          e.g ==> 12-4 and 4-8
          and job time overlaps between the timeslots
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start1 = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        timeslot_end1 = timeslot_start1 + datetime.timedelta(hours=4)  # 16
        timeslot_period1 = DateTimeTZRange(timeslot_start1, timeslot_end1)

        timeslot_start2 = make_aware(datetime.datetime(2019, 12, 27, 16, 0))
        timeslot_end2 = timeslot_start2 + datetime.timedelta(hours=4)  # 20
        timeslot_period2 = DateTimeTZRange(timeslot_start2, timeslot_end2)

        # offset timeslot (not in job duration range)
        timeslot_start3 = make_aware(datetime.datetime(2019, 12, 27, 8, 0))
        timeslot_end3 = timeslot_start3 + datetime.timedelta(hours=3)  # 11
        timeslot_period3 = DateTimeTZRange(timeslot_start3, timeslot_end3)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 14, 0))
        job_end = job_start + datetime.timedelta(hours=18)  # 18
        job_duration = DateTimeTZRange(job_start, job_end)

        # create  timeslots for the executor
        samples.sample_timeslot(executor, period=timeslot_period1)
        samples.sample_timeslot(executor, period=timeslot_period2)
        samples.sample_timeslot(executor, period=timeslot_period3)

        # create a job with start time end time out of the
        # executor's time slot
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        job = Job.objects.create(**job_kwargs)

        self.assertEqual(job.creator, job_kwargs['creator'])
        self.assertEqual(job.executor, job_kwargs['executor'])
        self.assertEqual(job.duration, job_kwargs['duration'])
        self.assertEqual(Job.objects.all().count(), 1)

    def test_create_job_non_continuous_timeslot_unsuccessful(self):
        """ Test to create a new job  in which  user has
          have a valid 2 timeslots that are not continuous
          e.g ==> 12-16 and 17-21
          and job time overlaps between the timeslots
          e.g ==> 15-18
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start1 = make_aware(datetime.datetime(2019, 12, 27, 12, 0))
        timeslot_end1 = timeslot_start1 + datetime.timedelta(hours=4)  # 16
        timeslot_period1 = DateTimeTZRange(timeslot_start1, timeslot_end1)

        timeslot_start2 = make_aware(datetime.datetime(2019, 12, 27, 17, 0))
        timeslot_end2 = timeslot_start2 + datetime.timedelta(hours=4)  # 21
        timeslot_period2 = DateTimeTZRange(timeslot_start2, timeslot_end2)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 15, 0))
        job_end = job_start + datetime.timedelta(hours=3)  # 18
        job_duration = DateTimeTZRange(job_start, job_end)

        # create  timeslots for the executor
        samples.sample_timeslot(executor, period=timeslot_period1)
        samples.sample_timeslot(executor, period=timeslot_period2)

        # create a job with start time/ end time out of
        # the executor's time slot
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(TimeSlotsNotContinuousError):
            Job.objects.create(**job_kwargs)

    def test_create_job_non_continuous_timeslot_unsuccessful2(self):
        """ Test to create a new job  in which  user has
          have a valid 3 timeslots that are not continuous
          e.g ==> 11-12 and 13-15 and 15-18
          and job time overlaps between the timeslots
          e.g ==> 11-17
        """
        creator = samples.sample_user()
        executor = samples.sample_user(email='tito123@pluto.com')

        timeslot_start1 = make_aware(datetime.datetime(2019, 12, 27, 11, 0))
        timeslot_end1 = timeslot_start1 + datetime.timedelta(hours=1)  # 12
        timeslot_period1 = DateTimeTZRange(timeslot_start1, timeslot_end1)

        timeslot_start2 = make_aware(datetime.datetime(2019, 12, 27, 13, 0))
        timeslot_end2 = timeslot_start2 + datetime.timedelta(hours=2)  # 15
        timeslot_period2 = DateTimeTZRange(timeslot_start2, timeslot_end2)

        timeslot_start3 = make_aware(datetime.datetime(2019, 12, 27, 15, 0))
        timeslot_end3 = timeslot_start3 + datetime.timedelta(hours=3)  # 18
        timeslot_period3 = DateTimeTZRange(timeslot_start3, timeslot_end3)

        job_start = make_aware(datetime.datetime(2019, 12, 27, 11, 0))
        job_end = job_start + datetime.timedelta(hours=6)  # 17
        job_duration = DateTimeTZRange(job_start, job_end)

        # create  timeslots for the executor
        samples.sample_timeslot(executor, period=timeslot_period1)
        samples.sample_timeslot(executor, period=timeslot_period2)
        samples.sample_timeslot(executor, period=timeslot_period3)

        # create a job with start time/ end time out of the
        # executor's time slot
        job_kwargs = dict(
            creator=creator,
            executor=executor,
            duration=job_duration,
            type='turnover',
            price=30.05,
        )
        with self.assertRaises(TimeSlotsNotContinuousError):
            Job.objects.create(**job_kwargs)
