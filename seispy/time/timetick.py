import matplotlib.pyplot as plt
from matplotlib import ticker
from seispy.time.utc import *
import datetime
import numpy as np

MINUTE = 60.
HOUR = 60. * MINUTE
DAY = 24. * HOUR
YEAR = 365.25 * DAY


class MajorTimeLocator(ticker.LinearLocator):
    """the crappiest code I ever wrote, but works, so ..."""

    def tick_values(self, vmin, vmax):
        utmin = UTCFromTimestamp(vmin)
        utmax = UTCFromTimestamp(vmax)

        duration = (utmax - utmin).total_seconds()

        # ----------------------------------------------
        if duration >= 1. * YEAR:
            if duration >= 100. * YEAR:
                yearmin = int(100. * (utmin.flooryear.year / 100))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 20)]

            elif duration >= 40. * YEAR:
                yearmin = int(10. * (utmin.flooryear.year / 10))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 10)]

            elif duration >= 15. * YEAR:
                yearmin = int(5. * (utmin.flooryear.year / 5))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 5)]

            elif duration >= 5. * YEAR:
                yearmin = int(2. * (utmin.flooryear.year / 2))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 2)]

            elif duration >= 3. * YEAR:
                years = years_between(utmin, utmax)
                xticks = [t.timestamp for t in years]

            else:  # if duration >= 1. * YEAR:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=100)
                xticks = [t.timestamp for t in years + days]

        # ----------------------------------------------
        elif duration >= 2. * DAY:
            if duration >= 6. * 30. * DAY:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=50)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 2. * 30. * DAY:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=20)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 15. * DAY:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 5. * DAY:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + days]

            else:  # if duration >= 2. * DAY:
                years = years_between(utmin, utmax)
                days = days_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + days]

        # ----------------------------------------------
        elif duration >= HOUR:
            if duration >= 30. * HOUR:
                years = years_between(utmin, utmax)
                hours = hours_between(utmin, utmax, step=12)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 15. * HOUR:
                years = years_between(utmin, utmax)
                hours = hours_between(utmin, utmax, step=6)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 5. * HOUR:
                years = years_between(utmin, utmax)
                hours = hours_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 2. * HOUR:
                years = years_between(utmin, utmax)
                hours = hours_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + hours]

            else:  # if duration >= HOUR:
                years = years_between(utmin, utmax)
                minutes = minutes_between(utmin, utmax, step=30)
                xticks = [t.timestamp for t in years + minutes]

        # ----------------------------------------------
        elif duration >= 10.:
            if duration >= 15. * MINUTE:
                years = years_between(utmin, utmax)
                minutes = minutes_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + minutes]

            elif duration >= 5. * MINUTE:
                years = years_between(utmin, utmax)
                minutes = minutes_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + minutes]

            elif duration >= 2. * MINUTE:
                years = years_between(utmin, utmax)
                minutes = minutes_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + minutes]

            elif duration >= MINUTE:
                years = years_between(utmin, utmax)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp + 1., 20.)
                xticks = [y.timestamp for y in years] + list(seconds)

            elif duration >= 20.:
                years = years_between(utmin, utmax)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 10.)
                xticks = [y.timestamp for y in years] + list(seconds)

            else:  # if duration >= 10.:
                years = years_between(utmin, utmax)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 5.)
                xticks = [y.timestamp for y in years] + list(seconds)

        # ----------------------------------------------
        elif duration >= 5.:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 2.)
            xticks = [y.timestamp for y in years] + list(seconds)

        elif duration >= 2.:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 1.)
            xticks = [y.timestamp for y in years] + list(seconds)

        elif duration >= 1.:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .5)
            xticks = [y.timestamp for y in years] + list(seconds)

        elif duration >= .5:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .25)
            xticks = [y.timestamp for y in years] + list(seconds)

        elif duration >= .2:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .1)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .1:
            years = years_between(utmin, utmax)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .05)
            xticks = [t.timestamp for t in years] + list(seconds)

        else:
            xticks = []

        return np.unique(xticks)


