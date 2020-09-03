import time
import datetime
import numpy as np

MINUTE = 60.
HOUR = 60. * MINUTE
DAY = 24. * HOUR
YEAR = 365.25 * DAY
WEEK = 7. * DAY


class UTC(datetime.datetime):

    def __new__(cls, year=1970, month=1, day=1,
                hour=0, minute=0, second=0, microsecond=0):

        self = super(UTC, cls).__new__(
            cls, year=year, month=month, day=day,
            hour=hour, minute=minute,
            second=second, microsecond=microsecond,
            tzinfo=datetime.timezone.utc)
        return self

    def __getstate__(self):
        return {"year": self.year,
                "month": self.month,
                "day": self.day,
                "hour": self.hour,
                "minute": self.minute,
                "second": self.second,
                "microsecond": self.microsecond}

    def __str__(self):
        return f'{self.year:04d}-{self.month:02d}-{self.day:02d}T' \
               f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}.{self.microsecond:06d}Z'

    @property
    def timestamp(self):
        return datetime.datetime.timestamp(self)

    def __float__(self):
        return self.timestamp

    @property
    def weekday(self):
        # 0 = Monday
        return datetime.datetime.weekday(self)

    @property
    def julday(self):
        from obspy.core import UTCDateTime

        timedelta = (self - self.flooryear)
        julday = int(np.floor(timedelta.total_seconds() / DAY))
        print(self, str(UTCDateTime(self.timestamp)))
        print(UTCDateTime(self.timestamp).julday, julday + 1)
        return julday + 1

    @property
    def flooryear(self):
        return UTC(year=self.year, month=1, day=1,
                   hour=0, minute=0, second=0, microsecond=0)

    @property
    def ceilyear(self):
        fy = self.flooryear
        if self == fy:
            return fy
        return UTC(year=self.year+1, month=1, day=1,
                   hour=0, minute=0, second=0, microsecond=0)

    @property
    def floormonth(self):
        return UTC(year=self.year, month=self.month, day=1,
                   hour=0, minute=0, second=0, microsecond=0)

    @property
    def ceilmonth(self):
        fm = self.floormonth
        if self == fm:
            return fm
        if self.month < 12:
            return UTC(year=self.year, month=self.month+1, day=1,
                       hour=0, minute=0, second=0, microsecond=0)
        else:
            return self.ceilyear

    @property
    def floorday(self):
        return UTC(year=self.year, month=self.month, day=self.day,
                   hour=0, minute=0, second=0, microsecond=0)

    @property
    def ceilday(self):
        fd = self.floorday
        if self == fd:
            return fd
        try:
            return UTC(year=self.year, month=self.month, day=self.day+1,
                       hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            return self.ceilmonth

    @property
    def floorhour(self):
        return UTC(year=self.year, month=self.month, day=self.day,
                   hour=self.hour, minute=0, second=0, microsecond=0)

    @property
    def ceilhour(self):
        fh = self.floorhour
        if self == fh:
            return fh
        try:
            return UTC(year=self.year, month=self.month, day=self.day+1,
                       hour=self.hour+1, minute=0, second=0, microsecond=0)
        except ValueError:
            return self.ceilday

    @property
    def floorminute(self):
        return UTC(year=self.year, month=self.month, day=self.day,
                   hour=self.hour, minute=self.minute, second=0, microsecond=0)

    @property
    def ceilminute(self):
        fm = self.floorminute
        if self == fm:
            return fm
        try:
            return UTC(year=self.year, month=self.month, day=self.day+1,
                       hour=self.hour, minute=self.minute+1, second=0, microsecond=0)
        except ValueError:
            return self.ceilhour

    @property
    def floorweek(self):
        fd = self.floorday
        return UTCFromTimestamp(fd.timestamp - self.weekday * DAY)

    @property
    def ceilweek(self):
        fd = self.floorweek
        if fd == self:
            return fd
        return UTCFromTimestamp(self.timestamp + WEEK).floorweek


class UTCFromTimestamp(UTC):
    def __new__(cls, timestamp):
        d = datetime.datetime.fromtimestamp(timestamp - HOUR)   # ????
        self = super(UTCFromTimestamp, cls).__new__(
            cls, year=d.year, month=d.month, day=d.day,
            hour=d.hour, minute=d.minute,
            second=d.second, microsecond=d.microsecond)
        return self


class UTCFromStr(UTC):
    def __new__(cls, string):

        yyyymtdd, hhmnssnnnnnnZ = string.split('T')
        yyyy, mt, dd = yyyymtdd.split('-')
        hh, mn, ssnnnnnnZ = hhmnssnnnnnnZ.split(':')
        ss, nnnnnnZ = ssnnnnnnZ.split('.')
        n = nnnnnnZ.strip('Z')

        self = super(UTCFromStr, cls).__new__(
            cls,
            year=int(yyyy),
            month=int(mt),
            day=int(dd),
            hour=int(hh),
            minute=int(mn),
            second=int(ss),
            microsecond=int(n))
        return self

#
# def years_between(t1: UTC, t2: UTC, step=1) -> list:
#     """included"""
#     start = t1.ceilyear
#     end = t2.flooryear
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         return [UTC(year=y) for y in range(start.year, end.year+1, step)]
#
#
# def months_between(t1: UTC, t2: UTC, step: int=1) -> list:
#     """included"""
#     start = t1.ceilmonth
#     end = t2.floormonth
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         out = []
#         t = start
#         while t <= end:
#             out.append(t)
#             t = UTCFromTimestamp(t.timestamp + 1.).ceilmonth
#         return out[::step]
#
#
# def days_between(t1: UTC, t2: UTC, step: int=1) -> list:
#     """included"""
#     start = t1.ceilday
#     end = t2.floorday
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         out = []
#         t = start
#         while t <= end:
#             out.append(t)
#             t = UTCFromTimestamp(t.timestamp + 1.).ceilday
#         return out[::step]
#
#
# def mondays_between(t1: UTC, t2: UTC, step: int=1) -> list:
#     """included"""
#     start = t1.ceilweek
#     end = t2.floorweek
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         out = []
#         t = start
#         while t <= end:
#             out.append(t)
#             t = UTCFromTimestamp(t.timestamp + 1.).ceilweek
#         return out[::step]
#
#
# def hours_between(t1: UTC, t2: UTC, step: int=1) -> list:
#     """included"""
#     start = t1.ceilhour
#     end = t2.floorhour
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         out = []
#         t = start
#         while t <= end:
#             out.append(t)
#             t = UTCFromTimestamp(t.timestamp + 1.).ceilhour
#         return out[::step]
#
#
# def minutes_between(t1: UTC, t2: UTC, step: int=1) -> list:
#     """included"""
#     start = t1.ceilminute
#     end = t2.floorminute
#     if start > end:
#         return []
#     elif start == end:
#         return [start]
#     else:
#         out = []
#         t = start
#         while t <= end:
#             out.append(t)
#             t = UTCFromTimestamp(t.timestamp + 1.).ceilminute
#         return out[::step]

def years_between(t1: UTC, t2: UTC) -> list:
    """included"""
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')
    yearmin = t1.ceilyear.year
    yearmax = t2.flooryear.year
    if yearmin > yearmax:
        return []
    years = [UTC(y) for y in range(yearmin, yearmax + 1)]
    return years


def howmanydaysinmonth(t: UTC) -> int:
    """count days in a month
    :param t: a UTCDateTime, count the number of days in the corresponding year.month
    :return:
    """
    ndays = 32
    while True:
        try:
            out = UTC(t.year, t.month, ndays).day
            break
        except ValueError:
            ndays -= 1
    return out


def months_between(t1, t2) -> list:
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')
    if t2 - t1 > 50 * YEAR:
        raise ValueError('time period too large')
    monthmin = t1.ceilmonth
    monthmax = t2.floormonth
    if monthmin > monthmax:
        return []

    months = [monthmin]
    while months[-1] < monthmax:
        months.append(
            UTCFromTimestamp(months[-1].timestamp + howmanydaysinmonth(months[-1]) * DAY))
    print(months)
    return months


# def getmondays(utmin, utmax):
#     """
#     get all mondays between two UTCDateTimes
#     :param utmin:
#     :param utmax:
#     :return:
#     """
#     if utmin >= utmax:
#         raise ValueError('utmin must be lower than utmax')
#     weekmin = ceilweek(utmin)
#     weekmax = floorweek(utmax)
#     if weekmin > weekmax: return []
#     utweeks = [weekmin]
#     while utweeks[-1] < weekmax:
#         utweeks.append(utweeks[-1] + 7. * 24. * 3600.)
#     return utweeks


def days_between(t1, t2, step=1):
    """
    get all days between two times every daystep
    :param t1:
    :param t2:
    :param step:
    :return:
    """
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')
    if not isinstance(step, int): raise TypeError('')
    t1 = t1.ceilday
    t2 = t2.floorday
    if t1 > t2:
        return []

    daymin = UTCFromTimestamp(t1.flooryear.timestamp - DAY + step * np.ceil(t1.julday / float(step)) * DAY)
    daymax = UTCFromTimestamp(t2.flooryear.timestamp - DAY + step * np.floor(t2.julday / float(step)) * DAY)

    if daymin > daymax:
        return []
    days = [daymin]
    while True:
        next = UTCFromTimestamp(days[-1].flooryear.timestamp - DAY + step * (1 + np.floor(days[-1].julday / float(step))) * DAY)
        if next > daymax: break
        if next.year > days[-1].year:
            next = days[-1].ceilyear
        days.append(next)
    for _ in days:
        print(_)
    return days


def hours_between(t1: UTC, t2: UTC, step=1) -> list:

    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')

    if not isinstance(step, int):
        raise TypeError('hourstep is not an integer')
    t1 = t1.ceilhour
    t2 = t2.floorhour
    if t1 > t2:
        return []

    hourmin = UTCFromTimestamp(t1.floorday.timestamp + step * np.ceil(t1.hour / float(step)) * HOUR)
    hourmax = UTCFromTimestamp(t2.floorday.timestamp + step * np.floor(t2.hour / float(step)) * HOUR)

    if hourmin > hourmax:
        return []

    hours = [hourmin]
    while True:
        next = UTCFromTimestamp(hours[-1].floorday.timestamp + step * (1 + np.floor(hours[-1].hour / float(step))) * HOUR)
        if next > hourmax:
            break
        if next.julday > hours[-1].julday:
            next = hours[-1].ceilday
        hours.append(next)

    return hours


def minutes_between(t1, t2, step=1):
    """

    :param t1:
    :param t2:
    :param step:
    :return:
    """
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')

    if not isinstance(step, int):
        raise TypeError('minutestep must be an int')
    t1 = t1.ceilminute
    t2 = t2.floorminute
    if t1 >= t2:
        return []

    minmin = t1.floorhour + step * np.ceil(t1.minute / float(step)) * MINUTE
    minmax = t2.floorhour + step * np.floor(t2.minute / float(step)) * MINUTE

    if minmin > minmax:
        return []

    minutes = [minmin]
    while True:
        next = minutes[-1].floorhour + step * (1 + np.floor(minutes[-1].minute / float(step))) * MINUTE
        if next > minmax:
            break
        if next.hour > minutes[-1].hour:
            next = minutes[-1].ceilhour
        minutes.append(next)

    return minutes


if __name__ == '__main__':
    #

    from obspy.core import UTCDateTime

    t = UTCFromTimestamp(0.)
    ut = UTCDateTime(0.)
    print(str(t), str(ut))
    # assert str(t) == str(ut)


    utc = UTC(year=2000, month=12, day=31, hour=10)
    utd = UTCDateTime(year=2000, month=12, day=31, hour=10)
    print(utc.timestamp, utd.timestamp)

    utc = UTCFromTimestamp(timestamp=utc.timestamp)
    utc = UTCFromStr(string=str(utc))

    print(utc)

    print(utc.timestamp)
    print(utc.year)
    print(utc.julday)
    print(utc.flooryear)
    print(utc.ceilyear)
    print(utc.floormonth)
    print(utc.ceilmonth)
    print(utc.floorday)
    print(utc.ceilday)

    u1 = UTCFromTimestamp(1)
    u2 = UTCFromTimestamp(2)
    assert u2 > u1
    dt = u2 - u1
    print(dt.total_seconds())

    print(years_between(
        UTC(2000, 2), UTC(2010, 2)))

    print(months_between(
        UTC(2000, 2), UTC(2010, 2)))
