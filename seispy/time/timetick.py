import matplotlib.pyplot as plt
from matplotlib import ticker
from seispy.time.utc import *
import datetime
import numpy as np

MINUTE = 60.
HOUR = 60. * MINUTE
DAY = 24. * HOUR
YEAR = 365.25 * DAY


# class MajorTimeLocator(ticker.LinearLocator):
#     ntick_min = 10
#     ntick_max = 12
#     def tick_values(self, vmin: float, vmax: float):
#         tmin = UTCFromTimestamp(vmin)
#         tmax = UTCFromTimestamp(vmax)
# 
#         years = years_between(tmin, tmax, step=1)
#         xticks = [_.timestamp for _ in years]
#         if len(xticks) > self.ntick_min:
#             if len(xticks) > self.ntick_max:
#                 xticks = xticks[::len(xticks)//self.ntick_max]
#             return xticks
# 
#         days = days_between(tmin, tmax, step=1)
#         xticks = xticks + [_.timestamp for _ in days]
#         xticks = list(np.unique(xticks))
#         if len(xticks) > self.ntick_min:
#             if len(xticks) > self.ntick_max:
#                 xticks = xticks[::len(xticks)//self.ntick_max]
#             return xticks
# 
#         hours = hours_between(tmin, tmax, step=1)
#         xticks = xticks + [_.timestamp for _ in hours]
#         xticks = list(np.unique(xticks))
#         if len(xticks) > self.ntick_min:
#             if len(xticks) > self.ntick_max:
#                 xticks = xticks[::len(xticks)//self.ntick_max]
#             return xticks
# 
#         minutes = minutes_between(tmin, tmax, step=1)
#         xticks = xticks + [_.timestamp for _ in minutes]
#         xticks = list(np.unique(xticks))
#         if len(xticks) > self.ntick_min:
#             if len(xticks) > self.ntick_max:
#                 xticks = xticks[::len(xticks)//self.ntick_max]
#             return xticks
# 
#         return xticks
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
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 20)]

            elif duration >= 40. * YEAR:
                yearmin = int(10. * (utmin.flooryear.year / 10))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 10)]

            elif duration >= 15. * YEAR:
                yearmin = int(5. * (utmin.flooryear.year / 5))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 5)]

            elif duration >= 5. * YEAR:
                yearmin = int(2. * (utmin.flooryear.year / 2))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 2)]

            elif duration >= 3. * YEAR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                xticks = [t.timestamp for t in years]

            else:  # if duration >= 1. * YEAR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=100)
                xticks = [t.timestamp for t in years + days]

        # ----------------------------------------------
        elif duration >= 2. * DAY:
            if duration >= 6. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=50)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 2. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=20)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 15. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + days]

            elif duration >= 5. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + days]

            else:  # if duration >= 2. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + days]

        # ----------------------------------------------
        elif duration >= HOUR:
            if duration >= 30. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=12)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 15. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=6)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 5. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + hours]

            elif duration >= 2. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + hours]

            else:  # if duration >= HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=30)
                xticks = [t.timestamp for t in years + minutes]

        # ----------------------------------------------
        elif duration >= 10.:
            if duration >= 15. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + minutes]


            elif duration >= 5. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + minutes]


            elif duration >= 2. * MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + minutes]


            elif duration >= MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 20.)
                xticks = [t.timestamp for t in years] + list(seconds)


            elif duration >= 20.:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 10.)
                xticks = [t.timestamp for t in years] + list(seconds)


            else:  # if duration >= 10.:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 5.)
                xticks = [t.timestamp for t in years] + list(seconds)


        # ----------------------------------------------
        elif duration >= 5.:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 2.)
            xticks = [t.timestamp for t in years] + list(seconds)


        elif duration >= 2.:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 1.)
            xticks = [t.timestamp for t in years] + list(seconds)


        elif duration >= 1.:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .5)
            xticks = [t.timestamp for t in years] + list(seconds)


        elif duration >= .5:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .25)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .2:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .1)
            xticks = [t.timestamp for t in years] + list(seconds)

        elif duration >= .1:

            years = years_between(utmin.flooryear, utmax.ceilyear)
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
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 10)]
                return np.unique(xticks)

            elif duration >= 5. * YEAR:
                yearmin = int(2. * (utmin.flooryear.year / 2))
                yearmax = utmax.ceilyear.year
                xticks = [UTC(year=y, month=1, day=1, hour=0).timestamp for y in np.arange(yearmin, yearmax, 1)]
                return np.unique(xticks)

            elif duration >= 2. * YEAR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                months = months_between(utmin, utmax)
                xticks = [t.timestamp for t in years + months] 
                return np.unique(xticks)

            else:  # if duration >= 6. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=10)
                xticks = [t.timestamp for t in years + days]   
                return np.unique(xticks)

        # -------------------------------------------
        if duration >= 15. * HOUR:      
            if duration >= 2. * 30. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + days] 
                return np.unique(xticks)

            elif duration >= 15. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                days = days_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + days]
                return np.unique(xticks)

            elif duration >= 5. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=12)
                xticks = [t.timestamp for t in years + hours]
                return np.unique(xticks)

            elif duration >= 2. * DAY:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=2)
                xticks = [t.timestamp for t in years + hours]
                return np.unique(xticks)

            else:  # if duration >= 15. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                hours = hours_between(utmin, utmax, step=1)
                xticks = [t.timestamp for t in years + hours]
                return np.unique(xticks)

        # -------------------------------------------
        if duration >= HOUR:
            if duration >= 5. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=30)
                xticks = [t.timestamp for t in years + minutes]
                return np.unique(xticks)

            elif duration >= 2. * HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=10)
                xticks = [t.timestamp for t in years + minutes]
                return np.unique(xticks)

            else:  # if duration >= HOUR:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                minutes = minutes_between(utmin, utmax, step=5)
                xticks = [t.timestamp for t in years + minutes]
                return np.unique(xticks)

        # -------------------------------------------
        if duration >= 10.:
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
                return np.unique(xticks)

            elif duration >= MINUTE:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 2.)
                xticks = [t.timestamp for t in years] + list(seconds)
                return np.unique(xticks)

            elif duration >= 20.:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, 1.)
                xticks = [t.timestamp for t in years] + list(seconds)
                return np.unique(xticks)

            else:
                years = years_between(utmin.flooryear, utmax.ceilyear)
                secondmin = utmin.floorminute
                secondmax = utmax.ceilminute
                seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .5)
                xticks = [t.timestamp for t in years] + list(seconds)
                return np.unique(xticks)

        # -------------------------------------------
        if duration >= 2.:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .1)
            xticks = [t.timestamp for t in years] + list(seconds)
            return np.unique(xticks)

        elif duration >= .5:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .05)
            xticks = [t.timestamp for t in years] + list(seconds)
            return np.unique(xticks)

        elif duration >= .2:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .025)
            xticks = [t.timestamp for t in years] + list(seconds)
            return np.unique(xticks)

        elif duration >= .1:
            years = years_between(utmin.flooryear, utmax.ceilyear)
            secondmin = utmin.floorminute
            secondmax = utmax.ceilminute
            seconds = np.arange(secondmin.timestamp, secondmax.timestamp, .01)
            xticks = [t.timestamp for t in years] + list(seconds)
            return np.unique(xticks)

        else:
            return []


