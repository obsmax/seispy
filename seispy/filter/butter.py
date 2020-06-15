from scipy.signal import butter, lfilter


# ---- filter coefficients or frequency response
def butter_bandpass_coefficients(freqmin, freqmax, sampling_rate, order=4.):
    """
    :param freqmin:
    :param freqmax:
    :param sampling_rate:
    :param order:
    :return:
    """
    nyq = 0.5 * sampling_rate
    b, a = butter(N=order, Wn=[freqmin / nyq, freqmax / nyq], btype='band')
    return b, a


def butter_lowpass_coefficients(freqmax, sampling_rate, order=4.):
    """
    :param freqmin:
    :param freqmax:
    :param sampling_rate:
    :param order:
    :return:
    """
    nyq = 0.5 * sampling_rate
    b, a = butter(order, [freqmax / nyq], btype='low')
    return b, a


def butter_highpass_coefficients(freqmin, sampling_rate, order=4.):
    """
    :param freqmin:
    :param freqmax:
    :param sampling_rate:
    :param order:
    :return:
    """
    nyq = 0.5 * sampling_rate
    b, a = butter(order, [freqmin / nyq], btype='high')
    return b, a


# ---- apply filter from coefficients or frequency response
def butter_filter(data, b, a, axis=-1):
    """
    apply butterworth filter to time domain data

    :param data:
    :param b:
    :param a:
    :param axis:
    :return:
    """
    filtered_data = lfilter(b, a, data, axis=axis)
    return filtered_data


# ---- high level filters
def bandpass(data, freqmin, freqmax, sampling_rate, order, zerophase=False):
    """
    equivalent to obspy bandpass
    :param data: 
    :param freqmin: 
    :param freqmax: 
    :param order: 
    :return: 
    """
    b, a = butter_bandpass_coefficients(freqmin, freqmax, sampling_rate, order)
    filtered_data = butter_filter(data, b, a)
    if zerophase:
        filtered_data = butter_filter(filtered_data[::-1], b, a)[::-1]
    return filtered_data


def lowpass(data, freqmax, sampling_rate, order, zerophase=False):
    """
    equivalent to obspy bandpass
    :param data:
    :param freqmax:
    :param order:
    :return:
    """
    b, a = butter_lowpass_coefficients(freqmax, sampling_rate, order)
    filtered_data = butter_filter(data, b, a)
    if zerophase:
        filtered_data = butter_filter(filtered_data[::-1], b, a)[::-1]
    return filtered_data


def highpass(data, freqmin, sampling_rate, order, zerophase=False):
    """
    equivalent to obspy bandpass
    :param data:
    :param freqmin:
    :param order:
    :return:
    """
    b, a = butter_highpass_coefficients(freqmin, sampling_rate, order)
    filtered_data = butter_filter(data, b, a)
    if zerophase:
        filtered_data = butter_filter(filtered_data[::-1], b, a)[::-1]
    return filtered_data
