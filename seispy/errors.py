class DataAvailabilityError(Exception):
    """all errors due to missing data"""
    pass


class DataTypeError(Exception):
    pass


# traces in broad sense
class MissingResponseError(Exception):
    pass


class SamplingError(Exception):
    """for all errors related to sampling"""
    pass


class SamplingRateError(SamplingError):
    """for all errors related to sampling rate"""
    pass


class NptsError(SamplingError):
    """for all errors related to number of samples"""
    pass


class StarttimeError(SamplingError):
    """for all errors related to inconsistent starttimes"""
    pass


class EndtimeError(SamplingError):
    """for all errors related to inconsistent starttimes"""
    pass


class TraceIdError(Exception):
    """for inconsistent ids between waveforms"""
    pass


class CoordinateError(Exception):
    """for inconsistent coordinates"""
    pass


class ComponentLetterError(Exception):
    """
    error related to the letter (Z, N, E, R, T) of a channel
    """
    pass


class TrimmingError(Exception):
    pass


class TrimmingWindowError(Exception):
    pass


class CoordinatesError(Exception):
    pass


# streams
class EmptyStreamError(Exception):
    pass


class TooFewTracesInStreamError(Exception):
    pass
