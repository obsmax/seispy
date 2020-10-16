import numpy as np


def costaperwidth(npts, sampling_rate, width, dtype=float):
    tap = np.ones(npts, dtype)
    Nwidth = int(np.round(width * sampling_rate))
    if not Nwidth :
        return tap

    t = np.arange(npts) / sampling_rate
    ttap = 0.5 * (np.sin(np.pi * t[:Nwidth] / float(width) / 1.0 + np.pi / 2.0) + 1.)
    tap[:Nwidth] *= ttap[::-1]
    tap[-Nwidth:] *= ttap
    return tap
