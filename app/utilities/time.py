import collections


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


def timeslot_continuity_check(qs):
    """ To check if a  queryset of DTrange objects are continuous"""
    if not isinstance(qs, collections.abc.Iterable):
        raise ValueError("Argument must be an Iterable")
    if not qs.exists():
        return False
    cue = qs[0].period.lower
    for item in qs:
        if cue == item.period.lower:
            cue = item.period.upper
            continue
        else:
            return False
    return True
