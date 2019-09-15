from django.db import models
from django.contrib.auth import get_user_model


class JobManager(models.Manager):
    def _create_new_job(self, creator, executor, price, start, end, **extra_fields):
        """helper to create a new job model"""
        if creator == executor:
            raise ValueError("You cannot assign a job to yourself")
        if start >= end:
            raise ValueError(
                "The End time should be greater than the Start time")

        job = self.model(
            creator=creator,
            executor=executor,
            price=price,
            start=start,
            end=end,
            **extra_fields
        )
        job.save(using=self._db)
        return job

    def create(self, creator, executor, price, start, end, **extra_fields):
        """ creates a new job"""
        return self._create_new_job(creator, executor,
                                    price, start, end,
                                    **extra_fields)


class Job(models.Model):
    creator = models.ForeignKey(get_user_model(), related_name='creator', on_delete=models.CASCADE)
    executor = models.ForeignKey(get_user_model(), related_name='executor', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()
    comment = models.TextField(blank=True)
    job_status = models.CharField(max_length=20, default="incomplete")
    payment_status = models.CharField(max_length=20, default="pending")

    objects = JobManager()




