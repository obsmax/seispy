from seispy.time.utc import UTC, UTCFromTimestamp, UTCFromStr
import numpy as np

"""
check consistency with obspy
obspy needed for this tests
"""
try:
    from obspy.core import UTCDateTime
except ImportError:
    raise ImportError('obspy not installed')


def test_utc():

    start = UTC(1990)
    end = UTC(2000)
    timestamps = np.arange(start.timestamp, end.timestamp, 1234.)

    for timestamp in timestamps:
        t = UTCDateTime(timestamp)

        x = UTC(year=t.year, month=t.month, day=t.day, hour=t.hour,
                minute=t.minute, second=t.second, microsecond=t.microsecond)
        y = UTCDateTime(year=t.year, month=t.month, day=t.day, hour=t.hour,
                        minute=t.minute, second=t.second, microsecond=t.microsecond)

        assert x.timestamp == y.timestamp
        assert str(x) == str(y)
        assert x.julday == y.julday


def test_utcfromtimestamp():
    start = UTC(1990)
    end = UTC(2000)
    timestamps = np.arange(start.timestamp, end.timestamp, 1234.)

    for timestamp in timestamps:
        x = UTCFromTimestamp(timestamp)
        y = UTCDateTime(timestamp)

        assert str(x) == str(y)
        assert x.julday == y.julday


def test_utcfromstr():
    start = UTC(1990)
    end = UTC(2000)
    timestamps = np.arange(start.timestamp, end.timestamp, 1234.)

    for timestamp in timestamps:
        s = str(UTCDateTime(timestamp))

        x = UTCFromStr(s)
        y = UTCDateTime(s)

        assert str(x) == str(y)
        assert x.timestamp == y.timestamp
        assert x.julday == y.julday


def test_utcjulday():
    start = UTC(1990)
    end = UTC(2000)
    timestamps = np.arange(start.timestamp, end.timestamp, 1234.)

    for timestamp in timestamps:
        s = str(UTCDateTime(timestamp))

        x = UTCFromStr(s)
        y = UTCDateTime(s)

        assert str(x) == str(y)
        assert x.timestamp == y.timestamp
        assert x.julday == y.julday