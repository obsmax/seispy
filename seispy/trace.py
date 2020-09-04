from copy import deepcopy
import warnings
import numpy as np
from seispy.filter.butter import lowpass, highpass, bandpass
from seispy.time.timetick import timetick

"""
Simplified objects for trace and stream without obspy 
"""


class Trace(object):
    def __init__(self, seedid: str = "",
                 delta: float = 0.,
                 starttime: float = 0.0,
                 longitude: float = 0.0,
                 latitude: float = 0.0,
                 elevation: float = 0.0,
                 distance: float = 0.0,
                 data: np.ndarray = np.array([], np.dtype('float64'))):

        self.seedid: str = seedid
        self.delta: float = delta
        self.starttime: float = starttime
        self.longitude: float = longitude
        self.latitude: float = latitude
        self.elevation: float = elevation
        self.distance: float = distance
        self.data: np.ndarray = data

    def __str__(self):
        return 'seedid:{} npts:{} delta:{}s starttime:{}s'.format(
            self.seedid,
            self.npts,
            self.delta,
            self.starttime)

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return deepcopy(self)

    @property
    def npts(self):
        return len(self.data)

    @property
    def endtime(self):
        return self.starttime + (self.npts - 1) * self.delta

    def from_obspy(self, trace):
        """
        :param trace: obspy.trace.Trace used to populate this object
        :return:
        """
        self.seedid = "{network}.{station}.{location}.{channel}".format(**trace.stats)
        self.delta = trace.stats.delta
        self.starttime = trace.stats.starttime.timestamp
        self.data = trace.data

        for key in ['longitude', 'latitude', 'elevation', 'distance']:

            try:
                self.__setattr__(key, trace.stats.coordinates[key])

            except (AttributeError, NameError, KeyError):

                warnings.warn('could not set attribute {}'.format(key))

    def to_obspy(self):
        """
        :return data, header: objects to use if you need to initate an obspy.trace.Trace
        """
        # warning this module must keep independant from obspy, I just assume here that the user is
        # trying to convert this object to obspy, so obspy is supposed to be installed
        try:
            from obspy.core.trace import Trace as ObspyTrace, UTCDateTime as ObspyUTCDateTime
        except ImportError as e:
            e.args = ('obspy not installed', )
            raise e

        network, station, location, channel = self.seedid.split('.')
        header = {"network": network,
                  "station": station,
                  "location": location,
                  "channel": channel,
                  "delta": self.delta,
                  "starttime": ObspyUTCDateTime(self.starttime),
                  "coordinates":{"longitude": self.longitude,
                                 "latitude": self.latitude,
                                 "elevation": self.elevation,
                                 "distance": self.distance}}

        return ObspyTrace(self.data, header)

    def rtime(self):
        return np.arange(self.npts) * self.delta

    def atime(self):
        return self.starttime + self.rtime()

    def obspy_like_decim(self, nwin=1000):
        """obspy-like data decimation for display (and only for display)"""
        t = self.atime()
        d = self.data
        if self.npts <= nwin:
            return t, d
        n_per_win = int(np.ceil(self.npts / float(nwin)))
        npad = n_per_win * nwin - self.npts
        lwin = n_per_win * self.delta
        assert self.npts + npad == n_per_win * nwin
        d = np.concatenate((self.data,
                            self.data[-1] * np.ones(npad, self.data.dtype)))
        d = d.reshape((nwin, n_per_win))
        min_values = d.min(axis=1)
        max_values = d.max(axis=1)

        values = np.zeros(2 * nwin + 2, d.dtype)
        timestamps = np.zeros(2 * nwin + 2, t.dtype)

        values[1:-1:2] = max_values
        values[2::2] = min_values
        values[0] = self.data[0]
        values[-1] = self.data[-1]
        timestamps[0] = self.starttime
        timestamps[-1] = self.endtime
        timestamps[1:-1:2] = timestamps[2::2] = \
            self.starttime + np.arange(nwin) * lwin + 0.5 * lwin

        return timestamps, values

    def obspy_like_show(self, ax, nwin=1000, *args, **kwargs):
        timestamps, values = self.obspy_like_decim(nwin)
        ax.plot(timestamps, values, *args, **kwargs)

    def show(self, ax, *args, **kwargs):
        ax.plot(self.atime(), self.data, *args, **kwargs)
        timetick(ax=ax, axis="x", major=True, minor=True)

    # ======================= PROCESSING
    def bandpass(self, freqmin, freqmax, order, zerophase):
        self.data = bandpass(
            self.data,
            freqmin=freqmin,
            freqmax=freqmax,
            sampling_rate=1. / self.delta,
            order=order,
            zerophase=zerophase)

    def lowpass(self, freqmax, order, zerophase):
        self.data = lowpass(
            self.data,
            freqmax=freqmax,
            sampling_rate=1. / self.delta,
            order=order,
            zerophase=zerophase)

    def highpass(self, freqmin, order, zerophase):
        self.data = highpass(
            self.data,
            freqmin=freqmin,
            sampling_rate=1. / self.delta,
            order=order,
            zerophase=zerophase)

    def gaussbandpass(self, freq0, alpha):
        from scipy.fftpack import fft, ifft, fftfreq, next_fast_len
        assert freq0 > 0
        nfft = next_fast_len(self.npts)
        freq = fftfreq(nfft, self.delta)
        g = np.exp(-alpha * ((np.abs(freq) - freq0) / freq0) ** 2.0)

        self.data = ifft(g * fft(self.data, nfft)).real
