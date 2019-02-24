from __future__ import division
import scipy.signal as sig
import numpy as np
from .utility import disambiguate_params, As_from_beta

try:
    from math import gcd
except:
    from fractions import gcd

# global cache of resamplers
_precomputed_filters = {}

def compute_filt(up, down, fc='nn', beta=5.0, N=32001, return_fc=False):
    r"""
    Computes a filter to resample a signal from rate "down" to rate "up"

    Parameters
    ----------
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    fc : float or string (optional)
        cutoff frequency (normalized to Nyquist, f_s/2) or type
        of method to determine fc.  Options are "nn" (null-on-Nyquist),
        'kaiser' (edge of transition band as given by formula by Kaiser),
        or 'standard' (middle of transition band).
    beta : float (optional)
        Beta factor for Kaiser window.  Determines tradeoff between
        stopband attenuation and transition band width
    N : int (optional)
        FIR filter order.  Determines stopband attenuation.  The higher
        the better, ath the cost of complexity.
    return_fc : bool
        If true, fc (the numerical value) is returned as well. Default false.

    Returns
    -------
    filt : array
        The FIR filter coefficients

    Notes
    -----
    This function is to be used if you want to manage your own filters
    to be used with scipy.signal.resample_poly (use the `window=...`
    parameter).  WARNING: Some versions (at least 0.19.1) of scipy
    modify the passed filter, so make sure to make a copy beforehand:

    out = scipy.signal.resample_poly(in up, down, window=numpy.array(filt))
    """

    # Determine our up and down factors
    g = gcd(up, down)
    up = up//g
    down = down//g
    max_rate = max(up, down)

    sfact = np.sqrt(1+(beta/np.pi)**2)

    if isinstance(fc, float):
        pass

    # the "standard" way to generate the filter is to just place fc on the
    # Nyquist frequency, which results in considerable aliasing but is
    # neccesary for perfect reconstruction multirate filterbanks but not
    # for audio resampling!  Included here mostly for completeness and
    # comparison purposes.
    elif fc == 'standard':
        fc = 1/max_rate

    # The paper by Kaiser gives a formula for the neccesary length of the
    # filter given a desired stopband attenuation and transition band width;
    # conversly, we can determine the transition band width from the stop
    # band attenuation and filter length.  This allows us to shift fc.
    elif fc == 'kaiser' or fc == 'Kaiser':
        As = As_from_beta(beta)
        offset = (As-7.95)/(14.36*N)
        fc = (1/max_rate)-offset

    # The null-on-Nyquist method: the reason I wrote this package in the first
    # place.  My argument is that the cutoff frequency should be on the border
    # between the main lobe of the filter and the first sidelobe; this should
    # give the best tradeoff between retaining the desired signal and
    # suppressing aliasing.
    elif fc == 'nn':
        # This is a two-step procedure.  First we generate a filter in the
        # 'normal' way: with 6dB attenuation at Falsef_c.
        init_filt = sig.fir_filter_design.firwin(N, 1/max_rate,
                                                 window=('kaiser', beta))

        # Next, find the first null. Convert the filter into frequency domain.
        N_FFT = 2**19
        NBINS = N_FFT/2+1
        paddedfilt = np.zeros(N_FFT)
        paddedfilt[:N] = init_filt
        ffilt = np.fft.rfft(paddedfilt)

        # Now find the minimum between f_c and f_c+sqrt(1+(beta/pi)^2)/L
        bot = int(np.floor(NBINS/max_rate))
        top = int(np.ceil(NBINS*(1/max_rate + 2*sfact/N)))
        firstnull = (np.argmin(np.abs(ffilt[bot:top])) + bot)/NBINS

        # get the new fc
        fc = -firstnull+2/max_rate

    else:
        raise ValueError('Unknown option for fc in compute_filt')

    # Now we can generate the desired filter
    f = sig.fir_filter_design.firwin(N, fc, window=('kaiser', beta))

    if return_fc:
        return f, fc
    else:
        return f

def resample(s, up, down, axis=0, fc='nn', **kwargs):
    r"""
    Resample a signal from rate "down" to rate "up"

    Parameters
    ----------
    s : array_like
        The data to be resampled.
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    axis : int, optional
        The axis of `x` that is resampled. Default is 0.
    As : float (optional)
        Stopband attenuation in dB
    N : float (optional)
        Filter order (length of impulse response in samples)
    df : float (optional)
        Transition band width, normalized to Nyquist (fs/2)
    beta : float (optional)
        The beta parameter of the Kaiser window

    Returns
    -------
    resampled_x : array
        The resampled array.

    Notes
    -----
    The function keeps a global cache of filters, since they are
    determined entirely by up, down, fc, beta, and L.  If a filter
    has previously been used it is looked up instead of being
    recomputed.
    """

    # from design parameters, find the generative parameters
    N, beta, As = disambiguate_params(**kwargs)

    # check if a resampling filter with the chosen parameters already exists
    params = (up, down, fc, beta, N)
    if params in _precomputed_filters.keys():
        # if so, use it.
        filt = _precomputed_filters[params]
    else:
        # if not, generate filter, store it, use it
        filt = compute_filt(up, down, fc, beta=beta, N=N)
        _precomputed_filters[params] = filt

    return sig.resample_poly(s, up, down, window=np.array(filt), axis=axis)