class MinorTimeLocator(ticker.LinearLocator):

    def tick_values(self, vmin, vmax):
        utmin = UTCFromTimestamp(vmin)
        utmax = UTCFromTimestamp(vmax)

        duration = (utmax - utmin).total_seconds()
        # -------------------------------------------
        if duration >= 6. * 30. * DAY:
            if duration >= 100. * YEAR:
                yearmin = int(100. * (utmin.flooryear.year / 100))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 10)]

            elif duration >= 5. * YEAR:
                yearmin = int(2. * (utmin.flooryear.year / 2))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp
                          for y in np.arange(yearmin, yearmax, 1)]

            elif duration >= 2. * YEAR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                months = months_between(utmin, utmax)
                xticks = [t.timestamp for t in years + months] 

            else:  # if duration >= 6. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=10)
                xticks = [t.timestamp for t in years + days]   

        # -------------------------------------------
        elif duration >= 15. * HOUR:
            if duration >= 2. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + days] 

            elif duration >= 15. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 5. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=12)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 2. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + hours]

            else:  # if duration >= 15. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + hours]

        # -------------------------------------------
        elif duration >= HOUR:
            if duration >= 5. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=30)
                xticks = [t.timestamp for t in years + minutes]

            elif duration >= 2. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=10)
                xticks = [t.timestamp for t in years + minutes]

            else:  # if duration >= HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + minutes]

        # -------------------------------------------
        elif duration >= 10.:
            if duration >= 15. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + minutes]
                return np.unique(xticks)

            elif duration >= 5. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 30.)
                xticks = [t.timestamp for t in years] + list(seconds)
                return np.unique(xticks)

            elif duration >= 2. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 5.)
                xticks = [t.timestamp for t in years] + list(seconds)

            elif duration >= MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 2.)
                xticks = [t.timestamp for t in years] + list(seconds)

            elif duration >= 20.:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 1.)
                xticks = [t.timestamp for t in years] + list(seconds)

            else:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .5)
                xticks = [t.timestamp for t in years] + list(seconds)

        # -------------------------------------------
        elif duration >= 2.:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .1)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .5:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .05)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .2:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .025)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .1:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .01)
            xticks = [t.timestamp for t in years] + list(seconds)

        else:
            xticks = []

        return np.unique(xticks)


def TimeFormatter(timevalue, tickposition=None):

    utime = UTCFromTimestamp(timevalue)

    if utime.microsecond:
        return f"{utime.hour:02d}:" \
               f"{utime.minute:02d}:" \
               f"{utime.second + 1e-6 * utime.microsecond:04.2f}".rstrip('0')

    elif utime.second:
        return f"{utime.hour:02d}:" \
               f"{utime.minute:02d}:" \
               f"{utime.second:02d}"

    elif utime.minute:
        return f"{utime.hour:02d}:" \
               f"{utime.minute:02d}"

    elif utime.hour:
        return f"{utime.hour:02d}:00"

    elif utime.julday != 1:
        return f"{utime.julday:03d}"

    elif utime.year != 1970:
        return f"{utime.year:04d}"

    else:
        return "0"


def timetick(ax, axis='x', major=True, minor=True):

    M = MajorTimeLocator()
    m = MinorTimeLocator()

    if 'x' in axis:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(TimeFormatter))
        if major:
            ax.xaxis.set_major_locator(M)
        if minor:
            ax.xaxis.set_minor_locator(m)

    if 'y' in axis:
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(TimeFormatter))
        if major:
            ax.yaxis.set_major_locator(M)
        if minor:
            ax.yaxis.set_minor_locator(m)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    start = UTC(2018, 1, 20)
    end = UTC(2018, 2, 3)
    t = np.linspace(start.timestamp, end.timestamp, 100)
    plt.plot(t, t * 0, 'ko')
    timetick(plt.gca(), 'x')
    plt.show()