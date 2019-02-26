from __future__ import division
from numpy import ceil
from scipy.optimize import brentq
import logging

def beta_from_As(As):
    r"""
    Find beta given the stopband attenuation (in dB)

    Parameters
    ----------
    As : float
        Stopband attenuation in dB

    Returns
    -------
    beta : float
        The computed beta

    This is a standard formula from Kaiser."""

    if As>50:
        return 0.1102*(As-8.7)
    elif As>21:
        return 0.5842*(As-21)**0.4 + 0.07886*(As-21)
    else:
        return 0.0

def As_from_beta(beta):
    r"""
    Find stopband attenuation given beta

    Parameters
    ----------
    beta : float
        The Kaiser window beta parameter

    Returns
    -------
    As : float
        The computed stopband attenuation in dB

    Notes
    -----
    For beta <= 0 we simply return 21. beta<0 makes no sense, but
    returning something is better than throwing an exception.

    The "forward" formula is linear for As>50.  That is easy to
    handle since the formula is monotonic to boot.

    In between though, there is no easy way to my knowledge.
    So, I use a root finder from scipy.
    """
    if beta<=0:
        return 21.0
    if beta>beta_from_As(50):
        return 9.07441*beta+8.7

    return brentq(lambda x: beta_from_As(x)-beta, 0, 50, xtol=0.001, rtol=1e-5)

def disambiguate_params(As=None, N=None, df=None, beta=None):
    r"""
    Disambiguate the parameters passed to the resampler.

    Parameters
    ----------
    As : float
        Stopband attenuation in dB
    N : float
        Filter order (length of impulse response in samples)
    df : float
        Transition band width, normalized to Nyquist (fs/2)
    beta : float
        The beta parameter of the Kaiser window

    Returns
    -------
    N, beta, As: tuple(int, float, float)
        The computed parameters to generate the window

    Notes
    -----
    We need two parameters to specify the window, but the ones we
    need to calculate it are not the natural ones we might want to
    specify.  So, we need to figure out N and beta from the parmeters
    given: beta is directly related to the stopband attenuation, but
    the window lenght is a function of the transition band width and the
    stopband attenuation.

    If beta and As (the stopband attenuation in dB) are given, As is used.
    If neither is given, assume As = 60 dB.

    If N is not given, we can compute it from a desired transition band
    width (and the stopband attenuation), else we use a default of
    32001 samples.

    There is one edge case which rare, but is handled first: beta can be
    derived (via As) if N and df ONLY are given.
    """
    default_N = 32001
    default_As = 60

    if beta is None:
        if As is None:
            if N is not None and df is not None:
                As = 14.36*df*N + 7.95
            else:
                As = default_As
        beta = beta_from_As(As)
    elif As is not None:
        logging.warning('Both beta and the stopband attenuation specified. Stopband attenuation used.')
        beta = beta_from_As(As)
    else:
        # beta is given, but As is not.  To compute the width of the transition
        # band we need to get As.
        As = As_from_beta(beta)

    assert(beta is not None)
    assert(As is not None)

    if N is None:
        if df is not None:
            N = ceil((As-7.95)/14.36*df)
        else:
            N = default_N

    return N, beta, As
