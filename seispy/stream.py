from copy import deepcopy
import numpy as np
from numpy.lib.npyio import _savez
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
from seispy.trace import Trace, FourierDomainTrace
from seispy.errors import EmptyStreamError, DataTypeError, \
    SamplingError, SamplingRateError, NptsError, StarttimeError
from timetools.timetick import timetick
# from seispy.time.timetick import timetick


def readseispystream(npzfilename):
    st = Stream()
    st.from_npz(npzfilename=npzfilename)
    return st


class Stream(list):

    def __init__(self, traces: list = None):
        """
        initiate the instance with the stream (obspy or obsmax4)
        or nothing :  see self.from_obspy or self.from_npz"""

        if traces is None:
            super().__init__([])

        else:
            for trace in traces:
                if not isinstance(trace, Trace):
                    raise TypeError(type(traces))
            super().__init__(traces)

    def copy(self):
        return deepcopy(self)

    def __str__(self):
        return "\n".join([str(tr) for tr in self])

    def __repr__(self):
        return self.__str__()

    # ============ convertion from or to obspy
    def from_obspy(self, stream):
        """populate the objects with an obspy stream
        use it to convert obspy into a seispy object
        """

        for obspy_trace in stream:
            trace = Trace()
            trace.from_obspy(obspy_trace)
            self.append(trace)

    def to_obspy(self):
        # warning this module must keep independant from obspy, I just assume here that the user is
        # trying to convert this object to obspy, so obspy is installed
        try:
            from obspy.core.stream import Stream as ObspyStream
        except ImportError as e:
            e.args = ('obspy not installed', )
            raise e

        obspy_traces = []
        for seispy_trace in self:
            obspy_trace = seispy_trace.to_obspy()
            obspy_traces.append(obspy_trace)

        return ObspyStream(obspy_traces)

    # ============
    def check_data_types(self):

        if not len(self):
            raise EmptyStreamError()

        dtype = self[0].data.dtype
        for trace in self[1:]:
            if dtype != trace.data.dtype:
                raise DataTypeError
        return dtype

    def check_stream_sampling_regularization(self):
        """
        verifies that all traces have the same time vector
        :return:
        """

        if not len(self):
            raise EmptyStreamError()

        msg = 'the stream is not regularized, please resample {}, ({}, {})'
        nptss = np.asarray([tr.npts for tr in self], int)
        deltas = np.asarray([tr.delta for tr in self], float)
        starttimes = np.asarray([tr.starttime for tr in self], float)

        npts = self[0].npts
        delta = self[0].delta
        starttime = self[0].starttime

        is_npts = nptss == npts
        is_delta = deltas == delta
        is_start = starttimes == starttime

        if not is_npts.all():
            raise NptsError(msg.format("npts", npts, nptss[~is_npts][0]))

        elif not is_delta.all():
            raise SamplingRateError(msg.format("delta", delta, deltas[~is_delta][0]))

        elif not is_start.all():
            raise StarttimeError(msg.format("starttime", starttime, starttimes[~is_start][0]))

        return npts, delta, starttime

    def regularize(self, fill_value: float = 0.0, qc: bool = True):

        if not len(self):
            raise EmptyStreamError()

        starttimes = np.asarray([tr.starttime for tr in self], float)
        endtimes = np.asarray([tr.endtime for tr in self], float)
        deltas = np.asarray([tr.delta for tr in self], float)

        delta = np.min(deltas)
        start = np.min(starttimes)
        end = np.max(endtimes)

        new_npts = int(np.floor((end - start) / delta))
        new_time = np.arange(new_npts) * delta + start

        for n, tr in enumerate(self):
            tr: Trace

            if (tr.delta == delta) and \
                    (tr.starttime == start) and \
                    (tr.npts == new_npts):
                # no need to interpolate the signal
                continue

            old_time = tr.atime()
            old_data = tr.data

            tr.data = np.interp(
                new_time, xp=old_time, fp=old_data,
                left=fill_value, right=fill_value)

            tr.starttime = start
            tr.delta = delta

        if qc:
            try:
                self.check_stream_sampling_regularization()
            except (EmptyStreamError, SamplingError) as e:
                e.args = ("the regularization failed, {}".format(str(e)))

    def mean(self):
        nptss = np.asarray([tr.npts for tr in self], float)
        sum = np.sum([tr.data.sum() for tr in self])
        mean = sum / nptss.sum()
        return mean

    def pseudo_std(self):
        """
        std is evaluated by means of deviations relative to the mean of each trace
        and not relative to the ensemble mean as in self.std
        """
        nptss = np.asarray([tr.npts for tr in self], float)
        covariances = np.asarray([tr.data.std() ** 2.0 for tr in self], float)  # E((Xi - E(Xi))^2)
        return ((nptss * covariances).sum() / nptss.sum()) ** 0.5

    def std(self):
        # return np.concatenate([tr.data for tr in self]).std()

        # same as above without concatenating arrays
        nptss = np.asarray([tr.npts for tr in self], float)
        means = np.asarray([tr.data.mean() for tr in self], float)
        mean = (nptss * means).sum() / nptss.sum()
        deviations = np.array([((tr.data - mean) ** 2.0).sum() for tr in self])
        return (deviations.sum() / nptss.sum()) ** 0.5

    def clip(self, nstd=10.0):
        """
        remove outliers above a certain threshold given in number of times the pseudo_std
        :param nstd:
        :return:
        """
        means = np.asarray([tr.data.mean() for tr in self], float)
        pseudo_std = self.pseudo_std()
        for tr, m in zip(self, means):
            tr.data = tr.data.clip(m - nstd * pseudo_std, m + nstd * pseudo_std)

    def show(self, ax, gain=0.1, color="k", alpha=0.4,
             seedticks=False, linewidth=2, linestyle="-",
             obspy_decim=False, obspy_decim_nwin=1000):
        """
        show many traces on same plot with vertical offset 1 per trace

        :param ax:
        :param gain:
        :param color:
        :param alpha:
        :param seedticks:
        :param linewidth:
        :param linestyle:
        :param obspy_decim:
        :return:
        """

        if len(self) <= 1:
            raise ValueError('too few items for st.show, ')

        fourier_domain = np.all([isinstance(tr, FourierDomainTrace) for tr in self])

        xmin, xmax = np.inf, -np.inf
        edge_segments = []
        assert 0 < alpha <= 1.0
        i = 0

        if fourier_domain:
            fs, dats = [], []
            for i, tr in enumerate(self):
                f, dat = tr.side(sign=1, zero=False, copy=False)
                fs.append(f)
                dats.append(np.abs(dat))

            k = gain / np.std(np.hstack(dats))
            xmin = np.hstack(fs).min()
            xmax = np.hstack(fs).max()

            for i, (f, dat) in enumerate(zip(fs, dats)):
                edge_segments.append(np.column_stack((f, k * dat + i)))

        else:
            k = gain / self.std()
            for i, tr in enumerate(self):
                if obspy_decim:
                    t, dat = tr.obspy_like_decim(nwin=obspy_decim_nwin)
                    dat = np.column_stack((t, k * dat + i))
                else:
                    dat = np.column_stack((tr.atime(), k * tr.data + i))

                edge_segments.append(dat)

                if tr.starttime < xmin:
                    xmin = tr.starttime
                if tr.endtime > xmax:
                    xmax = tr.endtime

        coll = LineCollection(
            edge_segments, colors=color, alpha=alpha,
            linewidths=linewidth, linestyles=linestyle)
        ax.add_collection(coll)

        if seedticks:
            yticks = np.arange(len(self))
            yticklabels = [_.seedid for _ in self]
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)

        ax.set_xlim(xmin, xmax)
        ax.set_ylim(-1., i + 1.)

        if fourier_domain:
            pass
        else:
            timetick(ax=ax, axis="x", major=True, minor=True)
        return coll

    def shade(self, ax, cmap=None, vmin=None, vmax=None, powergain=1., seedticks=False, **kwargs):
        """

        :param ax: obsmax4.graphictools.gutils.myax object, use obsmax4.graphictools.gca
        :param cmap: colormap
        :param vmin: float, lowest value, or None
        :param vmax: float, highest value, or None
        :param powergain: float, > 0, apply power gain to the plotted amplitudes
        :param cticks:
        :param args:
        :param kwargs:
        :return:
        """

        assert len(self)
        kwargs.setdefault('rasterized', True)

        fourier_domain = np.all([isinstance(tr, FourierDomainTrace) for tr in self])

        if cmap is None:
            if fourier_domain:
                cmap = plt.get_cmap('nipy_spectral')
            else:
                cmap = plt.get_cmap('gray')

        nmax = np.max([len(tr.data) for tr in self])

        T, I, D = [], [], []
        dmin, dmax = np.inf, -np.inf
        for n, tr in enumerate(self):
            if fourier_domain:
                f, d = tr.side(sign=1, zero=False, copy=False)
                d = np.abs(d)
            else:
                d = tr.data[:]

            if powergain != 1.:
                d = np.sign(d) * np.abs(d) ** powergain

            # all items in D must be the same length
            d = np.concatenate((d, np.nan * np.zeros(nmax - len(d))))
            d = np.ma.masked_where(np.isnan(d) | np.isinf(d), d)
            dmin = np.min([dmin, d.min()])
            dmax = np.max([dmax, d.max()])
            # -----
            D.append(d)
            if n <= len(self) - 2:
                D.append(d * 0.)

            # -----
            if fourier_domain:
                df = f[1] - f[0]
                f = -.5 * df + np.hstack((f, (f[-1] + df) * np.ones(nmax + 1 - len(f))))
                T.append(f)
                T.append(f)
            else:
                dt = tr.delta
                t = -.5 * dt + tr.starttime + np.arange(nmax+1) * dt
                T.append(t)
                T.append(t)

            # -----
            I.append(n - .5 * np.ones(len(d) + 1))
            I.append(n + .5 * np.ones(len(d) + 1))

        T, I, D = [np.asarray(_) for _ in [T, I, D]]
        if vmin is None and vmax is None:
            vmax = np.max([abs(dmin), abs(dmax)])
            vmin = -vmax
        if vmax is None:
            vmax = dmax
        if vmin is None:
            vmin = dmin

        if fourier_domain:
            vmin=0.
            vmax=vmax

        # print(T.shape, I.shape, D.shape)
        coll = ax.pcolormesh(
            T, I, D,
            cmap=cmap,
            vmin=vmin, vmax=vmax,
            **kwargs)

        if seedticks:
            yticks = np.arange(len(self))
            yticklabels = [_.seedid for _ in self]
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)

        ax.set_xlim((T.min(), T.max()))
        ax.set_ylim((0, I.max()))

        cbarwidth = 0.008
        cbarheight = 0.5
        cbardist = 0.012
        p = ax.get_position()
        cax = ax.figure.add_axes((p.x1 + cbardist * p.width,
                                    p.y0 + 0.5 * (1. - cbarheight) * p.height,
                                    cbarwidth, cbarheight * p.height))

        ax.figure.colorbar(coll, cax=cax, ticks=[vmin, 0, vmax])
        cax.set_yticklabels(["-", "0", "+"])

        if not fourier_domain:
            timetick(ax=ax, axis="x", major=True, minor=True)

        return coll, cax

    def savez(self, npzfilename):
        """
        write the stream under npz format
        the filename must end with .seispystream.npz

        :param npzfilename:
        :return:
        """
        if not len(self):
            raise EmptyStreamError

        if not npzfilename.endswith('.seispystream.npz'):
            raise ValueError('npzfilename does not end with .seispystream.npz')

        # == put the metadata into lists, one per item
        kwargs = {
            "npts":      np.array([trace.npts      for trace in self], np.dtype('uint32')),
            "delta":     np.array([trace.delta     for trace in self], np.dtype('float64')),
            "starttime": np.array([trace.starttime for trace in self], np.dtype('float64')),
            "seedid":    np.array([trace.seedid    for trace in self], np.dtype('str')),
            "longitude": np.array([trace.longitude for trace in self], np.dtype('float64')),
            "latitude":  np.array([trace.latitude  for trace in self], np.dtype('float64')),
            "elevation": np.array([trace.elevation for trace in self], np.dtype('float64')),
            "distance":  np.array([trace.distance  for trace in self], np.dtype('float64'))}

        # == store the data arrays as individual items named
        #    data_network_station_location_channel_idnumber
        for array_id, trace in enumerate(self):
            key = "data_{seedid}_{array_id}".format(
                seedid=trace.seedid.replace('.', '_'),
                array_id=array_id)
            kwargs[key] = trace.data

        _savez(npzfilename, args=(), compress=True, allow_pickle=False,
               kwds=kwargs)

    def from_npz(self, npzfilename):
        """
        populate the object with a .seispystream.npz file
        :param npzfilename:
        :return:
        """
        assert npzfilename.endswith('.seispystream.npz')

        with np.load(npzfilename) as loader:
            delta = loader["delta"]
            starttime = loader["starttime"]
            seedid = loader["seedid"]
            longitude = loader["longitude"]
            latitude = loader["latitude"]
            elevation = loader["elevation"]
            distance = loader["distance"]

            for array_id in range(len(delta)):
                data_key_old = 'data_{seedid}_{array_id}'.format(
                    seedid=seedid[array_id],
                    array_id=array_id)

                data_key_new = 'data_{seedid}_{array_id}'.format(
                    seedid=seedid[array_id].replace('.', '_'),
                    array_id=array_id)

                if data_key_new in loader.files:
                    data_key = data_key_new
                elif data_key_old in loader.files:
                    data_key = data_key_old
                else:
                    raise KeyError(npzfilename, data_key_new, data_key_old)

                trace = Trace(
                    seedid=seedid[array_id],
                    delta=delta[array_id],
                    starttime=starttime[array_id],
                    longitude=longitude[array_id],
                    latitude=latitude[array_id],
                    elevation=elevation[array_id],
                    distance=distance[array_id],
                    data=loader[data_key])

                self.append(trace)

    def get(self, key):

        if not len(self):
            raise EmptyStreamError

        try:
            values = np.asarray([trace.__getattribute__(key) for trace in self])

        except (AttributeError, KeyError) as e:
            message = "key {} was not found in " \
                      "the attributes of class {}".format(
                key, type(self[0]))
            e.args = (message, )
            raise e

        return values

    def sort_by(self, key, order=1):
        if not order in [1, -1]:
            raise ValueError

        # == extract sorting value
        values = self.get(key)

        # == order by sorting value
        i_sort = np.argsort(values)
        if order == -1:
            i_sort = i_sort[::-1]

        # == update the object
        self.__init__([self[i] for i in i_sort])

    def reject_seedids(self, seedids):
        if not len(self):
            raise EmptyStreamError

        trace_seedids = np.array([trace.seedid for trace in self], str)
        bad_traces = np.in1d(trace_seedids, seedids)

        self.__init__([self[i] for i in
                       range(len(self))
                       if not bad_traces[i]])

    def reject_nulls(self):
        seedids = self.get('seedid')
        bad_traces = np.array([(tr.data == 0.).all() for tr in self], bool)
        null_seedids = seedids[bad_traces]
        self.reject_seedids(null_seedids)
        return null_seedids

    def lowpass(self, *args, **kwargs):
        for trace in self:
            trace.lowpass(*args, **kwargs)

    def highpass(self, *args, **kwargs):
        for trace in self:
            trace.highpass(*args, **kwargs)

    def bandpass(self, *args, **kwargs):
        for trace in self:
            trace.bandpass(*args, **kwargs)

    def gaussbandpass(self, *args, **kwargs):
        for trace in self:
            trace.gaussbandpass(*args, **kwargs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    stream = Stream([])
    for _ in range(10):
        tr = Trace(
            seedid=str(int(np.random.rand() * 1.e4)),
            delta=0.4 + 0.1 * np.random.rand(),
            starttime=1000. + 10 * np.random.randn(),
            data=np.random.randn(int(2500 + np.random.randn() * 10)))
        stream.append(tr)

    print(stream)

    stream.show(plt.gca(), gain=0.1, color="k")

    # plt.show()

    dtype = stream.check_data_types()

    oldstd = stream.std()
    stream.regularize(qc=True)
    newstd = stream.std()

    stream.show(plt.gca(), gain=0.1 * newstd / oldstd, color="r", obspy_decim=True)
    stream.savez('toto.seispystream.npz')
    del stream
    stream = Stream([])
    stream.from_npz('toto.seispystream.npz')

    # plt.show()
    stream.show(plt.gca(), gain=0.1 * newstd / oldstd, color="g", linestyle="--")
    print(stream)

    plt.show()
