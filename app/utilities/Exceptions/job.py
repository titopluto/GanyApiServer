class JobError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)


class JobOverlapError(JobError):
    """ A new job overlaps an existing one"""

    def __init__(self, jobs, duration, msg):
        JobError.__init__(self, msg)
        self.jobs = jobs
        self.duration = duration

class JobOnRecessError(JobError):
    """ A new job is being  attempted to be scheduled
    on a user's Recess time"""

    def __init__(self, jobs, duration, msg):
        JobError.__init__(self, msg)
        self.jobs = jobs
        self.duration = duration


class JobUnknownError(JobError):
    """ A new job is being  attempted to be scheduled
    on a user's Recess time"""

    def __init__(self, msg):
        JobError.__init__(self, msg)

