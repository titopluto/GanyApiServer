class TimeSlotError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)


class TimeSlotsNotFound(TimeSlotError):
    """ No timeslot found for a user """

    def __init__(self, count, msg):
        TimeSlotError.__init__(self, msg)
        self.count = count


class TimeSlotsNotContinuousError(TimeSlotError):
    """ A group of timeslot does have a continuous
    range """

    def __init__(self, timeslots, msg):
        TimeSlotError.__init__(self, msg)
        self.timeslots = timeslots


class TimeSlotsJobMatchError(TimeSlotError):
    """ The job durations does match the existing timeslot
    a user has"""

    def __init__(self, timeslots, msg):
        TimeSlotError.__init__(self, msg)
        self.timeslots = timeslots


class TimeSlotsOverlapError(TimeSlotError):
    """ a new timeslot overlaps on an existing one"""

    def __init__(self, timeslots, msg):
        TimeSlotError.__init__(self, msg)
        self.timeslots = timeslots