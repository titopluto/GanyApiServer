from django.db import models
from django.contrib.auth import get_user_model
from job.models import Job

class ReviewManager(models.Manager):
    def _create_new_review(self, creator, executor, job, rating, **extra_fields):
        """helper to create a new job model"""
        if creator != job.creator:
            raise ValueError("You can only review a job you assigned")
        if  executor != job.executor:
            raise ValueError("The review executor must match with the job executor")

        review = self.model(
            creator=creator,
            executor=executor,
            job=job,
            rating=rating,
            **extra_fields
        )
        review.save(using=self._db)
        return review

    def create(self, creator, executor, job, rating, **extra_fields):
        """ creates a new job"""
        return self._create_new_review(creator, executor,
                                   job, rating, **extra_fields)

class Review(models.Model):
    creator = models.ForeignKey(get_user_model(), related_name='review_creator', on_delete=models.CASCADE)
    executor = models.ForeignKey(get_user_model(), related_name='review_executor', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='reviewed_job', on_delete=models.CASCADE)
    rating = models.IntegerField()
    note = models.CharField(max_length=255, blank=True)

    objects = ReviewManager()