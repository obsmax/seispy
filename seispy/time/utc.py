import time
import datetime
import numpy as np

MINUTE = 60.
HOUR = 60. * MINUTE
DAY = 24. * HOUR
YEAR = 365.25 * DAY
WEEK = 7. * DAY

UTCTZINFO = datetime.timezone(datetime.timedelta(0), 'UTC')


class UTC(datetime.datetime):

    def __new__(cls, year=1970, month=1, day=1,
                hour=0, minute=0, second=0, microsecond=0):

        self = super(UTC, cls).__new__(
            cls, year=year, month=month, day=day,
            hour=hour, minute=minute,
            second=second, microsecond=microsecond,
            tzinfo=UTCTZINFO)
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
        timedelta = (self - self.flooryear)
        julday = int(np.floor(timedelta.total_seconds() / DAY)) + 1
        return julday

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
            return UTC(year=self.year, month=self.month, day=self.day,
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
            return UTC(year=self.year, month=self.month, day=self.day,
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
        # d = datetime.datetime.fromtimestamp(timestamp - HOUR)   # ????
        d = datetime.datetime.fromtimestamp(timestamp, tz=UTCTZINFO)   # ????
        self = UTC.__new__(
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

        self = UTC.__new__(
            cls,
            year=int(yyyy),
            month=int(mt),
            day=int(dd),
            hour=int(hh),
            minute=int(mn),
            second=int(ss),
            microsecond=int(n))
        return self


def years_between(t1: UTC, t2: UTC) -> list:
    """bounds included"""
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')
    yearmin = t1.ceilyear.year
    yearmax = t2.flooryear.year
    if yearmin > yearmax:
        return []
    years = [UTC(y) for y in range(yearmin, yearmax + 1)]
    return years


def months_between(t1: UTC, t2: UTC) -> list:
    """bounds included"""
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
        months.append(UTCFromTimestamp(months[-1].timestamp + 1.).ceilmonth)

    return months


def days_between(t1: UTC, t2: UTC, step: int=1) -> list:
    """bounds included"""
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')

    t1_timestamp = t1.timestamp
    t2_timestamp = t2.timestamp

    days = np.arange(t1.flooryear.timestamp, t2.ceilyear.timestamp + 1, step * DAY)
    days = [UTCFromTimestamp(d) for d in days if t1_timestamp <= d <= t2_timestamp]
    return days


def hours_between(t1: UTC, t2: UTC, step: int=1) -> list:
    """bounds included"""
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')

    t1_timestamp = t1.timestamp
    t2_timestamp = t2.timestamp

    hours = np.arange(t1.floorday.timestamp, t2.ceilday.timestamp + 1., step * HOUR)
    hours = [UTCFromTimestamp(h) for h in hours if t1_timestamp <= h <= t2_timestamp]
    return hours


def minutes_between(t1: UTC, t2: UTC, step: int=1) -> list:
    """bounds included"""
    if t1 >= t2:
        raise ValueError('utmin must be lower than utmax')

    t1_timestamp = t1.timestamp
    t2_timestamp = t2.timestamp

    minutes = np.arange(t1.floorhour.timestamp, t2.ceilhour.timestamp + 1., step * MINUTE)
    minutes = [UTCFromTimestamp(m) for m in minutes if t1_timestamp <= m <= t2_timestamp]
    return minutes


if __name__ == '__main__':
    #

    from obspy.core import UTCDateTime

    x, y = [], []
    for year in range(1990, 1995):
        for month in range(1, 13):
            for day in range(32):
                for hour in range(0, 25, 1):
                    try:
                        x = UTC(year=year, month=month, day=day, hour=hour)
                        y = UTCDateTime(year=year, month=month, day=day, hour=hour)
                        assert x.timestamp == y.timestamp
                        assert str(x) == str(y)
                    except ValueError:
                        pass

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
