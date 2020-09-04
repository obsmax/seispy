import numpy as np
import matplotlib.pyplot as plt
import datetime
from obspy.core import UTCDateTime

UTCTZINFO = datetime.timezone(datetime.timedelta(0), 'UTC')

x, y = [], []
for year in range(1990, 1995):
    for month in range(1, 13):
        for day in range(32):
            for hour in range(0, 25, 1):
                try:
                    x.append(datetime.datetime(year=year, month=month, day=day, hour=hour, tzinfo=UTCTZINFO).timestamp())
                    y.append(UTCDateTime(year=year, month=month, day=day, hour=hour).timestamp)
                except ValueError:
                    pass

x = np.asarray(x, float)
y = np.asarray(y, float)

plt.plot((x - y) / 3600.)
plt.show()