def TimeFormatter(timevalue, tickposition=None):
    """

    :param timevalue:
    :param tickposition:
    :return:
    """
    utime = UTCFromTimestamp(timevalue)
    y,j,h,m,s,ms = utime.year, utime.julday, utime.hour, \
                   utime.minute, utime.second, utime.microsecond
    if ms != 0:
        if int(ms / 100.) == float(ms) / 100.:
            return "%02.0f:%02.0f:%04.2f" % (h,m,s + 1.0e-6 *ms)
        return "%02.0f:%02.0f:%09.6f %04.0f-%02.0f-%02.0f" % \
               (h,m,s + 1.0e-6 *ms, y, utime.month, utime.day)
    if s != 0:
        return "%02.0f:%02.0f:%02.0f" % (h,m,s)
    if m != 0:
        return "%02.0f:%02.0f" % (h,m)
    if h != 0:
        return "%02.0f:00" % h
    if j != 1:
        return "%03.0f" % (j)
    else:
        if y != 1970: return "%04.0f" % y
        else: return "0"


def timetick(axe, axis='x', major=True, minor=True):
    """
    k > 1. increase the number of ticks
    """

    M = MajorTimeLocator()
    m = MinorTimeLocator()

    if 'x' in axis:
        axe.xaxis.set_major_formatter(ticker.FuncFormatter(TimeFormatter))
        if major: axe.xaxis.set_major_locator(M)
        # if minor: axe.xaxis.set_minor_locator(m)
    if 'y' in axis:
        axe.yaxis.set_major_formatter(ticker.FuncFormatter(TimeFormatter))
        if major: axe.yaxis.set_major_locator(M)
        # if minor: axe.yaxis.set_minor_locator(m)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    start = UTC(2018, 1, 20)
    end = UTC(2018, 2, 3)
    t = np.linspace(start.timestamp, end.timestamp, 100)
    plt.plot(t, t * 0, 'ko')
    timetick(plt.gca(), 'x')
    plt.show()