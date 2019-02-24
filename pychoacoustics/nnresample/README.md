# nnresample
A resampling function based on placing the filter's first null on Nyquist (Null-on-Nyquist Resample)

This package provides a sample rate converter which is basically a wrapper around
`scipy.signal.resample_poly`, replacing the default filter with one of much higher order
and with the special feature that the cutoff frequency of the antialias filter is set
such that the first null (the point where the main lobe ends and the first side lobe
begins) falls on the Nyquist frequency (half of the sampling rate).  Thus the name
'nnresample" for "Null-on-Nyquist Resample" --- the alternate name
"nonresample" was deemed too confusing.

Please report bugs at https://github.com/jthiem/nnresample

This code is licensed under a Creative Commons Attribution 3.0 Unported (CC BY 3.0)
License (https://creativecommons.org/licenses/by/3.0/)

## Usage

```
import nnresample

newsound = nnresample.resample(sound, newsampleratre, oldsamplerate)
```

## Detailed function description

The functions are written with the assumption that once a particular set of
resampling parameters is chosen, you'll be wanting to use that filter again.
Since finding the null takes more time than just calculating a filter the default
way, a filter used once is not recalculated.  For the most part, this happens
behind the scenes, and you can just call `nnresample.resample()` without
restrictions - the first call with a particular set of parameters will take longer
but subsequent calls will be faster.

If you want to handle the filter coefficients yourself and call
`scipy.signal.resample_poly` yourself with the `window=` parameter (this may
also be useful if you want to use the same filter across multiple
invocations of python and just store the filter in a file), you can call the
`nnresample.compute_filt()` function, which returns the windowed sinc
FIR filter. *** Note the workaround for the bug in scipy ***

```
    resample(s, up, down, axis=0, fc='nn', **kwargs):

    Resample a signal from rate "down" to rate "up"

    Parameters
    ----------
    s : array_like
        The data to be resampled.
    up : int
        The upsampling factor.
    down : int
        The downsampling factor.
    axis : int (optional)
        The axis of `x` that is resampled. Default is 0.
    fc : float (optional)
        cutoff frequency relative to Nyquist (fs/2) or
        type of calculation ('nn', 'standard' or 'kaiser')
        Default 'nn'.
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
    determined entirely by up, down, beta, and L.  If a filter
    has previously been used it is looked up instead of being
    recomputed.
```
```
    compute_filt(up, down, fc='nn', beta=5.0, N=32001, return_fc=False):

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

    out = scipy.signal.resample_poly(in, up, down, window=numpy.array(filt))
```