# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2020 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of sndlib

#    sndlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    sndlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with sndlib.  If not, see <http://www.gnu.org/licenses/>.

"""
A module for generating sounds in python.
"""

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import copy, numpy, multiprocessing, warnings
from numpy import abs, angle, arange, array, asarray, ceil, concatenate, convolve, cos, cumsum, floor, int_, int64, log, log2, log10, linspace, logspace, mean, ones, pi, real, repeat, sin, sqrt, where, zeros
from numpy.fft import fft, ifft, irfft, rfft
from scipy.signal import firwin2
import scipy


def addSounds(snd1, snd2, delay, fs):
    """
    Add or concatenate two sounds.

    Parameters
    ----------
    snd1 : array of floats
        First sound.
    snd2 : array of floats
        Second sound.
    delay : float
        Delay in milliseconds between the onset of 'snd1' and the onset of 'snd2'
    fs : float
        Sampling frequency in hertz of the two sounds.

    Returns
    --------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> snd1 = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> snd2 = pureTone(frequency=880, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> snd = addSounds(snd1=snd1, snd2=snd2, delay=100, fs=48000)
    """
  
    #delay in ms
    delay = delay / 1000 #convert from ms to sec

    nSnd1 = len(snd1[:,1])
    nSnd2 = len(snd2[:,1])
    snd1Duration = nSnd1/fs
    snd2Duration = nSnd2/fs

    #------------------------
    #            ...............................

    # Seg1           Seg2              Seg3
    
    nSampSeg1 = round(delay * fs)
    if nSampSeg1 < nSnd1:
        nSampSeg2 = nSnd1 - nSampSeg1
        nSampSeg3 = nSnd2 - nSampSeg2
        seg1 = snd1[0:nSampSeg1,:]
        seg2a = snd1[nSampSeg1:nSnd1,:]
        if nSampSeg2 > nSnd2: # snd2 shorter than seg2, fill with zeros
            ldiff = nSampSeg2 - nSnd2
            diffSeg = zeros((ldiff, 2))
            seg2b = concatenate((snd2, diffSeg), axis=0)
        else:
            seg2b = snd2[0:nSampSeg2,:]
            seg3 = snd2[nSampSeg2:nSnd2,:]

        seg2 = seg2a+seg2b
        snd = concatenate((seg1, seg2), axis=0)

        if nSampSeg2 < nSnd2:
            snd = concatenate((snd, seg3), axis=0)
            
    else:
        seg1 = snd1
        seg2 = makeSilence((delay - snd1Duration)*1000, fs)
        seg3 = snd2
        snd = concatenate((seg1, seg2), axis=0)
        snd = concatenate((snd, seg3), axis=0)
        
    return snd

def AMTone(frequency=1000, AMFreq=20, AMDepth=1, phase=0, AMPhase=0, level=60,
           duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate an amplitude modulated tone.

    Parameters
    ----------
    frequency : float
        Carrier frequency in hertz.
    AMFreq : float
        Amplitude modulation frequency in Hz.
    AMDepth : float
        Amplitude modulation depth (a value of 1
        corresponds to 100% modulation). 
    phase : float
        Starting phase in radians.
    AMPhase : float
        Starting AM phase in radians.
    level : float
        Average tone level in dB SPL. See notes.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats

    Notes
    ------
    For a fixed base amplitude, the average power of an AM tone (as defined in this function) increases proportionally with AM depth by a factor of 1+AMDepth^2/2 (Viemeister, 1979, Yost et al., 1989, Hartmann, 2004). This function compensates for this average increase in power. You can use the `AMToneVarLev` function if you want to generate AM tones varying in average power with AM depth.

    References
    ----------
    .. [H] Hartmann, W. M. (2004). Signals, Sound, and Sensation. Springer Science & Business Media
    .. [V79] Viemeister, N. F. (1979). Temporal modulation transfer functions based upon modulation thresholds. The Journal of the Acoustical Society of America, 66(5), 1364–1380. https://doi.org/10.1121/1.383531
    .. [YSO] Yost, W., Sheft, S., & Opie, J. (1989). Modulation interference in detection and discrimination of amplitude modulation. The Journal of the Acoustical Society of America, 86(December 1989), 2138–2147. https://doi.org/10.1121/1.398474
       
    Examples
    --------
    >>> snd = AMTone(frequency=1000, AMFreq=20, AMDepth=1, phase=0, 
    ...     AMPhase=1.5*pi, level=65, duration=180, ramp=10, channel='Both', 
    ...     fs=48000, maxLevel=100)
    
    """        

    duration = duration / 1000 #convert from ms to sec
    
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp/1000 * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))

    if channel == "Right":
        snd[:, 1] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+AMPhase)) * sin(2*pi*frequency * timeAll[:] + phase)
    elif channel == "Left":
        snd[:, 0] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+AMPhase)) * sin(2*pi*frequency * timeAll[:] + phase)
    elif channel == "Both":
        snd[:, 0] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+AMPhase)) * sin(2*pi*frequency * timeAll[:] + phase)
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left' or 'Both'")

    snd = setLevel_(level, snd, maxLevel, channel=channel)
    snd = gate(ramp, snd, fs)

    return snd


def AMToneVarLev(frequency=1000, AMFreq=20, AMDepth=1, phase=0, AMPhase=0, level=60,
                 duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate an amplitude modulated (AM) tone.

    Parameters
    ----------
    frequency : float
        Carrier frequency in hertz.
    AMFreq : float
        Amplitude modulation frequency in Hz.
    AMDepth : float
        Amplitude modulation depth (a value of 1
        corresponds to 100% modulation). 
    phase : float
        Starting phase in radians.
    AMPhase : float
        Starting AM phase in radians.
    level : float
        Average level of the tone in dB SPL when the `AMDepth` is zero. The level of the tone will be higher when `AMDepth` is > zero. See notes. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats

    Notes
    ------
    For a fixed base amplitude, the average power of an AM tone (as defined in this function) increases proportionally with AM depth by a factor of 1+AMDepth^2/2 (Viemeister, 1979, Yost et al., 1989, Hartmann, 2004). This function does not compensate for this average increase in power. You can use the `AMTone` function if you want to generate AM tones matched in average power irrespective of AM depth.

    References
    ----------
    .. [H] Hartmann, W. M. (2004). Signals, Sound, and Sensation. Springer Science & Business Media
    .. [V79]Viemeister, N. F. (1979). Temporal modulation transfer functions based upon modulation thresholds. The Journal of the Acoustical Society of America, 66(5), 1364–1380. https://doi.org/10.1121/1.383531
    .. [YSO] Yost, W., Sheft, S., & Opie, J. (1989). Modulation interference in detection and discrimination of amplitude modulation. The Journal of the Acoustical Society of America, 86(December 1989), 2138–2147. https://doi.org/10.1121/1.398474
       
    Examples
    --------
    >>> snd = AMToneVarLev(frequency=1000, AMFreq=20, AMDepth=1, phase=0, 
    ...       AMPhase=1.5*pi, level=65, duration=180, ramp=10, channel='Both', 
    ...       fs=48000, maxLevel=100)
    
    """        

    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))

    if channel == "Right":
        snd[0:nRamp, 1] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[0:nRamp]+AMPhase)) * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 1] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp:nRamp+nSamples]+AMPhase)) * sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:nTot, 1] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp+nSamples:nTot]+AMPhase)) * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:nTot] + phase)
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[0:nRamp]+AMPhase)) * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp:nRamp+nSamples]+AMPhase)) * sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:nTot, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp+nSamples:nTot]+AMPhase)) * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:nTot] + phase)
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[0:nRamp]+AMPhase)) * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp:nRamp+nSamples]+AMPhase)) * sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:nTot, 0] = amp * (1 + AMDepth*sin(2*pi*AMFreq*timeAll[nRamp+nSamples:nTot]+AMPhase)) * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:nTot] + phase)
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left' or 'Both'")
       
    return snd


def AMToneIPD(frequency=1000, AMFreq=20, AMDepth=1, phase=0, AMPhase=0,
              phaseIPD=0, AMPhaseIPD=0, level=60, duration=980, ramp=10,
              channel="Right", fs=48000, maxLevel=101):
    """
    Generate an amplitude modulated tone with an interaural
    phase difference (IPD) in the carrier and/or modulation phase.

    Parameters
    ----------
    frequency : float
        Carrier frequency in hertz.
    AMFreq : float
        Amplitude modulation frequency in Hz.
    AMDepth : float
        Amplitude modulation depth (a value of 1
        corresponds to 100% modulation). 
    phase : float
        Starting phase in radians.
    AMPhase : float
        Starting AM phase in radians.
    phaseIPD : float
        IPD to apply to the carrier phase.
    AMPhaseIPD : float
        IPD to apply to the modulation phase.
    level : float
        Average tone level in dB SPL. See notes.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left')
        Channel in which the phase will be shifted.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats

    Notes
    ------
    For a fixed base amplitude, the average power of an AM tone (as defined in this function) increases proportionally with AM depth by a factor of 1+AMDepth^2/2 (Viemeister, 1979, Yost et al., 1989, Hartmann, 2004). This function does not compensate for this average increase in power. You can use the `AMTone` function if you want to generate AM tones matched in average power irrespective of AM depth.

    References
    ----------
    .. [H] Hartmann, W. M. (2004). Signals, Sound, and Sensation. Springer Science & Business Media
    .. [V79] Viemeister, N. F. (1979). Temporal modulation transfer functions based upon modulation thresholds. The Journal of the Acoustical Society of America, 66(5), 1364–1380. https://doi.org/10.1121/1.383531
    .. [YSO] Yost, W., Sheft, S., & Opie, J. (1989). Modulation interference in detection and discrimination of amplitude modulation. The Journal of the Acoustical Society of America, 86(December 1989), 2138–2147. https://doi.org/10.1121/1.398474
       
    Examples
    --------
    >>> snd = AMToneIPD(frequency=1000, AMFreq=20, AMDepth=1, phase=0, AMPhase=1.5*pi,
    ...     phaseIPD=0, AMPhaseIPD=pi, level=65, 
    ...     duration=180, ramp=10, channel='Right', fs=48000, maxLevel=100)
    
    """

    nSamples = int(round(duration/1000 * fs))
    nRamp = int(round(ramp/1000 * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs

    snd = zeros((nTot, 2))

    shiftedPhase = phase+phaseIPD
    shiftedAMPhase = AMPhase+AMPhaseIPD
    #print(shiftedPhase-phase, shiftedAMPhase-AMPhase)

    if channel == "Right":
        snd[:, 1] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+shiftedAMPhase)) * sin(2*pi*frequency * timeAll[:] + shiftedPhase)
        snd[:, 0] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+AMPhase)) * sin(2*pi*frequency * timeAll[:] + phase)

    elif channel == "Left":
        snd[:, 1] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+AMPhase)) * sin(2*pi*frequency * timeAll[:] + phase)
        snd[:, 0] = (1 + AMDepth*sin(2*pi*AMFreq*timeAll[:]+shiftedAMPhase)) * sin(2*pi*frequency * timeAll[:] + shiftedPhase)

    else:
        raise ValueError("Invalid channel argument. Channel must be either 'Right' or 'Left'")
  
    snd = setLevel_(level, snd, maxLevel, channel="Both")
    snd = gate(ramp, snd, fs)
    
    return snd


def binauralPureTone(frequency=1000, phase=0, level=60, duration=980, ramp=10, channel="Both", itd=0, itdRef="Right", ild=10, ildRef="Right", fs=48000, maxLevel=101):
    """
    Generate a pure tone with an optional interaural time or level difference.

    Parameters
    ----------
    frequency : float
        Tone frequency in hertz.
    phase : float
        Starting phase in radians.
    level : float
        Tone level in dB SPL. If 'ild' is different than zero, this will
        be the level of the tone in the reference channel.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    itd : float
        Interaural time difference, in microseconds.
    itdRef : 'Right', 'Left' or None
        The reference channel for the 'itd'. The interaural time
        difference will be applied to the other channel with
        respect to the reference channel.
    ild : float
        Interaural level difference in dB SPL.
    ildRef : 'Right', 'Left' or None
        The reference channel for the 'ild'.
        The level of the other channel will be
        icreased of attenuated by 'ild' dB SPL
        with respect to the reference channel.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       
    Examples
    --------
    >>> itdTone = binauralPureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Both', itd=480, itdRef='Right', ild=0, ildRef=None,
    ...     fs=48000, maxLevel=100)
    >>> ildTone = binauralPureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Both', itd=0, itdRef=None, ild=-20, ildRef='Right',
    ...     fs=48000, maxLevel=100)
    
    """
        
    if itdRef not in ["Right", "Left", None]:
        raise ValueError("Invalid 'itdRef' argument. 'itdRef' must be one of 'Right', 'Left' or None")
    if ildRef not in ["Right", "Left", None]:
        raise ValueError("Invalid 'ildRef' argument. 'ildRef' must be one of 'Right', 'Left' or None")
    
    if itd != 0 and itdRef == None:
        warnings.warn("'itd' is different than zero but no 'itdRef' was given. No 'itd' will be applied.")
    if ild != 0 and ildRef == None:
        warnings.warn("'ild' is different than zero but no 'ildRef' was given. No 'ild' will be applied.")

    
    if channel == 'Both':
        ipd = itdtoipd(itd/1000000, frequency)
        if ildRef == 'Right':
            ampRight = 10**((level - maxLevel) / 20)
            ampLeft = 10**((level + ild - maxLevel) / 20)
        elif ildRef == 'Left':
            ampLeft = 10**((level - maxLevel) / 20)
            ampRight = 10**((level + ild - maxLevel) / 20)
        elif ildRef == None:
            ampRight = 10**((level - maxLevel) / 20)
            ampLeft = ampRight

        if itdRef == 'Right':
            phaseRight = phase
            phaseLeft = phase + ipd
        elif itdRef == 'Left':
            phaseLeft = phase
            phaseRight = phase + ipd
        elif itdRef == None:
            phaseRight = phase
            phaseLeft = phase
    else:
        amp = 10**((level - maxLevel) / 20.)
            
    duration = duration / 1000. #convert from ms to sec
    ramp = ramp / 1000.

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0., nTot) / fs
    timeRamp = arange(0., nRamp) 

    snd = zeros((nTot, 2))


    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phase)
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phase)
    elif channel == "Both":
        snd[0:nRamp, 0] = ampLeft * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phaseLeft)
        snd[nRamp:nRamp+nSamples, 0] = ampLeft* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phaseLeft)
        snd[nRamp+nSamples:len(timeAll), 0] = ampLeft * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phaseLeft)

        snd[0:nRamp, 1] = ampRight * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phaseRight)
        snd[nRamp:nRamp+nSamples, 1] = ampRight* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phaseRight)
        snd[nRamp+nSamples:len(timeAll), 1] = ampRight * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phaseRight)
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left' or 'Both'")


    return snd


def broadbandNoise(spectrumLevel=25, duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a broadband noise.

    Parameters
    ----------
    spectrumLevel : float
        Intensity spectrum level of the noise in dB SPL. 
    duration : float
        Noise duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ("Right", "Left", "Both", or "Dichotic")
        Channel in which the noise will be generated. If 'Both' the
        same noise will be generated in both channels. If 'Dichotic'
        the noise will be independent at the two ears.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       
    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel="Both", fs=48000, maxLevel=100)
    
    """
    """ Comments:.
    The intensity spectrum level in dB is ISL
    The peak amplitude A to achieve a desired ISL is
    ISL = 10*log10(A^2/NHz) that is the total intensity (A^2) divided by the freq band
    ISL/10 = log10(A^2/NHz)
    10^(ISL/10) = A^2/NHz
    A^2 = 10^(ISL/10) * NHz
    A = 10^(ISL/20) * sqrt(NHz)
    NHz = sampRate / 2 (Nyquist)
    
    """
    amp = sqrt(fs/2)*(10**((spectrumLevel - maxLevel) / 20))
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    snd_mono = zeros(nTot)
    #random is a numpy module
    noise = (numpy.random.random(nTot) + numpy.random.random(nTot)) - (numpy.random.random(nTot) + numpy.random.random(nTot))
    RMS = sqrt(mean(noise*noise))
    #noise/RMS would scale the noise so that its RMS = 1
    #noise/(RMS*sqrt(2)) scales the noise so that its RMS equals the RMS of a sinusoid with peak amplitude 1 (that is 1/sqrt(2))
    scaled_noise = noise / (RMS * sqrt(2))

    snd_mono[0:nRamp] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise[0:nRamp]
    snd_mono[nRamp:nRamp+nSamples] = amp * scaled_noise[nRamp:nRamp+nSamples]
    snd_mono[nRamp+nSamples:len(timeAll)] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise[nRamp+nSamples:len(timeAll)]

    if channel == "Dichotic":
        snd_mono2 = zeros(nTot)
        noise2 = (numpy.random.random(nTot) + numpy.random.random(nTot)) - (numpy.random.random(nTot) + numpy.random.random(nTot))
        RMS = sqrt(mean(noise2*noise2))
        #scale the noise so that its RMS = 1
        #since A = RMS*sqrt(2)
        scaled_noise2 = noise2 / (RMS * sqrt(2))

        snd_mono2[0:nRamp] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise2[0:nRamp]
        snd_mono2[nRamp:nRamp+nSamples] = amp * scaled_noise2[nRamp:nRamp+nSamples]
        snd_mono2[nRamp+nSamples:len(timeAll)] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise2[nRamp+nSamples:len(timeAll)]
        
    if channel == "Right":
        snd[:,1] = snd_mono
    elif channel == "Left":
        snd[:,0] = snd_mono
    elif channel == "Both":
        snd[:,1] = snd_mono
        snd[:,0] = snd_mono
    elif channel == "Dichotic":
        snd[:,1] = snd_mono
        snd[:,0] = snd_mono2
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', 'Both', or 'Dichotic'")
        
    return snd

def camSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=5, deltaCams=1, fmPhase=pi, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a complex tone frequency modulated with an exponential sinusoid.

    Parameters
    ----------
    F0 : float
        Fundamental aarrier frequency in hertz.
    lowHarm: int
        Lowest harmonic number.
    highHarm: int
        Highest harmonic number.
    harmPhase: string
        Harmonic phase relationship. One of 'Sine', 'Cosine', or 'Alternating'.
    fm : float
        Modulation frequency in Hz.
    deltaCams : float
        Frequency excursion in cam units (ERBn number scale). 
    fmPhase : float
        Starting fmPhase in radians.
    level : float
        Tone level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> snd_peak = camSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=5, deltaCams=1, fmPhase=pi, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=100)
    >>> snd_trough = camSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=5, deltaCams=1, fmPhase=0, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=100)
    
    """
    for i in range(int(lowHarm), int(highHarm)+1):
        if harmPhase == "Sine":
            startPhase = 0
        elif harmPhase == "Cosine":
            startPhase = pi/2
        elif harmPhase == "Alternating":
            if i%2 > 0: #odd harmonic
                startPhase = 0
            else:
                startPhase = pi/2
        else:
            raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one of 'Sine', 'Cosine', or 'Alternating'")
        
        if i == lowHarm:
            snd = camSinFMTone(F0*i, fm, deltaCams, fmPhase, startPhase, level, duration, ramp, channel, fs, maxLevel)
        else:
            snd = snd + camSinFMTone(F0*i, fm, deltaCams, fmPhase, startPhase, level, duration, ramp, channel, fs, maxLevel)
        
    return snd


def camSinFMTone(fc=450, fm=5, deltaCams=1, fmPhase=pi, startPhase=0, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=100):
    """
    Generate a tone frequency modulated with an exponential sinusoid.

    Parameters
    ----------
    fc : float
        Carrier frequency in hertz. 
    fm : float
        Modulation frequency in Hz.
    deltaCams : float
        Frequency excursion in cam units (ERBn number scale). 
    fmPhase : float
        Starting fmPhase in radians.
    level : float
        Tone level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> tone_peak = camSinFMTone(fc=450, fm=5, deltaCams=1, fmPhase=pi, startPhase=0, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=100)
    >>> tone_trough = camSinFMTone(fc=450, fm=5, deltaCams=1, fmPhase=0, startPhase=0, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=100)
    
    """
  
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)
    #fArr = 2*pi*fc*2**((deltaCents/1200)*cos(2*pi*fm*timeAll+fmPhase))
    fArr = 2*pi*freqFromERBInterval(fc, deltaCams*cos(2*pi*fm*timeAll+fmPhase)) 
    ang = (cumsum(fArr)/fs) + startPhase

    snd = zeros((nTot, 2))

    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both'")
       

    return snd

def chirp(freqStart=440, ftype="linear", rate=500, level=60, duration=980, phase=0, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetize a chirp, that is a tone with frequency changing linearly or
    exponentially over time with a give rate.
    

    Parameters
    ----------
    freqStart : float
        Starting frequency in hertz.
    ftype : string
        If 'linear', the frequency will change linearly on a Hz scale.
        If 'exponential', the frequency will change exponentially on a cents scale.
    rate : float
        Rate of frequency change, Hz/s if ftype is 'linear',
        and cents/s if ftype is 'exponential'.
    level : float
        Level of the tone in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       
    Examples
    --------
    >>> gl = chirp(freqStart=440, ftype='linear', rate=500, level=55,
            duration=980, phase=0, ramp=10, channel='Both',
            fs=48000, maxLevel=100)

    """
    
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000
    totDur = duration+ramp*2
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)
    if ftype == "exponential":
        k = 2**(rate/1200)
        frequency = freqStart*( ( ( (k**timeAll) - 1) /log(k) + phase) )
    elif ftype == "linear":
        frequency = freqStart*timeAll + (rate/2)*timeAll**2 + phase
    else:
        raise ValueError("Invalid ftype argument. 'ftype' must be either 'linear', or 'exponential'")


    snd = zeros((nTot, 2))

    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[0:nRamp] )
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(2*pi*frequency[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[nRamp+nSamples:len(timeAll)])
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[0:nRamp] )
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*frequency[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[nRamp+nSamples:len(timeAll)])
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[0:nRamp] )
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*frequency[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency[nRamp+nSamples:len(timeAll)])
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both'")

    return snd


def complexTone(F0=220, harmPhase="Sine", lowHarm=1, highHarm=10, stretch=0, level=60, duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a complex tone.

    Parameters
    ----------
    F0 : float
        Tone fundamental frequency in hertz.
    harmPhase : one of 'Sine', 'Cosine', 'Alternating', 'Random', 'Schroeder-', 'Schroeder+'
        Phase relationship between the partials of the complex tone.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    stretch : float
        Harmonic stretch in %F0. Increase each harmonic frequency by a fixed value
        that is equal to (F0*stretch)/100. If 'stretch' is different than
        zero, an inhanmonic complex tone will be generated.
    level : float
        The level of each partial in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left', 'Both', 'Odd Right' or 'Odd Left'
        Channel in which the tone will be generated. If 'channel'
        if 'Odd Right', odd numbered harmonics will be presented
        to the right channel and even number harmonics to the left
        channel. The opposite is true if 'channel' is 'Odd Left'.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
    >>> ct = complexTone(F0=440, harmPhase='Sine', lowHarm=3, highHarm=10,
    ...     stretch=0, level=55, duration=180, ramp=10, channel='Both',
    ...     fs=48000, maxLevel=100)
    
    """
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000. #convert from ms to sec
    ramp = ramp / 1000
    stretchHz = (F0*stretch)/100
    
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)
    
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    if channel == "Right" or channel == "Left" or channel == "Both":
        tone = zeros(nTot)
    elif channel == "Odd Left" or channel == "Odd Right":
        toneOdd = zeros(nTot)
        toneEven = zeros(nTot)

    if harmPhase == "Sine":
        for i in range(lowHarm, highHarm+1):
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone =  tone + sin(2 * pi * ((F0 * i) + stretchHz) * timeAll)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd = toneOdd + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                else:
                    toneEven = toneEven + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll)
    elif harmPhase == "Cosine":
        for i in range(lowHarm, highHarm+1):
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone = tone + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd = toneOdd + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                else:
                    toneEven = toneEven + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
    elif harmPhase == "Alternating":
        for i in range(lowHarm, highHarm+1):
            if i%2 > 0: #odd harmonic
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                elif channel == "Odd Left" or channel == "Odd Right":
                    toneOdd = toneOdd + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
            else: #even harmonic
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                elif channel == "Odd Left" or channel == "Odd Right":
                    toneEven = toneEven + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll)
    elif harmPhase == "Schroeder-":
        for i in range(lowHarm, highHarm+1):
            phase = -pi*i*(i - 1)/(highHarm-lowHarm+1)
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd = toneOdd + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
                else:
                    toneEven = toneEven + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
    elif harmPhase == "Schroeder+":
        for i in range(lowHarm, highHarm+1):
            phase = pi*i*(i - 1)/(highHarm-lowHarm+1)
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd = toneOdd + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
                else:
                    toneEven = toneEven + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
    elif harmPhase == "Random":
        for i in range(lowHarm, highHarm+1):
            phase = numpy.random.random() * 2 * pi
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd = toneOdd + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
                else:
                    toneEven = toneEven + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
    else:
        raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one 'Sine', 'Cosine', 'Alternating', 'Schroeder-', 'Schroeder+', or 'Random'")


    if channel == "Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:len(timeAll)]
    elif channel == "Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:len(timeAll)]
    elif channel == "Both":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:len(timeAll)]
        snd[:, 1] = snd[:, 0]
    elif channel == "Odd Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:len(timeAll)]
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:len(timeAll)]
    elif channel == "Odd Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:len(timeAll)]
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:len(timeAll)]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', 'Both', 'Odd Left', or 'Odd Right'")
        

    return snd


def complexToneParallel(F0=220, harmPhase="Sine", lowHarm=1, highHarm=10, stretch=0, level=0, duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a complex tone.

    This function produces the same results of complexTone. The only difference
    is that it uses the multiprocessing Python module to exploit multicore
    processors and compute the partials in a parallel fashion. Notice that
    there is a substantial overhead in setting up the parallel computations.
    This means that for relatively short sounds (in the order of seconds),
    this function will actually be *slower* than complexTone.

    Parameters
    ----------
    F0 : float
        Tone fundamental frequency in hertz.
    harmPhase : one of 'Sine', 'Cosine', 'Alternating', 'Random', 'Schroeder-', 'Schroeder+'
        Phase relationship between the partials of the complex tone.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    stretch : float
        Harmonic stretch in %F0. Increase each harmonic frequency by a fixed value
        that is equal to (F0*stretch)/100. If 'stretch' is different than
        zero, an inhanmonic complex tone will be generated.
    level : float
        The level of each partial in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left', 'Both', 'Odd Right' or 'Odd Left'
        Channel in which the tone will be generated. If 'channel'
        if 'Odd Right', odd numbered harmonics will be presented
        to the right channel and even number harmonics to the left
        channel. The opposite is true if 'channel' is 'Odd Left'.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
    >>> ct = complexToneParallel(F0=440, harmPhase='Sine', lowHarm=3, highHarm=10,
    ...     stretch=0, level=55, duration=180, ramp=10, channel='Both',
    ...     fs=48000, maxLevel=100)
    
    """
    amp = 10**((level - maxLevel) / 20)
    durationSec = duration / 1000 #convert from ms to sec
    rampSec = ramp / 1000
    stretchHz = (F0*stretch)/100
    
    nSamples = int(round(durationSec * fs))
    nRamp = int(round(rampSec * fs))
    nTot = nSamples + (nRamp * 2)
    snd = zeros((nTot, 2))
    tn = []
    pool = multiprocessing.Pool()
    
    for i in range(lowHarm, highHarm+1):
        #Select channel
        if channel == "Right" or channel == "Left" or channel == "Both":
            thisChan = channel
        elif channel == "Odd Left" or channel == "Odd Right":
            if i%2 > 0: #odd harmonic
                if channel == "Odd Left":
                    thisChan = "Left"
                elif channel == "Odd Right":
                    thisChan = "Right"
            else: #even harmonic
                if channel == "Odd Left":
                    thisChan = "Right"
                elif channel == "Odd Right":
                    thisChan = "Left"
        else:
            raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', 'Both', 'Odd Right', or 'Odd Left'")
        #Select phase
        if harmPhase == "Sine":
            thisPhase = 0
        elif harmPhase == "Cosine":
            thisPhase = pi/2
        elif harmPhase == "Alternating":
            if i%2 > 0: #odd harmonic
                thisPhase = 0
            else:
                thisPhase = pi/2
        elif harmPhase == "Schroeder-":
            thisPhase = -pi * i * (i - 1) / (highHarm-lowHarm+1)
        elif harmPhase == "Schroeder+":
            thisPhase = pi * i * (i - 1) / (highHarm-lowHarm+1)
        elif harmPhase == "Random":
            thisPhase =  numpy.random.random() * 2 * pi
        else:
            raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one 'Sine', 'Cosine', 'Alternating', 'Schroeder-', 'Schroeder+', or 'Random'")
                
        pool.apply_async(pureTone, (F0*i+stretchHz, thisPhase, level, duration, ramp, thisChan, fs, maxLevel), callback=tn.append)

    pool.close()
    pool.join()
    
    for i in range(len(tn)):
        snd = snd + tn[i]
        
    return snd

def complexToneIPD(F0=220, harmPhase="Sine", lowHarm=1, highHarm=10, stretch=0, level=60, duration=980, ramp=10, IPD=3.14, targetEar="Right", fs=48000, maxLevel=101):
    """
    Synthetise a complex tone with an interaural phase difference (IPD).

    Parameters
    ----------
    F0 : float
        Tone fundamental frequency in hertz.
    harmPhase : one of 'Sine', 'Cosine', 'Alternating', 'Random', 'Schroeder-', 'Schroeder+'
        Phase relationship between the partials of the complex tone.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    stretch : float
        Harmonic stretch in %F0. Increase each harmonic frequency by a fixed value
        that is equal to (F0*stretch)/100. If 'stretch' is different than
        zero, an inhanmonic complex tone will be generated.
    level : float
        The level of each partial in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    IPD : float
        Interaural phase difference, in radians.
    targetEar : string
        The ear in which the phase will be shifted.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
    >>> ct = complexToneIPD(F0=440, harmPhase='Sine', lowHarm=3, highHarm=10,
    ...     stretch=0, level=55, duration=180, ramp=10, IPD=3.14, targetEar="Right",
    ...     fs=48000, maxLevel=100)
    
    """
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000. #convert from ms to sec
    ramp = ramp / 1000
    stretchHz = (F0*stretch)/100
    
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)
    
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    tone = zeros(nTot)
    toneShift = zeros(nTot)

    if harmPhase == "Sine":
        for i in range(lowHarm, highHarm+1):
            tone =  tone + sin(2 * pi * ((F0 * i) + stretchHz) * timeAll)
            toneShift =  toneShift + sin(2 * pi * ((F0 * i) + stretchHz) * timeAll + IPD)
    elif harmPhase == "Cosine":
        for i in range(lowHarm, highHarm+1):
            tone = tone + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
            toneShift = toneShift + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll + IPD)
    elif harmPhase == "Alternating":
        for i in range(lowHarm, highHarm+1):
            if i%2 > 0: #odd harmonic
                tone = tone + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                toneShift = toneShift + cos(2 * pi * ((F0 * i)+stretchHz) * timeAll + IPD)
            else: #even harmonic
                tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll)
                toneShift = toneShift + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + IPD)
    elif harmPhase == "Schroeder-":
        for i in range(lowHarm, highHarm+1):
            phase = -pi * i * (i - 1) / (highHarm-lowHarm+1)
            tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            toneShift = toneShift + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase + IPD)
    elif harmPhase == "Schroeder+":
        for i in range(lowHarm, highHarm+1):
            phase = pi * i * (i - 1) / (highHarm-lowHarm+1)
            tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            toneShift = toneShift + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase + IPD)      
    elif harmPhase == "Random":
        for i in range(lowHarm, highHarm+1):
            phase = numpy.random.random() * 2 * pi
            tone = tone + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase)
            toneShift = toneShift + sin(2 * pi * ((F0 * i)+stretchHz) * timeAll + phase + IPD)
    else:
        raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one 'Sine', 'Cosine', 'Alternating', 'Schroeder-', 'Schroeder+', or 'Random'")

    if targetEar == "Right":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:len(timeAll)]

        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneShift[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneShift[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneShift[nRamp+nSamples:len(timeAll)]
    elif targetEar == "Left":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:len(timeAll)]

        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneShift[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneShift[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneShift[nRamp+nSamples:len(timeAll)]

    return snd


def delayAdd(sig, delay, gain, iterations, configuration, fs):
    """
    Delay and add algorithm for the generation of iterated rippled noise.

    Parameters
    ----------
    sig : array of floats
        The signal to manipulate
    delay : float
        delay in seconds
    gain : float
        The gain to apply to the delayed signal
    iterations : int
        The number of iterations of the delay-add cycle
    configuration : string
        If 'Add Same', the output of iteration N-1 is added to delayed signal of the current iteration.
        If 'Add Original', the original signal is added to delayed signal of the current iteration.
    fs : int
        Sampling frequency in Hz.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    References
    ----------
    .. [YPS1996] Yost, W. A., Patterson, R., & Sheft, S. (1996). A time domain description for the pitch strength of iterated rippled noise. J. Acoust. Soc. Am., 99(2), 1066–78. 

    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> irn = delayAdd(sig=noise, delay=1/440, gain=1, iterations=6, configuration='Add Same', fs=48000)

    """
    #delay in seconds
    delayPnt = round(delay * fs)
    nSamples = len(sig[:,0])
    en_input_right = sqrt(sum(sig[:,1]**2))
    en_input_left = sqrt(sum(sig[:,0]**2))
    snd = zeros((nSamples, 2))
    delayed_sig = zeros((nSamples, 2))
    if configuration == "Add Same":
        for i in range(iterations):
            delayed_sig = concatenate((sig[delayPnt:nSamples], sig[0:delayPnt]), axis=0)
            delayed_sig = delayed_sig * gain
            sig = sig + delayed_sig
    elif configuration == "Add Original":
        original_sig = copy.copy(sig)
        for i in range(iterations):
            delayed_sig = concatenate((sig[delayPnt:nSamples], sig[0:delayPnt]), axis=0)
            delayed_sig = delayed_sig * gain
            sig = original_sig + delayed_sig
    snd = sig
    en_output_right = sqrt(sum(snd[:,1]**2))
    en_output_left = sqrt(sum(snd[:,0]**2))
    scale_right = en_input_right / en_output_right
    scale_left  = en_input_left / en_output_left

    snd[:,1] = snd[:,1] * scale_right
    snd[:,0] = snd[:,0] * scale_left

    return snd

def dichoticNoiseFromSin(F0=300, lowHarm=1, highHarm=3, compLevel=30, narrowBandCompLevel=30,
                         lowFreq=40, highFreq=2000, compSpacing=10, sigBandwidth=100, distanceUnit="Cent",
                         phaseRelationship="NoSpi", dichoticDifference="IPD Stepped",
                         dichoticDifferenceValue=pi, duration=380, ramp=10, fs=48000, maxLevel=101):
    """
    Generate Huggins pitch or narrow-band noise from random-phase sinusoids.

    This function generates first noise by adding closely spaced
    sinusoids in a wide frequency range. Then, it can apply an interaural
    time difference (ITD), an interaural phase difference (IPD) or a
    level increase to harmonically related narrow frequency bands
    within the noise. In the first two cases (ITD and IPD) the result
    is a dichotic pitch. In the last case the pitch can also be heard
    monaurally; adjusting the level increase, its salience can be closely
    matched to that of a dichotic pitch.
    
    Parameters
    ----------
    F0 : float
        Centre frequency of the fundamental in hertz.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    compLevel : float
        Level of each sinusoidal frequency component of the noise.
    lowFreq : float
        Lowest frequency in hertz of the noise.
    highFreq : float
        Highest frequency in hertz of the noise.
    compSpacing : float
        Spacing between the sinusoidal components used to generate the
        noise.
    sigBandwidth : float
        Width of each harmonically related frequency band.
    distanceUnit : string (one of 'Hz', 'Cent', 'ERB')
        The unit of measure used for 'compSpacing' and 'sigBandwidth'
    phaseRelationship : string ('NoSpi' or 'NpiSo')
        If NoSpi, the phase of the regions within each frequency band will
        be shifted. If NpiSo, the phase of the regions between each
        frequency band will be shifted.
    dichoticDifference : string ('IPD Stepped', 'IPD Random', 'ITD', 'ILD Right', 'ILD Left')
        Selects whether the decorrelation in the target regions will be achieved
        by applying a costant interaural phase shift (IPD), a random IPD shift,
        a costant interaural time difference (ITD), or a constant interaural level difference
        achieved by a level change in the right ('ILD Right') or the left ('ILD Left') ear.
    dichoticDifferenceValue : float
        For 'IPD Stepped', this is the phase offset, in radians, between the correlated
        and the uncorrelated regions.
        For 'ITD' this is the ITD in the transition region, in micro seconds.
        For 'Random Phase', the range of phase shift randomization in the uncorrelated regions.
        For 'ILD Left' or 'ILD Right' this is the level difference between the left and right
        ear in the uncorrelated regions.
    narrowBandCompLevel : float
        Level of the sinusoidal components in the frequency bands.
        If the 'narrowBandCompLevel' is greater than the level
        of the background noise ('compLevel'), a complex tone
        consisting of narrowband noises in noise will be generated.
    duration : float
        Sound duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       

    Examples
    --------
    >>> s1 = dichoticNoiseFromSin(F0=300, lowHarm=1, highHarm=3,
        compLevel=30, narrowBandCompLevel=30,
        lowFreq=40, highFreq=2000, compSpacing=10,
        sigBandwidth=100, distanceUnit='Cent',
        phaseRelationship='NoSpi', dichoticDifference='IPD Stepped',
        dichoticDifferenceValue=pi, duration=380, ramp=10,
        fs=48000, maxLevel=101)

    """
    
    sDuration = duration/1000 #convert from ms to sec
    sRamp = ramp/1000

    totDur = sDuration + (2 * sRamp)
    nSamples = int(round(sDuration * fs))
    nRamp = int(round(sRamp * fs))
    nTot = nSamples + (nRamp * 2)
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 
    snd = zeros((nTot, 2))

    if distanceUnit == 'Hz':
        noiseBandwidth = highFreq - lowFreq
    elif distanceUnit == 'Cent':
        noiseBandwidth = 1200*log2(highFreq/lowFreq) #in cents
    elif distanceUnit == 'ERB':
        noiseBandwidth = ERBDistance(lowFreq, highFreq)
    else:
        raise ValueError("Invalid 'distanceUnit' argument. 'distanceUnit' must be one 'Hz', 'Cent', or 'ERB'")
    
    nComponents = int(floor(noiseBandwidth/compSpacing))
    
    amp = 10**((compLevel - maxLevel) / 20)
    amp2 = 10**((narrowBandCompLevel - maxLevel) / 20) #change amp to the amp of narrow-bands
    freqs = zeros(nComponents)
    freqs[0] = lowFreq
    if distanceUnit == "Hz":
        for i in range(1, nComponents): #indexing starts from 1
            freqs[i] = freqs[i-1] + compSpacing
    elif distanceUnit == "Cent":
        for i in range(1, nComponents): #indexing starts from 1
            freqs[i] = freqs[i-1]*(2**(compSpacing/1200))
    elif distanceUnit == "ERB":
        for i in range(1, nComponents): #indexing starts from 1
            freqs[i] = freqFromERBInterval(freqs[i-1], compSpacing) 

    phasesR = numpy.random.uniform(0, 2*pi, nComponents)

    freqsToShift = array([], int64)
    for i in range(lowHarm, highHarm+1):
        thisFreq = F0*i;
        prevFreq = F0*(i-1)
        if distanceUnit == "Hz":
            lo = thisFreq - (sigBandwidth/2)
            hi = thisFreq + (sigBandwidth/2)
            hiPrev = prevFreq + (sigBandwidth/2)
        if distanceUnit == "Cent":
            lo = thisFreq*2**(-(sigBandwidth/2)/1200)
            hi = thisFreq*2**((sigBandwidth/2)/1200)
            hiPrev = prevFreq*2**((sigBandwidth/2)/1200)
        elif distanceUnit == "ERB":
            lo = freqFromERBInterval(thisFreq, -sigBandwidth/2) 
            hi = freqFromERBInterval(thisFreq, sigBandwidth/2)
            hiPrev = freqFromERBInterval(prevFreq, sigBandwidth/2)
        
        if phaseRelationship == "NoSpi":
            thisFreqsToShift = numpy.where((freqs>lo) & (freqs<hi))
            freqsToShift = numpy.append(freqsToShift, thisFreqsToShift)
        elif phaseRelationship == "NpiSo":
            if i == 0:
                thisFreqsToShift = where((freqs>lowFreq) & (freqs<lo))
            else:
                thisFreqsToShift = where((freqs>hiPrev) & (freqs<lo))
            if i == highHarm:
                foo = where(freqs>hi)
                thisFreqsToShift = numpy.append(thisFreqsToShift, foo)
            freqsToShift = numpy.append(freqsToShift, thisFreqsToShift)
        else:
            raise ValueError("Invalid 'phaseRelationship' argument. 'phaseRelationship must be either 'NoSpi', or 'NpiSo'")

    amps = numpy.repeat(amp, nComponents)
    amps[freqsToShift] = amp2
    sinArrayRight = zeros((nComponents, nTot))
    for i in range(0, nComponents):
        sinArrayRight[i,] = amps[i] * sin(2*pi*freqs[i] * timeAll + phasesR[i])          
    sinArrayLeft = copy.copy(sinArrayRight)
    
    if dichoticDifference == "IPD Stepped":
        for i in range(0,len(freqsToShift)):
            sinArrayLeft[freqsToShift[i],] =  amp2* sin(2*pi*freqs[freqsToShift[i]] * timeAll + (phasesR[freqsToShift[i]]+dichoticDifferenceValue))
    elif dichoticDifference == "IPD Random":
        phasesL = copy.copy(phasesR)
        phasesL[freqsToShift] = phasesL[freqsToShift] + numpy.random.uniform(0, dichoticDifferenceValue, len(phasesL[freqsToShift]))
        for i in range(0,len(freqsToShift)):
            sinArrayLeft[freqsToShift[i],] =  amp2* sin(2*pi*freqs[freqsToShift[i]] * timeAll + phasesL[i])
    elif dichoticDifference == "ITD":
        for i in range(0,len(freqsToShift)):
            thisIpd = itdtoipd(dichoticDifferenceValue/1000000, freqs[freqsToShift[i]])
            sinArrayLeft[freqsToShift[i],] =  amp2* sin(2*pi*freqs[freqsToShift[i]] * timeAll + (phasesR[freqsToShift[i]]+thisIpd))
    elif dichoticDifference == "ILD Right" or dichoticDifference == "ILD Left":
        amp3 = 10**((narrowBandCompLevel+dichoticDifferenceValue - maxLevel) / 20) #change amp to the amp of narrow-bands
        if dichoticDifference == "ILD Left":
            for i in range(0,len(freqsToShift)):
                sinArrayLeft[freqsToShift[i],]  = amp3* sin(2*pi*freqs[freqsToShift[i]] * timeAll + phasesR[freqsToShift[i]])
        elif dichoticDifference == "ILD Right":
            for i in range(0,len(freqsToShift)):
                sinArrayRight[freqsToShift[i],]  = amp3* sin(2*pi*freqs[freqsToShift[i]] * timeAll + phasesR[freqsToShift[i]])
    else:
        raise ValueError("Invalid 'dichoticDifference' argument. 'dichoticDifference' must be one of 'IPD Stepped', 'IPD Random', 'ITD', 'IDL Right', or 'IDL Left'")

    snd[:,0] = sum(sinArrayRight,0)
    snd[:,1] = sum(sinArrayLeft,0)
    snd = gate(ramp, snd, fs)

    return snd
    

def ERBDistance(f1, f2):
    """
    Compute the distance in equivalent rectangular bandwiths (ERBs) between f1 and f2.

    Parameters
    ----------
    f1 : float
        frequency 1 in Hz
    f2 : float
        frequency 2 in Hz

    Returns
    -------
    deltaERB : float
        distance between f1 and f2 in ERBs

    References
    ----------
    .. [GM] Glasberg, B. R., & Moore, B. C. J. (1990). Derivation of auditory filter shapes from notched-noise data. Hear. Res., 47(1-2), 103–38.
    
    Examples
    --------
    >>> ERBDistance(1000, 1200)
    
    """
    deltaERB = 21.4*log10(0.00437*f2+1) - 21.4*log10(0.00437*f1+1)

    return deltaERB


def expAMNoise(fc=150, fm=2.5, deltaCents=1200, fmPhase=pi, AMDepth=1,
               spectrumLevel=24, duration=480, ramp=10, channel="Both",
               fs=48000, maxLevel=101):
    """
    Generate a sinusoidally amplitude-modulated noise with an exponentially
    modulated AM frequency.

    Parameters
    ----------
    fc : float
        Carrier AM frequency in hertz. 
    fm : float
        Modulation of the AM frequency in Hz.
    deltaCents : float
        AM frequency excursion in cents. The instataneous AM frequency of the 
        noise will vary from fc**(-deltaCents/1200) to fc**(deltaCents/1200).
    fmPhase : float
        Starting phase of the AM modulation in radians.
    AMDepth : float
        Amplitude modulation depth.
    spectrumLevel : float
        Noise spectrum level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> snd = expAMNoise(fc=150, fm=2.5, deltaCents=1200, fmPhase=3.14, 
        AMDepth = 1, spectrumLevel=24, duration=480, ramp=10, channel='Both', 
        fs=48000, maxLevel=100)
    
    """
    
    amp = sqrt(fs/2)*(10**((spectrumLevel - maxLevel) / 20))
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    #random is a numpy module
    noise = (numpy.random.random(nTot) + numpy.random.random(nTot)) - (numpy.random.random(nTot) + numpy.random.random(nTot))
    RMS = sqrt(mean(noise*noise))
    #scale the noise so that the maxAmplitude goes from -1 to 1
    #since A = RMS*sqrt(2)
    scaled_noise = noise / (RMS * sqrt(2))

    #(1 + AMDepth*sin(2*pi*AMFreq*timeAll[0:nRamp]))

    fArr = 2*pi*fc*2**((deltaCents/1200)*cos(2*pi*fm*timeAll+fmPhase))
    ang = (cumsum(fArr)/fs) #+ startPhase
    #amp* sin(ang[nRamp:nRamp+nSamples])
    #* (1 + AMDepth*sin(ang[0:nRamp]))
    #* (1 + AMDepth*sin(ang[nRamp:nRamp+nSamples]))
    #* (1 + AMDepth*sin(ang[nRamp+nSamples:len(timeAll)]))
    if channel == "Right":
        snd[0:nRamp, 1] = amp * (1 + AMDepth*sin(ang[0:nRamp])) * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1] = amp * (1 + AMDepth*sin(ang[nRamp:nRamp+nSamples])) * scaled_noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * (1 + AMDepth*sin(ang[nRamp+nSamples:len(timeAll)])) * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise[nRamp+nSamples:len(timeAll)]
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * (1 + AMDepth*sin(ang[0:nRamp])) * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0] = amp * (1 + AMDepth*sin(ang[nRamp:nRamp+nSamples])) * scaled_noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * (1 + AMDepth*sin(ang[nRamp+nSamples:len(timeAll)])) * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise[nRamp+nSamples:len(timeAll)]
    elif channel == "Both":
        snd[0:nRamp, 1] = amp * (1 + AMDepth*sin(ang[0:nRamp])) * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1] = amp * (1 + AMDepth*sin(ang[nRamp:nRamp+nSamples])) * scaled_noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * (1 + AMDepth*sin(ang[nRamp+nSamples:len(timeAll)])) * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise[nRamp+nSamples:len(timeAll)]

        snd[0:nRamp, 0] = amp * (1 + AMDepth*sin(ang[0:nRamp])) * ((1-cos(pi * timeRamp/nRamp))/2) * scaled_noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0] = amp * (1 + AMDepth*sin(ang[nRamp:nRamp+nSamples])) * scaled_noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * (1 + AMDepth*sin(ang[nRamp+nSamples:len(timeAll)])) * ((1+cos(pi * timeRamp/nRamp))/2) * scaled_noise[nRamp+nSamples:len(timeAll)]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both'")

    return snd


def expSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=40, deltaCents=1200, fmPhase=0, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a frequency-modulated complex tone with an exponential sinusoid.

    Parameters
    ----------
    fc : float
        Carrier frequency in hertz. 
    fm : float
        Modulation frequency in Hz.
    deltaCents : float
        Frequency excursion in cents. The instataneous frequency of the tone
         will vary from fc**(-deltaCents/1200) to fc**(+deltaCents/1200).
    fmPhase : float
        Starting fmPhase in radians.
    level : float
        Tone level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> tone_peak = expSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=5, deltaCents=300, fmPhase=pi, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101)
    >>> tone_trough = expSinFMComplex(F0=150, lowHarm=1, highHarm=10, harmPhase="Sine", fm=5, deltaCents=300, fmPhase=0, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101)
    
    """

    for i in range(int(lowHarm), int(highHarm)+1):
        if harmPhase == "Sine":
            startPhase = 0
        elif harmPhase == "Cosine":
            startPhase = pi/2
        elif harmPhase == "Alternating":
            if i%2 > 0: #odd harmonic
                startPhase = 0
            else:
                startPhase = pi/2
        else:
            raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one of 'Sine', 'Cosine', or 'Alternating'")
        if i == lowHarm:
            snd = expSinFMTone(F0*i, fm, deltaCents, fmPhase, startPhase, level, duration, ramp, channel, fs, maxLevel)
        else:
            snd = snd + expSinFMTone(F0*i, fm, deltaCents, fmPhase, startPhase, level, duration, ramp, channel, fs, maxLevel)
        
    return snd


def expSinFMTone(fc=450, fm=5, deltaCents=300, fmPhase=pi, startPhase=0, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a frequency-modulated tone with an exponential sinusoid.

    Parameters
    ----------
    fc : float
        Carrier frequency in hertz. 
    fm : float
        Modulation frequency in Hz.
    deltaCents : float
        Frequency excursion in cents. The instataneous frequency of the tone
         will vary from fc**(-deltaCents/1200) to fc**(+deltaCents/1200).
    fmPhase : float
        Starting fmPhase in radians.
    level : float
        Tone level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> tone_peak = expSinFMTone(fc=450, fm=5, deltaCents=300, fmPhase=pi, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101)
    >>> tone_trough = expSinFMTone(fc=450, fm=5, deltaCents=300, fmPhase=0, level=60, 
    ...     duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101)
    
    """
  
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)
    fArr = 2*pi*fc*2**((deltaCents/1200)*cos(2*pi*fm*timeAll+fmPhase))
    ang = (cumsum(fArr)/fs) + startPhase

    snd = zeros((nTot, 2))

    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(ang[0:nRamp])
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(ang[nRamp:nRamp+nSamples])
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(ang[nRamp+nSamples:len(timeAll)])
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both'")
       

    return snd


def fm_complex1(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=1.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a complex tone with an embedded FM starting and stopping
    at a chosen time after the tone onset.

    Parameters
    ----------
    midF0 : float
        F0 at the FM zero crossing
    harmPhase : one of 'Sine', 'Cosine', 'Alternating', 'Random', 'Schroeder-', or 'Schroeder+'
        Phase relationship between the partials of the complex tone.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    level : float
        The level of each partial in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    fmFreq : float
        FM frequency in Hz.
    fmDepth : float
        FM depth in %
    fmStartPhase : float
        Starting phase of FM
    fmStartTime : float
        Start of FM in ms after start of tone
    fmDuration : float
        Duration of FM, in ms
    levelAdj : logical
        If `True`, scale the harmonic level so that for a complex
        tone within a bandpass filter the overall level does not
        change with F0 modulations.
    channel: 'Right', 'Left', 'Both', 'Odd Right' or 'Odd Left'
        Channel in which the tone will be generated. If 'channel'
        if 'Odd Right', odd numbered harmonics will be presented
        to the right channel and even number harmonics to the left
        channel. The opposite is true if 'channel' is 'Odd Left'.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Examples
    --------
    >>> tone_up = fm_complex1(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=1.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101)
    >>> tone_down = fm_complex1(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=0.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101)

    """
    
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    fmStartTime = fmStartTime / 1000  #convert from ms to sec
    fmDuration = fmDuration / 1000  #convert from ms to sec
    ramp = ramp / 1000
    fmStartPnt = int(round(fmStartTime*fs)) #sample where FM starts
    nFMSamples = int(round(fmDuration*fs)) #number of FM samples
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)
    
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)

    timeAllSamp = arange(0, nTot) #time array not scaled by fs
    time1 = timeAllSamp[0:fmStartPnt]
    time2 = timeAllSamp[fmStartPnt:fmStartPnt+nFMSamples]
    time3 = timeAllSamp[fmStartPnt+nFMSamples:nTot]
    fmTime = arange(0, nFMSamples)

    fmDepthHz = fmDepth*midF0/100 #convert from % to Hz
    B = fmDepthHz / fmFreq #Beta
    fmStartDepth = fmDepthHz*sin(fmStartPhase)

    fmRadFreq = 2*pi*fmFreq/fs

    midF0Rad = 2*pi*midF0/fs
    startF0Rad = 2*pi*(midF0 + fmDepthHz*sin(fmStartPhase))/fs
    endF0Rad = 2*pi*(midF0 + fmDepthHz*sin(fmStartPhase + nFMSamples*fmRadFreq)) / fs
    
    if channel == "Right" or channel == "Left" or channel == "Both":
        tone = zeros(nTot)
    elif channel == "Odd Left" or channel == "Odd Right":
        toneOdd = zeros(nTot)
        toneEven = zeros(nTot)
    snd = zeros((nTot, 2))

    #from Hartmann, WM (1997) Signals, sound, and sensation. New York: AIP Press
    #angular frequency is the time derivative of the instantaneous phase
    #if the angular frequency is given by a constant carrier `wc`, plus a
    #sinusoidal deviation `dw`:
    #eq.1: w(t) = wc + dw*cos(wm*t+phi)
    #where `wm` is the modulation frequency, then the instantaneous phase is
    #given by the integral of the above expression with respect to time
    #eq.2: PHI(t) = wc*t + (dw/wm)*sin(wm*t+phi)
    #that's the canonical form of the FM equation
    #if instead of modulating the angular freq. in eq. 1 by `cos` we modulate it by `sin`:
    #eq. 3: w(t) = wc + dw*(cos(wm*tphi)
    #and the resulting integral is:
    #eq.4: PHI(t) = wc*t - (dw/wm)*cos(wm*t+phi)
    #this is what we're actually using below
    
    if harmPhase == "Sine":
        for i in range(lowHarm, highHarm+1):
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone[0:fmStartPnt] =  tone[0:fmStartPnt] + sin(startF0Rad*i*time1)
                phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd[0:fmStartPnt] = toneOdd[0:fmStartPnt] + sin(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneOdd[fmStartPnt+nFMSamples:nTot] =  toneOdd[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2)
                else:
                    toneEven[0:fmStartPnt] = toneEven[0:fmStartPnt] + sin(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneEven[fmStartPnt+nFMSamples:nTot] =  toneEven[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2)
    elif harmPhase == "Cosine":
        for i in range(lowHarm, highHarm+1):
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone[0:fmStartPnt] =  tone[0:fmStartPnt] + cos(startF0Rad*i*time1)
                phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + cos(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + cos(i*endF0Rad*time3 + phaseCorrect2)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd[0:fmStartPnt] = toneOdd[0:fmStartPnt] + cos(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] + cos(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneOdd[fmStartPnt+nFMSamples:nTot] =  toneOdd[fmStartPnt+nFMSamples:nTot] + cos(i*endF0Rad*time3 + phaseCorrect2)
                else:
                    toneEven[0:fmStartPnt] = toneEven[0:fmStartPnt] + cos(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples] + cos(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneEven[fmStartPnt+nFMSamples:nTot] =  toneEven[fmStartPnt+nFMSamples:nTot] + cos(i*endF0Rad*time3 + phaseCorrect2)

    elif harmPhase == "Alternating":
        for i in range(lowHarm, highHarm+1):
            if i%2 > 0: #odd harmonic
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone[0:fmStartPnt] =  tone[0:fmStartPnt] + cos(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + cos(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + cos(i*endF0Rad*time3 + phaseCorrect2)
                elif channel == "Odd Left" or channel == "Odd Right":
                    toneOdd[0:fmStartPnt] = toneOdd[0:fmStartPnt] + cos(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] + cos(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneOdd[fmStartPnt+nFMSamples:nTot] =  toneOdd[fmStartPnt+nFMSamples:nTot] + cos(i*endF0Rad*time3 + phaseCorrect2)
            else: #even harmonic
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone[0:fmStartPnt] =  tone[0:fmStartPnt] + sin(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2)
                elif channel == "Odd Left" or channel == "Odd Right":
                    toneEven[0:fmStartPnt] = toneEven[0:fmStartPnt] + sin(startF0Rad*i*time1)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)))
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneEven[fmStartPnt+nFMSamples:nTot] =  toneEven[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2)
    elif harmPhase in ["Schroeder-", "Schroeder+"]:
        for i in range(lowHarm, highHarm+1):
            if harmPhase == "Schroeder-":
                phase = -pi * i * (i - 1) / (highHarm-lowHarm+1)
            elif harmPhase == "Schroeder+":
                phase = pi * i * (i - 1) / (highHarm-lowHarm+1)
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone[0:fmStartPnt] =  tone[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd[0:fmStartPnt] =  toneOdd[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneOdd[fmStartPnt+nFMSamples:nTot] =  toneOdd[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
                else:
                    toneEven[0:fmStartPnt] =  toneEven[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneEven[fmStartPnt+nFMSamples:nTot] =  toneEven[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
    elif harmPhase == "Random":
        for i in range(lowHarm, highHarm+1):
            phase = numpy.random.random() * 2 * pi
            if channel == "Right" or channel == "Left" or channel == "Both":
                tone[0:fmStartPnt] =  tone[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                tone[fmStartPnt+nFMSamples:nTot] =  tone[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
            elif channel == "Odd Left" or channel == "Odd Right":
                if i%2 > 0: #odd harmonic
                    toneOdd[0:fmStartPnt] =  toneOdd[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneOdd[fmStartPnt+nFMSamples:nTot] =  toneOdd[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
                else:
                    toneEven[0:fmStartPnt] =  toneEven[0:fmStartPnt] + sin(startF0Rad*i*time1 + phase)
                    phaseCorrect1 =  (i*startF0Rad*fmStartPnt) - (i*midF0Rad*fmStartPnt) + (i*B*cos(fmStartPhase)) 
                    toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples] + sin(midF0Rad*i*time2+phaseCorrect1-(i*B*cos(fmRadFreq*fmTime+fmStartPhase)) + phase)
                    phaseCorrect2 = (i*midF0Rad*(fmStartPnt+nFMSamples)) + (phaseCorrect1 - i*B*cos(fmRadFreq*nFMSamples + fmStartPhase)) - (i*endF0Rad*(fmStartPnt+nFMSamples))
                    toneEven[fmStartPnt+nFMSamples:nTot] =  toneEven[fmStartPnt+nFMSamples:nTot] + sin(i*endF0Rad*time3 + phaseCorrect2 + phase)
    else:
        raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one 'Sine', 'Cosine', 'Alternating', 'Schroeder-', 'Schroeder+', or 'Random'")
            

    #numpy.savetxt('ptone.txt', tone)
    #level correction --------------
    if levelAdj == True:
        if channel == "Right" or channel == "Left" or channel == "Both":
            tone[0:fmStartPnt] = tone[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            tone[fmStartPnt+nFMSamples:nTot] = tone[fmStartPnt+nFMSamples:nTot] * sqrt( ((endF0Rad / (2*pi)) * (fs))/ midF0)
        else:
            toneEven[0:fmStartPnt] = toneEven[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples]  * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            toneEven[fmStartPnt+nFMSamples:nTot] = toneEven[fmStartPnt+nFMSamples:nTot] * sqrt(((endF0Rad / (2*pi)) * (fs))/ midF0)

            toneOdd[0:fmStartPnt] = toneOdd[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            toneOdd[fmStartPnt+nFMSamples:nTot] = toneOdd[fmStartPnt+nFMSamples:nTot] * sqrt(((endF0Rad / (2*pi)) * (fs))/ midF0)

    #end of level correction -----------    
    
    if channel == "Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
    elif channel == "Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
    elif channel == "Both":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
        snd[:, 1] = snd[:, 0]
    elif channel == "Odd Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:nTot]
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:nTot]
    elif channel == "Odd Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:nTot]
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:nTot]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both', 'Odd Right', or Odd Left'")
        

    return snd

def fm_complex2(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=1.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101):

    """
    Synthetise a complex tone with an embedded FM starting and stopping
    at a chosen time after the tone onset.

    Parameters
    ----------
    midF0 : float
        F0 at the FM zero crossing
    harmPhase : one of 'Sine', 'Cosine', 'Alternating', 'Random', 'Schroeder-', 'Schroeder+'
        Phase relationship between the partials of the complex tone.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    level : float
        The level of each partial in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    fmFreq : float
        FM frequency in Hz.
    fmDepth : float
        FM depth in %
    fmStartPhase : float
        Starting phase of FM
    fmStartTime : float
        Start of FM in ms after start of tone
    fmDuration : float
        Duration of FM, in ms
    levelAdj : logical
        If `True`, scale the harmonic level so that for a complex
        tone within a bandpass filter the overall level does not
        change with F0 modulations.
    channel: 'Right', 'Left', 'Both', 'Odd Right' or 'Odd Left'
        Channel in which the tone will be generated. If 'channel'
        if 'Odd Right', odd numbered harmonics will be presented
        to the right channel and even number harmonics to the left
        channel. The opposite is true if 'channel' is 'Odd Left'.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Examples
    --------
    >>> tone_up = fm_complex2(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=1.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101)
    >>> tone_down = fm_complex2(midF0=140, harmPhase="Sine", lowHarm=1, highHarm=10, level=60, duration=430, ramp=10, fmFreq=1.25, fmDepth=40, fmStartPhase=0.5*pi, fmStartTime=25, fmDuration=400, levelAdj=True, channel="Both", fs=48000, maxLevel=101)
    
    """
    
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    fmStartTime = fmStartTime / 1000  #convert from ms to sec
    fmDuration = fmDuration / 1000  #convert from ms to sec
    ramp = ramp / 1000
    fmStartPnt = int(round(fmStartTime*fs)) #sample where FM starts
    nFMSamples = int(round(fmDuration*fs)) #number of FM samples
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)
    
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)

    timeAllSamp = arange(0, nTot) #time array not scaled by fs
    time1 = timeAllSamp[0:fmStartPnt]
    time2 = timeAllSamp[fmStartPnt:fmStartPnt+nFMSamples]
    time3 = timeAllSamp[fmStartPnt+nFMSamples:nTot]
    fmTime = arange(0, nFMSamples)

    fmDepthHz = fmDepth*midF0/100 #convert from % to Hz
    B = fmDepthHz / fmFreq #Beta
    fmStartDepth = fmDepthHz*sin(fmStartPhase)

    fmRadFreq = 2*pi*fmFreq/fs

    midF0Rad = 2*pi*midF0/fs
    startF0Rad = 2*pi*(midF0 + fmDepthHz*sin(fmStartPhase))/fs
    endF0Rad = 2*pi*(midF0 + fmDepthHz*sin(fmStartPhase + nFMSamples*fmRadFreq)) / fs

    startF0 = midF0 + fmDepthHz*sin(fmStartPhase)
    endF0 = midF0 + fmDepthHz*sin(fmStartPhase + nFMSamples*fmRadFreq)
    
    if channel == "Right" or channel == "Left" or channel == "Both":
        tone = zeros(nTot)
    elif channel == "Odd Left" or channel == "Odd Right":
        toneOdd = zeros(nTot)
        toneEven = zeros(nTot)
    snd = zeros((nTot, 2))

    #from Hartmann, WM (1997) Signals, sound, and sensation. New York: AIP Press
    #angular frequency is the time derivative of the instantaneous phase
    #if the angular frequency is given by a constant carrier `wc`, plus a
    #sinusoidal deviation `dw`:
    #eq.1: w(t) = wc + dw*cos(wm*t+phi)
    #where `wm` is the modulation frequency, then the instantaneous phase is
    #given by the integral of the above expression with respect to time
    #eq.2: PHI(t) = wc*t + (dw/wm)*sin(wm*t+phi)
    #that's the canonical form of the FM equation
    #if instead of modulating the angular freq. in eq. 1 by `cos` we modulate it by `sin`:
    #eq. 3: w(t) = wc + dw*(cos(wm*tphi)
    #and the resulting integral is:
    #eq.4: PHI(t) = wc*t - (dw/wm)*cos(wm*t+phi)
    #this is what we're actually using below
    
    for i in range(lowHarm, highHarm+1):
            fArr = zeros(nTot)
            fArr[0:fmStartPnt] = startF0*i
            fArr[fmStartPnt:fmStartPnt+nFMSamples] = (midF0*i + fmDepthHz*i*sin(2*pi*fmFreq*fmTime/fs+fmStartPhase))
            fArr[fmStartPnt+nFMSamples:nTot] = endF0*i
            if harmPhase == "Sine":
                ang = cumsum(2*pi*fArr/fs)
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + sin(ang)
                elif channel == "Odd Left" or channel == "Odd Right":
                    if i%2 > 0: #odd harmonic
                        toneOdd = toneOdd + sin(ang)
                    else:
                        toneEven = toneEven + sin(ang)
            elif harmPhase == "Cosine":
                ang = cumsum(2*pi*fArr/fs)
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + cos(ang)
                elif channel == "Odd Left" or channel == "Odd Right":
                    if i%2 > 0: #odd harmonic
                        toneOdd = toneOdd + cos(ang)
                    else:
                        toneEven = toneEven + cos(ang)

            elif harmPhase == "Alternating":
                ang = cumsum(2*pi*fArr/fs)
                if i%2 > 0: #odd harmonic
                    if channel == "Right" or channel == "Left" or channel == "Both":
                        tone = tone + cos(ang)
                    elif channel == "Odd Left" or channel == "Odd Right":
                        toneOdd = toneOdd + cos(ang)
                else: #even harmonic
                    if channel == "Right" or channel == "Left" or channel == "Both":
                        tone = tone + sin(ang)
                    elif channel == "Odd Left" or channel == "Odd Right":
                        toneEven = toneEven + sin(ang)
            elif harmPhase == "Schroeder-":
                phase = -pi * i * (i - 1) / (highHarm-lowHarm+1)
                ang = cumsum(2*pi*fArr/fs + phase)
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + sin(ang)
                elif channel == "Odd Left" or channel == "Odd Right":
                    if i%2 > 0: #odd harmonic
                        toneOdd = toneOdd + sin(ang)
                    else:
                        toneEven = toneEven + sin(ang)
            elif harmPhase == "Schroeder+":
                phase = pi * i * (i - 1) / (highHarm-lowHarm+1)
                ang = cumsum(2*pi*fArr/fs + phase)
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + sin(ang)
                elif channel == "Odd Left" or channel == "Odd Right":
                    if i%2 > 0: #odd harmonic
                        toneOdd = toneOdd + sin(ang)
                    else:
                        toneEven = toneEven + sin(ang)
            elif harmPhase == "Random":
                phase = numpy.random.random() * 2 * pi
                ang = cumsum(2*pi*fArr/fs + phase)
                if channel == "Right" or channel == "Left" or channel == "Both":
                    tone = tone + sin(ang)
                elif channel == "Odd Left" or channel == "Odd Right":
                    if i%2 > 0: #odd harmonic
                        toneOdd = toneOdd + sin(ang)
                    else:
                        toneEven = toneEven + sin(ang)
            else:
                raise ValueError("Invalid 'harmPhase' argument. 'harmPhase' must be one 'Sine', 'Cosine', 'Alternating', 'Schroeder-', 'Schroeder+', or 'Random'")


    #level correction --------------
    if levelAdj == True:
        if channel == "Right" or channel == "Left" or channel == "Both":
            tone[0:fmStartPnt] = tone[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            tone[fmStartPnt:fmStartPnt+nFMSamples] = tone[fmStartPnt:fmStartPnt+nFMSamples] * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            tone[fmStartPnt+nFMSamples:nTot] = tone[fmStartPnt+nFMSamples:nTot] * sqrt( ((endF0Rad / (2*pi)) * (fs))/ midF0)
        else:
            toneEven[0:fmStartPnt] = toneEven[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            toneEven[fmStartPnt:fmStartPnt+nFMSamples] = toneEven[fmStartPnt:fmStartPnt+nFMSamples]  * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            toneEven[fmStartPnt+nFMSamples:nTot] = toneEven[fmStartPnt+nFMSamples:nTot] * sqrt(((endF0Rad / (2*pi)) * (fs))/ midF0)

            toneOdd[0:fmStartPnt] = toneOdd[0:fmStartPnt] * sqrt(((startF0Rad / (2*pi)) * (fs))/ midF0)
            toneOdd[fmStartPnt:fmStartPnt+nFMSamples] = toneOdd[fmStartPnt:fmStartPnt+nFMSamples] * sqrt((midF0 + (fmDepthHz * sin (fmStartPhase + (fmTime * fmRadFreq)))) / midF0)
            toneOdd[fmStartPnt+nFMSamples:nTot] = toneOdd[fmStartPnt+nFMSamples:nTot] * sqrt(((endF0Rad / (2*pi)) * (fs))/ midF0)

    #end of level correction -----------    
    
    if channel == "Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
    elif channel == "Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
    elif channel == "Both":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  tone[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * tone[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * tone[nRamp+nSamples:nTot]
        snd[:, 1] = snd[:, 0]
    elif channel == "Odd Left":
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:nTot]
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:nTot]
    elif channel == "Odd Right":
        snd[0:nRamp, 1]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) *  toneOdd[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1]        = amp * toneOdd[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneOdd[nRamp+nSamples:nTot]
        snd[0:nRamp, 0]                     = amp * ((1-cos(pi * timeRamp/nRamp))/2) * toneEven[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0]        = amp * toneEven[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:nTot, 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * toneEven[nRamp+nSamples:nTot]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', 'Both', 'Odd Right', or 'Odd Left'")
        

    return snd


def FMTone(fc=1000, fm=40, mi=1, phase=0, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a frequency modulated tone.

    Parameters
    ----------
    fc : float
        Carrier frequency in hertz. This is the frequency of the tone at fm zero crossing.
    fm : float
        Modulation frequency in Hz.
    mi : float
        Modulation index, also called beta and is equal to deltaF/fm, where
        deltaF is the maximum deviation of the instantaneous frequency from
        the carrier frequency.
    phase : float
        Starting phase in radians.
    level : float
        Tone level in dB SPL. 
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left' or 'Both'
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of
        amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> snd = FMTone(fc=1000, fm=40, mi=1, phase=0, level=55, duration=180,
    ...     ramp=10, channel='Both', fs=48000, maxLevel=100)
    
    """
  
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc*timeAll[0:nRamp] + mi*sin(2*pi*fm * timeAll[0:nRamp] + phase))
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(2*pi*fc * timeAll[nRamp:nRamp+nSamples] +mi*sin(2*pi*fm * timeAll[nRamp:nRamp+nSamples] + phase))
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc * timeAll[nRamp+nSamples:len(timeAll)]+mi*sin(2*pi*fm * timeAll[nRamp+nSamples:len(timeAll)] + phase))
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc*timeAll[0:nRamp] + mi*sin(2*pi*fm * timeAll[0:nRamp] + phase))
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*fc * timeAll[nRamp:nRamp+nSamples] +mi*sin(2*pi*fm * timeAll[nRamp:nRamp+nSamples] + phase))
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc * timeAll[nRamp+nSamples:len(timeAll)]+mi*sin(2*pi*fm * timeAll[nRamp+nSamples:len(timeAll)] + phase))
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc*timeAll[0:nRamp] + mi*sin(2*pi*fm * timeAll[0:nRamp] + phase))
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*fc * timeAll[nRamp:nRamp+nSamples] +mi*sin(2*pi*fm * timeAll[nRamp:nRamp+nSamples] + phase))
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*fc * timeAll[nRamp+nSamples:len(timeAll)]+mi*sin(2*pi*fm * timeAll[nRamp+nSamples:len(timeAll)] + phase))
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', or 'Both'")
       

    return snd


def fir2Filt(f1, f2, f3, f4, snd, fs):
    """
    Filter signal with a fir2 filter.

    This function designs and applies a fir2 filter to a sound.
    The frequency response of the ideal filter will transition
    from 0 to 1 between 'f1' and 'f2', and from 1 to zero
    between 'f3' and 'f4'. The frequencies must be given in
    increasing order.

    Parameters
    ----------
    f1 : float
        Frequency in hertz of the point at which the transition
        for the low-frequency cutoff ends. 
    f2 : float
        Frequency in hertz of the point at which the transition
        for the low-frequency cutoff starts.
    f3 : float
        Frequency in hertz of the point at which the transition
        for the high-frequency cutoff starts.
    f4 : float
        Frequency in hertz of the point at which the transition
        for the high-frequency cutoff ends. 
    snd : array of floats
        The sound to be filtered.
    fs : int
        Sampling frequency of 'snd'.

    Returns
    -------
    snd : 2-dimensional array of floats

    Notes
    -------
    If 'f1' and 'f2' are zero the filter will be lowpass.
    If 'f3' and 'f4' are equal to or greater than the nyquist
    frequency (fs/2) the filter will be highpass.
    In the other cases the filter will be bandpass.

    The order of the filter (number of taps) is fixed at 256.
    This function uses internally 'scipy.signal.firwin2'.
       
    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> lpNoise = fir2Filt(f1=0, f2=0, f3=1000, f4=1200, 
    ...     snd=noise, fs=48000) #lowpass filter
    >>> hpNoise = fir2Filt(f1=5000, f2=6000, f3=24000, f4=26000, 
    ...     snd=noise, fs=48000) #highpass filter
    >>> bpNoise = fir2Filt(f1=400, f2=600, f3=4000, f4=4400, 
    ...     snd=noise, fs=48000) #bandpass filter
    """

    f1 = (f1 * 2) / fs
    f2 = (f2 * 2) / fs
    f3 = (f3 * 2) / fs
    f4 = (f4 * 2) / fs

    n = 256

    if f2 == 0: #low pass
        f = [0, f3, f4, 1]
        m = [1, 1, 0.00003, 0]
        
    elif f3 < 1: #bandpass
        f = [0, f1, f2, ((f2+f3)/2), f3, f4, 1]
        m = [0, 0.00003, 1, 1, 1, 0.00003, 0]
        
    else:#high pass
        f = [0, f1, f2, 0.999999, 1] #scipy wants that gain at the Nyquist is 0
        m = [0, 0.00003, 1, 1, 0]
        
    #print(f)
    b = firwin2 (n,f,m);
    x = copy.copy(snd)
    x[:, 0] = convolve(snd[:,0], b, 1)
    x[:, 1] = convolve(snd[:,1], b, 1)
    
    return x


def freqFromERBInterval(f1, deltaERB):
    """
    Compute the frequency, in Hz, corresponding to a distance,
    in equivalent rectangular bandwidths (ERBs), of 'deltaERB' from f1.

    Parameters
    ----------
    f1 : float
        frequency at one end of the interval in Hz
    deltaERB : float
        distance in ERBs

    Returns
    -------
    f2 : float
        frequency at the other end of the interval in Hz

    References
    ----------
    .. [GM] Glasberg, B. R., & Moore, B. C. J. (1990). Derivation of auditory filter shapes from notched-noise data. Hear. Res., 47(1-2), 103–38.
    
    Examples
    --------
    >>> freqFromERBInterval(100, 1.5)
    >>> freqFromERBInterval(100, -1.5)
    >>> #for several frequencies
    >>> freqFromERBInterval([100, 200, 300], 1.5)
    >>> # for several distances
    >>> freqFromERBInterval(100, [1, 1.5, 2])
    
    """
    f1 = asarray(f1)
    deltaERB = asarray(deltaERB)
    f2 = (10**((deltaERB + 21.4*log10(0.00437*f1 +1))/21.4)-1) / 0.00437 

    return f2


def gate(ramps, sig, fs):
    """
    Impose onset and offset ramps to a sound.

    Parameters
    ----------
    ramps : float
        The duration of the ramps.
    sig : array of floats    
        The signal on which the ramps should be imposed.
    fs : int
        The sampling frequency os 'sig'

    Returns
    -------
    sig : array of floats
       The ramped signal.

    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=200, ramp=0,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> gate(ramps=10, sig=noise, fs=48000)

    """
    
    ramps = ramps / 1000.
    nRamp = int(round(ramps * fs))
    timeRamp = arange(0., nRamp)
    nTot = len(sig[:,1])
    nStartSecondRamp = nTot - nRamp
    
    sig[0:nRamp, 0] = sig[0:nRamp, 0] *  ((1-cos(pi * timeRamp/nRamp))/2)
    sig[0:nRamp, 1] = sig[0:nRamp, 1] *  ((1-cos(pi * timeRamp/nRamp))/2)
    sig[nStartSecondRamp:nTot, 0] = sig[nStartSecondRamp:nTot, 0] * ((1+cos(pi * timeRamp/nRamp))/2)
    sig[nStartSecondRamp:nTot, 1] = sig[nStartSecondRamp:nTot, 1] * ((1+cos(pi * timeRamp/nRamp))/2)

    return sig

def getRMS(sig, channel="each"):
    """
    Compute the root mean square (RMS) value of the signal.

    Parameters
    ----------
    sig : array of floats
        The signal for which the RMS needs to be computed.
    channel : string or int 
        Either an integer indicating the channel number,
        'each' for a list of the RMS values in each channel, or 'all'
        for the RMS across all channels.

    Returns
    -------
    rms : float
       The RMS of 'sig'.

    Examples
    --------
    >>> pt = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel="Right", fs=48000, maxLevel=100)
    >>> getRMS(pt, channel="each")

    """

    if type(channel) not in [str, int]:
        raise ValueError("Channel must be either a string or an integer")
    if sig.ndim == 2:
        if type(channel) == str:
            if channel == "each":
                nChans = sig.shape[1]
                rms = list()
                for i in range(nChans):
                    rms.append(sqrt(mean(sig[:,i]*sig[:,i])))
            elif channel == "all":
                rms = sqrt(mean(sig*sig))
            else:
                raise ValueError("If 'channel' is a string it must be either 'each' or 'all'")
        elif type(channel) == int:
            rms = sqrt(mean(sig[:,channel]*sig[:,channel]))
    elif sig.ndim == 1:
        if type(channel) == str:
            if channel == "each":
                rms = list()
                rms.append(sqrt(mean(sig*sig)))
            elif channel == "all":
                rms = sqrt(mean(sig*sig))
            else:
                raise ValueError("If 'channel' is a string it must be either 'each' or 'all'")
        elif type(channel) == int:
            if channel != 0:
                raise valueError("signal is 1 dimensional. Trying to access channel > 0")
            rms = sqrt(mean(sig*sig))
    else:
        raise ValueError("getRMS accepts only 1 or 2 dimensional signals")
    return rms


def glide(freqStart=440, ftype="exponential", excursion=500, level=60, duration=180, phase=0, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetize a rising or falling tone glide with frequency changing
    linearly or exponentially. 


    Parameters
    ----------
    freqStart : float
        Starting frequency in hertz.
    ftype : string
        If 'linear', the frequency will change linearly on a Hz scale.
        If 'exponential', the frequency will change exponentially on a cents scale.
    excursion : float
        If ftype is 'linear', excursion is the total frequency change in Hz.
        The final frequency will be freqStart + excursion.
        If ftype is 'exponential', excursion is the total frequency change in cents.
        The final frequency in Hz will be freqStart*2**(excursion/1200).
    level : float
        Level of the tone in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       
    Examples
    --------
    >>> gl = glide(freqStart=440, ftype='exponential', excursion=500,
            level=55, duration=180, phase=0, ramp=10, channel='Both',
            fs=48000, maxLevel=100)

    """

    totDur = duration/1000+ramp/1000*2
    rate = excursion / totDur
    snd = chirp(freqStart, ftype, rate, level, duration, phase, ramp, channel, fs, maxLevel)
    
    return snd


def harmComplFromNarrowbandNoise(F0=440, lowHarm=1, highHarm=8, level=40, bandwidth=80, bandwidthUnit="Hz", stretch=0, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate an harmonic complex tone from narrow noise bands.

    Parameters
    ----------
    F0 : float
        Fundamental frequency of the complex.
    lowHarm : int
        Lowest harmonic component number. The first component is #1.
    highHarm : int
        Highest harmonic component number.
    level : float
        The spectrum level of the noise bands in dB SPL.
    bandwidth : float
        The width of each noise band.
    bandwidthUnit : string ('Hz', 'Cent', 'ERB')
        Defines whether the bandwith of the noise bands is expressed
        in hertz (Hz), cents (Cent), or equivalent rectangular bandwidths (ERB).
    stretch : float
        Harmonic stretch in %F0. Increase each harmonic frequency by a fixed value
        that is equal to (F0*stretch)/100. If 'stretch' is different than
        zero, an inhanmonic complex tone will be generated.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : 'Right', 'Left', 'Both', 'Odd Right' or 'Odd Left'
        Channel in which the tone will be generated. If 'channel'
        if 'Odd Right', odd numbered harmonics will be presented
        to the right channel and even number harmonics to the left
        channel. The opposite is true if 'channel' is 'Odd Left'.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : array of floats

    Examples
    --------
    >>> c1 = harmComplFromNarrowbandNoise(F0=440, lowHarm=3, highHarm=8,
         level=40, bandwidth=80, bandwidthUnit="Hz", stretch=0, duration=180, ramp=10, channel='Both',
         fs=48000, maxLevel=100)
    
    """
    stretchHz = (F0*stretch)/100
    sDuration = duration / 1000 #convert from ms to sec
    sRamp = ramp / 1000
    totDur = sDuration + (2 * sRamp)
    nSamples = int(round(sDuration * fs))
    nRamp = int(round(sRamp * fs))
    nTot = nSamples + (nRamp * 2)
    snd = zeros((nTot, 2))
    
    if channel == "Right" or channel == "Left" or channel == "Both":
        tone = zeros((nTot, 2))
    elif channel == "Odd Left" or channel == "Odd Right":
        toneOdd = zeros((nTot, 2))
        toneEven = zeros((nTot, 2))
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left', 'Both', 'Odd Right', or 'Odd Left'")
    

    cfs = arange(lowHarm, highHarm+1)*F0 #center frequencies
    cfs = cfs + stretchHz
    if bandwidthUnit == "Hz":
        fLo = cfs - (bandwidth/2)
        fHi = cfs + (bandwidth/2)
    elif bandwidthUnit == "Cent":
        fLo = cfs*2**(-(bandwidth/2)/1200)
        fHi = cfs*2**((bandwidth/2)/1200)
    elif bandwidthUnit == "ERB":
        fLo = freqFromERBInterval(cfs, -bandwidth/2)
        fHi = freqFromERBInterval(cfs, bandwidth/2)
    else:
        raise ValueError("Invalid 'bandwidthUnit' argument. 'bandwidthUnit' must be one of 'Hz', 'Cent', or 'ERB'")

    for i in range(len(fLo)):
        if channel == "Right" or channel == "Left" or channel == "Both":
            tone =  tone + steepNoise(fLo[i], fHi[i], level, duration, ramp, channel, fs, maxLevel)
        elif channel == "Odd Left" or channel == "Odd Right":
            if i%2 > 0: #odd harmonic
                        #make the tone in the left channel, then move it where needed
                toneOdd = toneOdd + steepNoise(fLo[i], fHi[i], level, duration, ramp, "Left", fs, maxLevel)
            else:
                toneEven = toneEven + steepNoise(fLo[i], fHi[i], level, duration, ramp, "Left", fs, maxLevel)
  

    if channel == "Right" or channel == "Left" or channel == "Both":
        snd = tone
    elif channel == "Odd Left":
        snd[:,0] = toneOdd[:,0]
        snd[:,1] = toneEven[:,0]
    elif channel == "Odd Right":
     snd[:,1] = toneOdd[:,0]
     snd[:,0] = toneEven[:,0]
  
    return snd


def intNCyclesFreq(freq, duration):
    """
    Compute the frequency closest to 'freq' that has an integer number
    of cycles for the given sound duration.

    Parameters
    ----------
    frequency : float
        Frequency in hertz.
    duration : float
        Duration of the sound, in milliseconds.

    Returns
    -------
    adjFreq : float
       
    Examples
    --------
    >>> intNCyclesFreq(freq=2.1, duration=1000)
    2.0
    >>> intNCyclesFreq(freq=2, duration=1000)
    2.0

    """
    
    duration = duration / 1000 #convert from ms to sec
    adjFreq = round(freq*duration)/duration
    
    return adjFreq


def imposeLevelGlide(sig, deltaL, startTime, endTime, channel, fs):
    """
    Impose a glide in level to a sound.
    
    This function changes the level of a sound with a smooth transition (an amplitude
    ramp) between 'startTime' and 'endTime'. If the signal input to the function
    has a level L, the signal output by the function will have a level L
    between time 0 and 'startTime', and a level L+deltaL between endTime and
    the end of the sound.

    Parameters
    ----------
    sig : float
        Sound on which to impose the level change.
    deltaL : float
        Magnitude of the level change in dB SPL.
    startTime : float
        Start of the level transition in milliseconds.
    endTime : float
        End of the level transition in milliseconds.
    channel : string ('Right', 'Left' or 'Both')
        Channel to which apply the level transition.
    fs : int
        Samplig frequency of the sound in Hz.

    Returns
    -------
    snd : array of floats

    Examples
    --------
    >>> pt = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> pt2 = imposeLevelGlide(sig=pt, deltaL=10, startTime=100,
            endTime=120, channel='Both', fs=48000)
    
    """
    #here we impose an amplitude ramp rather than a linear intensity change
    #give startTime and endTime in ms as arguments, then convert to sec

    if deltaL != 0:

        startTime = startTime / 1000.
        endTime   = endTime   / 1000.

    
        startAmp = 1 #no change
        endAmp = 10**(deltaL/20)
        nSamples = len(sig[:,0])
        startPnt = round(startTime * fs)
        endPnt   = round(endTime   * fs)
        nRamp = endPnt - startPnt
        timeRamp = arange(0., nRamp) 

        x = (startAmp+endAmp)/(startAmp-endAmp)
        y = 2/(startAmp-endAmp)
    
        ramp = ((x+cos(pi * timeRamp/nRamp))/y)
        ampArray = ones(nSamples)
        ampArray[startPnt:endPnt] = ramp
        ampArray[endPnt:len(ampArray)] = repeat(endAmp, len(ampArray[endPnt:len(ampArray)]))

    
        snd = zeros((nSamples,2))
        if channel == "Right":
            snd[:,1] = sig[:,1] * ampArray
        elif channel == "Left":
            snd[:,0] = sig[:,0] * ampArray
        elif channel == "Both":
            snd[:,1] = sig[:,1] * ampArray
            snd[:,0] = sig[:,0] * ampArray

    else:
        snd = sig

    return snd


def ITDShift(sig, f1, f2, ITD, channel, fs):
    """
    Set the ITD of a sound within the frequency region bounded by 'f1' and 'f2'

    Parameters
    ----------
    sig : array of floats
        Input signal.
    f1 : float
        The start point of the frequency region to be
        phase-shifted in hertz.
    f2 : float
        The end point of the frequency region to be
        phase-shifted in hertz.
    ITD : float
        The amount of ITD shift in microseconds
    channel : string ('Right' or 'Left')
        The channel in which to apply the shift.
    fs : float
        The sampling frequency of the sound.
        
    Returns
    -------
    out : 2-dimensional array of floats

    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> hp = ITDShift(sig=noise, f1=500, f2=600, ITD=5,
            channel='Left', fs=48000) #this generates a Dichotic Pitch
    
    """
    
    nSamples = len(sig[:,0])
    fftPoints = 2**nextpow2(nSamples)
    snd = zeros((nSamples, 2))
    nUniquePnts = ceil((fftPoints+1)/2)
    #compute the frequencies of the first half of the FFT
    freqArray1 = arange(0, nUniquePnts, 1) * (fs / fftPoints)
    #remove DC offset and nyquist for the second half of the FFT
    freqArray2 = -arange(1, (nUniquePnts-1), 1)[::-1] * (fs / fftPoints) 
    #find the indexes of the frequencies for which to set the ITD for the first half of the FFT
    sh1 = where((freqArray1>f1) & (freqArray1<f2))
    #same as above for the second half of the FFT
    sh2 = where((freqArray2<-f1) & (freqArray2>-f2))
    #compute IPSs for the first half of the FFT
    phaseShiftArray1 = itdtoipd(ITD/1000000, freqArray1[sh1])
    #same as above for the second half of the FFT
    phaseShiftArray2 = itdtoipd(ITD/1000000, freqArray2[sh2])
    #get the indexes of the first half of the FFT
    p1Start = 0; p1End = len(freqArray1)
    #get the indexes of the second half of the FFT
    p2Start = len(freqArray1); p2End = fftPoints 
        
    if channel == "Left":
        x = fft(sig[:,0], fftPoints)
    elif channel == "Right":
        x = fft(sig[:,1], fftPoints)
    else:
        raise ValueError("Invalid channel argument. Channel must either 'Right', or 'Left'")
    
    x1 = x[p1Start:p1End] #first half of the FFT
    x2 = x[p2Start:p2End] #second half of the FFT
    x1mag = abs(x1); x2mag = abs(x2) 
    x1Phase =  angle(x1); x2Phase =  angle(x2);
    x1Phase[sh1] = x1Phase[sh1] + phaseShiftArray1 #change phases
    x2Phase[sh2] = x2Phase[sh2] + phaseShiftArray2
    x1 = x1mag * (cos(x1Phase) + (1j * sin(x1Phase))) #rebuild FFTs
    x2 = x2mag * (cos(x2Phase) + (1j * sin(x2Phase)))
    x = concatenate((x1, x2))
    x = real(ifft(x)) #inverse transform to get the sound back
    
    if channel == "Left":
        snd[:,0] = x[0:nSamples]
        snd[:,1] = sig[:,1]
    elif channel == "Right":
        snd[:,1] = x[0:nSamples]
        snd[:,0] = sig[:,0]

    return snd


def itdtoipd(itd, freq):
    """
    Convert an interaural time difference to an equivalent interaural
    phase difference for a given frequency.

    Parameters
    ----------
    itd : float
        Interaural time difference in seconds.
    freq : float
        Frequency in hertz.

    Returns
    -------
    ipd : float

    Examples
    --------
    >>> itd = 300 #microseconds
    >>> itd = 300/1000000 #convert to seconds
    >>> itdtoipd(itd=itd, freq=1000)
    
    """
    
    ipd = (itd / (1/asarray(freq))) * 2 * pi
    
    return ipd


def joinSndISI(sndList, ISIList, fs):

    """
    
    Join a list of sounds with given interstimulus intervals

    Parameters
    ----------
    sndList : list of arrays
        The sounds to be joined.
    ISIList : list of floats
        The interstimulus intervals between the sounds in milliseconds.
        This list should have one element less than the sndList.
    fs : int
        Sampling frequency of the sounds in Hz.

    Returns
    -------
    snd : array of floats

    Examples
    --------
    >>> pt1 = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...       ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> pt2 = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...       ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> tone_seq = joinSndISI([pt1, pt2], [500], 48000)
    
    """
    snd = sndList[0]
    for i in range(len(sndList)-1):
        if ISIList[i] >= 0:
            thisSilence = makeSilence(ISIList[i], fs)
            snd = concatenate((snd, thisSilence), axis=0)
            snd = concatenate((snd, sndList[i+1]), axis=0)
        else:
            delay = (snd.shape[0]/fs)*1000 + ISIList[i]
            snd = addSounds(snd, sndList[i+1], delay, fs)
            
    return snd


def makeAsynchChord(freqs, levels, phases, tonesDuration, tonesRamps, tonesChannel, SOA, fs, maxLevel):
    """
    Generate an asynchronous chord.

    This function will add a set of pure tones with a given
    stimulus onset asynchrony (SOA). The temporal order of the
    successive tones is random.

    Parameters
    ----------
    freqs : array or list of floats.
        Frequencies of the chord components in hertz.
    levels : array or list of floats.
        Level of each chord component in dB SPL.
    phases : array or list of floats.
        Starting phase of each chord component.
    tonesDuration : float
        Duration of the tones composing the chord in milliseconds.
        All tones have the same duration.
    tonesRamps : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the tones will be tonesDuration+ramp*2.
    tonesChannel : string ('Right', 'Left' or 'Both')
        Channel in which the tones will be generated.
    SOA : float
        Onset asynchrony between the chord components.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
       
    Examples
    --------
    >>> freqs = [250, 500, 1000]
    >>> levels = [50, 50, 50]
    >>> phases = [0, 0, 0]
    >>> c1 = makeAsynchChord(freqs=freqs, levels=levels, phases=phases,
            tonesDuration=180, tonesRamps=10, tonesChannel='Both',
            SOA=60, fs=48000, maxLevel=100)

    """
     
    seq = numpy.arange(len(freqs))
    numpy.random.shuffle(seq)

    for i in range(len(freqs)):
        thisFreq = freqs[seq[i]]; thisLev = levels[seq[i]]; thisPhase = phases[seq[i]]
        thisTone = pureTone(thisFreq, thisPhase, thisLev, tonesDuration, tonesRamps, tonesChannel, fs, maxLevel)
        if i == 0:
            snd = thisTone
        else:
            snd = addSounds(snd, thisTone, SOA*i, fs)
    return snd


def makeHugginsPitch(F0=300, lowHarm=1, highHarm=3, spectrumLevel=45, bandwidth=100,
                     bandwidthUnit="Hz", dichoticDifference="IPD Stepped",
                     dichoticDifferenceValue=pi, phaseRelationship="NoSpi", stretch=0,
                     noiseType="White", duration=480, ramp=10, fs=48000, maxLevel=101):
    """
    Synthetise a complex Huggings Pitch.

    Parameters
    ----------
    F0 : float
        The centre frequency of the F0 of the complex in hertz.
    lowHarm : int
        Lowest harmonic component number.
    highHarm : int
        Highest harmonic component number.
    spectrumLevel : float
        The spectrum level of the noise from which
        the Huggins pitch is derived in dB SPL.
        If 'noiseType' is 'Pink', the spectrum level
        will be equal to 'spectrumLevel' at 1 kHz.
    bandwidth : float
        Bandwidth of the frequency regions in which the
        phase transitions occurr.
    bandwidthUnit : string ('Hz', 'Cent', 'ERB')
        Defines whether the bandwith of the decorrelated bands is expressed
        in hertz (Hz), cents (Cent), or equivalent rectangular bandwidths (ERB).
    dichoticDifference : string ('IPD Linear', 'IPD Stepped', 'IPD Random', 'ITD')
        Selects whether the decorrelation in the target regions will be achieved
        by applying a costant interaural phase shift (IPD), an costant interaural
        time difference (ITD), or a random IPD shift.
    dichoticDifferenceValue : float
        For 'IPD Linear' this is the phase difference between the start and the end
        of each transition region, in radians.
        For 'IPD Stepped', this is the phase offset, in radians, between the correlated
        and the uncorrelated regions.
        For 'ITD' this is the ITD in the transition region, in micro seconds.
        For 'Random Phase', the range of phase shift randomization in the uncorrelated regions.
    phaseRelationship : string ('NoSpi' or 'NpiSo')
        If NoSpi, the phase of the regions within each frequency band will
        be shifted. If NpiSo, the phase of the regions between each
        frequency band will be shifted.
    stretch : float
        Harmonic stretch in %F0. Increase each harmonic frequency by a fixed value
        that is equal to (F0*stretch)/100. If 'stretch' is different than
        zero, an inhanmonic complex tone will be generated.
    noiseType : string ('White' or 'Pink')
        The type of noise used to derive the Huggins Pitch.
    duration : float
        Complex duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    References
    ----------
    .. [CH] Cramer, E. M., & Huggins, W. H. (1958). Creation of Pitch through Binaural Interaction. J. Acoust. Soc. Am., 30(5), 413. 
    .. [AS] Akeroyd, M. A., & Summerfield, a Q. (2000). The lateralization of simple dichotic pitches. J. Acoust. Soc. Am., 108(1), 316–334.
    .. [ZH] Zhang, P. X., & Hartmann, W. M. (2008). Lateralization of Huggins pitch. J. Acoust. Soc. Am., 124(6), 3873–87. 

    Examples
    --------
    >>> hp = makeHugginsPitch(F0=300, lowHarm=1, highHarm=3, spectrumLevel=45,
        bandwidth=100, bandwidthUnit='Hz', dichoticDifference='IPD Stepped',
        dichoticDifferenceValue=pi, phaseRelationship='NoSpi', stretch=0,
        noiseType='White', duration=380, ramp=10, fs=48000, maxLevel=101)
    
    """

    if bandwidthUnit not in ["Hz", "Cent", "ERB"]:
        raise ValueError("Invalid 'bandwidthUnit' argument. 'bandwidthUnit' must be one of 'Hz', 'Cent', 'ERB'")
    
    stretchHz = (F0*stretch)/100
    sDuration = duration / 1000 #convert from ms to sec
    sRamp = ramp / 1000
    totDur = sDuration + (2 * sRamp)
    nSamples = int(round(sDuration * fs))
    nRamp = int(round(sRamp * fs))
    nTot = nSamples + (nRamp * 2)
    snd = zeros((nTot, 2))

    tone = broadbandNoise(spectrumLevel, duration+(ramp*2), 0, "Both", fs, maxLevel)
    if noiseType == "Pink":
        makePink(tone, fs)

    cfs = arange(lowHarm, highHarm+1)*F0 #center frequencies
    cfs = cfs + stretchHz
    if phaseRelationship == "NoSpi":
        if bandwidthUnit == "Hz":
            shiftLo = cfs - (bandwidth/2)
            shiftHi = cfs + (bandwidth/2)
        elif bandwidthUnit == "Cent":
            shiftLo = cfs*2**(-(bandwidth/2)/1200)
            shiftHi = cfs*2**((bandwidth/2)/1200)
        elif bandwidthUnit == "ERB":
            shiftLo = freqFromERBInterval(cfs, -bandwidth/2)
            shiftHi = freqFromERBInterval(cfs, bandwidth/2)
    elif phaseRelationship == "NpiSo":
        nHarms = len(cfs)
        shiftLo = zeros(nHarms+1)
        shiftHi = zeros(nHarms+1)

        shiftLo[0] = 10
        shiftHi[len(shiftHi)-1] = fs/2
        if bandwidthUnit == "Hz":
            shiftLo[1:len(shiftLo)] = cfs + (bandwidth/2)
            shiftHi[0:len(shiftHi)-1] = cfs - (bandwidth/2)
        elif bandwidthUnit == "Cent":
            shiftLo[1:len(shiftLo)] = cfs*2**((bandwidth/2)/1200)
            shiftHi[0:len(shiftHi)-1] = cfs*2**((bandwidth/2)/1200)
        elif bandwidthUnit == "ERB":
            shiftLo[1:len(shiftLo)] = freqFromERBInterval(cfs, bandwidth/2)
            shiftHi[0:len(shiftHi)-1] = freqFromERBInterval(cfs, -bandwidth/2)
    else:
        raise ValueError("Invalid 'phaseRelationship' argument. 'phaseRelationship' must be either 'NoSpi', or 'NpiSo'")

    for i in range(len(shiftLo)):
        if dichoticDifference == "IPD Linear":
            tone = phaseShift(tone, shiftLo[i], shiftHi[i], dichoticDifferenceValue, 'Linear', "Left", fs)
        elif dichoticDifference == "IPD Stepped":
            tone = phaseShift(tone, shiftLo[i], shiftHi[i], dichoticDifferenceValue, 'Step', "Left", fs)
        elif dichoticDifference == "IPD Random":
            tone = phaseShift(tone, shiftLo[i], shiftHi[i], dichoticDifferenceValue, 'Random', "Left", fs)
        elif dichoticDifference == "ITD":
            tone = ITDShift(tone, shiftLo[i], shiftHi[i], dichoticDifferenceValue, "Left", fs)
        else:
            raise ValueError("Invalid 'dichoticDifference' argument. 'dichoticDifference' must be one of 'IPD Linear, 'IPD Stepped', 'IPD Random', or 'ITD'")
    
    tone = gate(ramp, tone, fs)    
    snd = tone

    return snd


def makeIRN(delay=1/440, gain=1, iterations=6, configuration="Add Same", spectrumLevel=25, duration=280, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a iterated rippled noise

    Parameters
    ----------
    delay : float
        delay in seconds
    gain : float
        The gain to apply to the delayed signal
    iterations : int
        The number of iterations of the delay-add cycle
    configuration : string
        If 'Add Same', the output of iteration N-1 is added to delayed signal of the current iteration.
        If 'Add Original', the original signal is added to delayed signal of the current iteration.
    spectrumLevel : float
        Intensity spectrum level of the noise in dB SPL.
    duration : float
        Noise duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left', 'Both', or 'Dichotic')
        Channel in which the noise will be generated.
    fs : int
        Sampling frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
    >>> irn = makeIRN(delay=1/440, gain=1, iterations=6, configuration='Add Same',
           spectrumLevel=25, duration=280, ramp=10, channel='Both', fs=48000,
           maxLevel=101)

    """
    
    snd = broadbandNoise(spectrumLevel, duration+(ramp*2), 0, channel, fs, maxLevel) 
    if configuration == "Add Same":
        snd = delayAdd(snd, delay, gain, iterations, configuration, fs)
    elif configuration == "Add Original":
        snd =  delayAdd(snd, delay, gain, iterations, configuration, fs)
    else:
        raise ValueError("Invalid 'configuration' argument. 'configuration' must be one of 'Add Same', or 'Add Original'")

    snd = gate(ramp, snd, fs)
        
    return snd


def makePink(sig, fs):
    """
    Convert a white noise into a pink noise.

    The spectrum level of the pink noise at 1000 Hz will be equal to
    the spectrum level of the white noise input to the function.

    Parameters
    ----------
    sig : array of floats
        The white noise to be turned into a pink noise.
    fs : int
        Sampling frequency of the sound.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
     >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
     ...     channel='Both', fs=48000, maxLevel=100)
     >>> noise = makePink(sig=noise, fs=48000)
    
    """
    nSamples = len(sig[:,0])
    if nSamples < 2:
        pass
    else:
        ref = 1 + (1000 * nSamples/fs)
        x = rfft(sig[:,0], nSamples)
        idx = arange(1, len(x))
        mag = zeros(len(x))
        mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/idx)
        mag[0] = abs(x[0])
        ph = angle(x)
        x = mag * (cos(ph) + 1j * sin(ph))
    
        sig0 = irfft(x, nSamples)


        x = rfft(sig[:,1], nSamples)
        idx = arange(1, len(x))
        mag = zeros(len(x))
        mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/idx)
        mag[0] = abs(x[0])
        ph = angle(x)
        x = mag * (cos(ph) + 1j * sin(ph))

        sig1 = irfft(x, nSamples)

        sig[:, 0] = sig0
        sig[:, 1] = sig1
    
    return sig

def makeBlueRef(sig, fs, refHz):
    """
    Convert a white noise into a blue noise.

    The spectrum level of the blue noise at the frequency 'refHz'
    will be equal to the spectrum level of the white noise input
    to the function.

    Parameters
    ----------
    sig : array of floats
        The white noise to be turned into a blue noise.
    fs : int
        Sampling frequency of the sound.
    refHz : int
        Reference frequency in Hz. The amplitude of the other
        frequencies will be scaled with respect to the amplitude
        of this frequency.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
     >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
     ...     channel='Both', fs=48000, maxLevel=100)
     >>> noise = makeBlueRef(sig=noise, fs=48000, refHz=1000)
    
    """
    
    nSamples = len(sig[:,0])
    ref = 1 + (refHz * nSamples/fs)

    x = rfft(sig[:,0], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref*idx)
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))
    
    sig0 = irfft(x, nSamples)


    x = rfft(sig[:,1], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref*idx)
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))

    sig1 = irfft(x, nSamples)

    sig[:, 0] = sig0
    sig[:, 1] = sig1
    
    return sig


def makePinkRef(sig, fs, refHz):
    """
    Convert a white noise into a pink noise.

    The spectrum level of the pink noise at the frequency 'refHz'
    will be equal to the spectrum level of the white noise input
    to the function.

    Parameters
    ----------
    sig : array of floats
        The white noise to be turned into a pink noise.
    fs : int
        Sampling frequency of the sound.
    refHz : int
        Reference frequency in Hz. The amplitude of the other
        frequencies will be scaled with respect to the amplitude
        of this frequency.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
     >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
     ...     channel='Both', fs=48000, maxLevel=100)
     >>> noise = makePinkRef(sig=noise, fs=48000, refHz=1000)
    
    """
    
    nSamples = len(sig[:,0])
    ref = 1 + (refHz * nSamples/fs)

    x = rfft(sig[:,0], nSamples, axis=0)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/idx)
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))
    
    sig0 = irfft(x, nSamples, axis=0)


    x = rfft(sig[:,1], nSamples, axis=0)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/idx)
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))

    sig1 = irfft(x, nSamples, axis=0)

    sig[:, 0] = sig0
    sig[:, 1] = sig1
    
    return sig

def makeRedRef(sig, fs, refHz):
    """
    Convert a white noise into a red noise.

    The spectrum level of the red noise at the frequency 'refHz'
    will be equal to the spectrum level of the white noise input
    to the function.

    Parameters
    ----------
    sig : array of floats
        The white noise to be turned into a red noise.
    fs : int
        Sampling frequency of the sound.
    refHz : int
        Reference frequency in Hz. The amplitude of the other
        frequencies will be scaled with respect to the amplitude
        of this frequency.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
     >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
     ...     channel='Both', fs=48000, maxLevel=100)
     >>> noise = makeRedRef(sig=noise, fs=48000, refHz=1000)
    
    """
    
    nSamples = len(sig[:,0])
    ref = 1 + (refHz * nSamples/fs)

    x = rfft(sig[:,0], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/(idx**2))
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))
    
    sig0 = irfft(x, nSamples)


    x = rfft(sig[:,1], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref/(idx**2))
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))

    sig1 = irfft(x, nSamples)

    sig[:, 0] = sig0
    sig[:, 1] = sig1
    
    return sig

def makeVioletRef(sig, fs, refHz):
    """
    Convert a white noise into a violet noise.

    The spectrum level of the violet noise at the frequency 'refHz'
    will be equal to the spectrum level of the white noise input
    to the function.

    Parameters
    ----------
    sig : array of floats
        The white noise to be turned into a violet noise.
    fs : int
        Sampling frequency of the sound.
    refHz : int
        Reference frequency in Hz. The amplitude of the other
        frequencies will be scaled with respect to the amplitude
        of this frequency.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).

    Examples
    --------
     >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
     ...     channel='Both', fs=48000, maxLevel=100)
     >>> noise = makeVioletRef(sig=noise, fs=48000, refHz=1000)
    
    """
    
    nSamples = len(sig[:,0])
    ref = 1 + (refHz * nSamples/fs)

    x = rfft(sig[:,0], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref*(idx**2))
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))
    
    sig0 = irfft(x, nSamples)


    x = rfft(sig[:,1], nSamples)
    idx = arange(1, len(x))
    mag = zeros(len(x))
    mag[1:len(x)] = abs(x[1:len(x)]) * sqrt(ref*(idx**2))
    mag[0] = abs(x[0])
    ph = angle(x)
    x = mag * (cos(ph) + 1j * sin(ph))

    sig1 = irfft(x, nSamples)

    sig[:, 0] = sig0
    sig[:, 1] = sig1
    
    return sig


def makeSilence(duration=1000, fs=48000):
    """
    Generate a silence.

    This function just fills an array with zeros for the
    desired duration.
    
    Parameters
    ----------
    duration : float
        Duration of the silence in milliseconds.
    fs : int
        Samplig frequency in Hz.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       

    Examples
    --------
    >>> sil = makeSilence(duration=200, fs=48000)

    """
    #duration in ms
    duration = duration / 1000 #convert from ms to sec
    nSamples = int(round(duration * fs))
    snd = zeros((nSamples, 2))
    
    return snd


def nextpow2(x):
    """
    Next power of two.

    Parameters
    ----------
    x : int
        Base number.

    Returns
    -------
    out : float
        The power to which 2 should be raised.

    Examples
    --------
    >>> nextpow2(511)
    9
    >>> 2**9
    512
    
    """
    out = int(ceil(log2(x)))
    return out
#def nextpow2(i):
#    n = 2
#    while n < i:
#        n = n * 2
#    return n


def phaseShift(sig, f1, f2, phaseShift, phaseShiftType, channel, fs):
    """
    Shift the interaural phases of a sound within a given frequency region.

    Parameters
    ----------
    sig : array of floats
        Input signal.
    f1 : float
        The start point of the frequency region to be
        phase-shifted in hertz.
    f2 : float
        The end point of the frequency region to be
        phase-shifted in hertz.
    phaseShift : float
        The amount of phase shift in radians. 
    phaseShiftType : string ('Linear', 'Step', 'Random')
        If 'Linear' the phase changes progressively
        on a linear Hz scale from X to X+'phaseShift' from f1 to f2.
        If 'Stepped' 'phaseShift' is added as a constant to the
        phases from f1 to f2.
        If 'Random' a random phase shift from 0 to 'phaseShift'
        is added to each frequency component from f1 to f2.
    channel : string (one of 'Right', 'Left' or 'Both')
        The channel in which to apply the phase shift.
    fs : float
        The sampling frequency of the sound.
        
    Returns
    -------
    out : 2-dimensional array of floats

    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> hp = phaseShift(sig=noise, f1=500, f2=600, phaseShift=3.14,
            phaseShiftType='Linear', channel='Left', fs=48000) #this generates a Dichotic Pitch
    
    """

    nSamples = len(sig[:,0])
    fftPoints = 2**nextpow2(nSamples)
    snd = zeros((nSamples, 2))
    nUniquePnts = ceil((fftPoints+1)/2)
    freqArray1 = arange(0, nUniquePnts, 1) * (fs / fftPoints)
    freqArray2 = -arange(1, (nUniquePnts-1), 1)[::-1] * (fs / fftPoints) #remove DC offset and nyquist
    sh1 = where((freqArray1>f1) & (freqArray1<f2))
    sh2 = where((freqArray2<-f1) & (freqArray2>-f2))
    p1Start = 0; p1End = len(freqArray1)
    p2Start = len(freqArray1); p2End = fftPoints

    if phaseShiftType == "Linear":
        phaseShiftArray1 = linspace(0, phaseShift, len(sh1))
        phaseShiftArray2 = - linspace(phaseShift, 0, len(sh2))
    elif phaseShiftType == "Step":
        phaseShiftArray1 = repeat(phaseShift, len(sh1))
        phaseShiftArray2 = - repeat(phaseShift, len(sh1))
    elif phaseShiftType == "Random":
        phaseShiftArray1 = numpy.random.uniform(0, phaseShift, len(sh1))
        phaseShiftArray2 = -phaseShiftArray1[::-1]
    else:
        raise ValueError("Invalid 'phaseShiftType' argument. 'phaseShiftType' must be one of 'Linear', 'Step', or 'Random'")

    if channel == "Left":
        x = fft(sig[:,0], fftPoints)
        x1 = x[p1Start:p1End]
        x2 = x[p2Start:p2End]
        x1mag = abs(x1); x2mag = abs(x2)
        x1Phase =  angle(x1); x2Phase =  angle(x2);
        x1Phase[sh1] = x1Phase[sh1] + phaseShiftArray1
        x2Phase[sh2] =  x2Phase[sh2] + phaseShiftArray2
        x1 = x1mag * (cos(x1Phase) + (1j * sin(x1Phase)))
        x2 = x2mag * (cos(x2Phase) + (1j * sin(x2Phase)))
        x = concatenate((x1, x2))
        x = real(ifft(x))
        snd[:,0] = x[0:nSamples]
        snd[:,1] = sig[:,1]
    elif channel == "Right":
        x = fft(sig[:,1], fftPoints)
        x1 = x[p1Start:p1End]
        x2 = x[p2Start:p2End]
        x1mag = abs(x1); x2mag = abs(x2)
        x1Phase =  angle(x1); x2Phase =  angle(x2);
        x1Phase[sh1] = x1Phase[sh1] + phaseShiftArray1
        x2Phase[sh2] = x2Phase[sh2] + phaseShiftArray2
        x1 = x1mag * (cos(x1Phase) + (1j * sin(x1Phase)))
        x2 = x2mag * (cos(x2Phase) + (1j * sin(x2Phase)))
        x = concatenate((x1, x2))
        x = real(ifft(x))
        snd[:,1] = x[0:nSamples]
        snd[:,0] = sig[:,0]
    elif channel == "Both":
        x = fft(sig[:,0], fftPoints)
        x1 = x[p1Start:p1End]
        x2 = x[p2Start:p2End]
        x1mag = abs(x1); x2mag = abs(x2)
        x1Phase =  angle(x1); x2Phase =  angle(x2);
        x1Phase[sh1] = x1Phase[sh1] + phaseShiftArray1
        x2Phase[sh2] = x2Phase[sh2] + phaseShiftArray2
        x1 = x1mag * (cos(x1Phase) + (1j * sin(x1Phase)))
        x2 = x2mag * (cos(x2Phase) + (1j * sin(x2Phase)))
        x = concatenate((x1, x2))
        x = real(ifft(x))
        snd[:,0] = x[0:nSamples]

        x = fft(sig[:,1], fftPoints)
        x1 = x[p1Start:p1End]
        x2 = x[p2Start:p2End]
        x1mag = abs(x1); x2mag = abs(x2)
        x1Phase =  angle(x1); x2Phase =  angle(x2);
        x1Phase[sh1] = x1Phase[sh1] + phaseShiftArray1
        x2Phase[sh2] = x2Phase[sh2] + phaseShiftArray2
        x1 = x1mag * (cos(x1Phase) + (1j * sin(x1Phase)))
        x2 = x2mag * (cos(x2Phase) + (1j * sin(x2Phase)))
        x = concatenate((x1, x2))
        x = real(ifft(x))
        snd[:,1] = x[0:nSamples]
    else:
        raise ValueError("Invalid channel argument. Channel must one of 'Right', 'Left', or 'Both'")

    return snd


def pinkNoiseFromSin(compLevel=23, lowCmp=100, highCmp=1000, spacing=20, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a pink noise by adding sinusoids spaced by a fixed
    interval in cents.

    Parameters
    ----------
    compLevel : float
        Level of each sinusoidal component in dB SPL.
    lowCmp : float
        Frequency of the lowest noise component in hertz.
    highCmp : float
        Frequency of the highest noise component in hertz.
    spacing : float
        Spacing between the frequencies of the sinusoidal components
        in hertz.
    duration : float
        Noise duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the noise will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
        
    Examples
    --------
    >>> noise = pinkNoiseFromSin(compLevel=23, lowCmp=100, highCmp=1000,
        spacing=20, duration=180, ramp=10, channel='Both',
        fs=48000, maxLevel=100)
    
    """
    sDuration = duration / 1000 #convert from ms to sec
    sRamp = ramp / 1000

    totDur = sDuration + (2 * sRamp)
    nSamples = int(round(sDuration * fs))
    nRamp = int(round(sRamp * fs))
    nTot = nSamples + (nRamp * 2)
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 
    snd = zeros((nTot, 2))
    noisBandwidth = 1200*log2(highCmp/lowCmp) #in cents
    nComponents = int(floor(noisBandwidth/spacing))
    amp = 10**((compLevel - maxLevel) / 20)
    freqs = zeros(nComponents)
    freqs[0] = lowCmp
    for i in range(1, nComponents): #indexing starts from 1
        freqs[i] = freqs[i-1]*(2**(spacing/1200.))

    phasesR = numpy.random.uniform(0, 2*pi, nComponents)
    sinArray = zeros((nComponents, nTot))

    for i in range(0, nComponents):
        sinArray[i,] = amp* sin(2*pi*freqs[i] * timeAll + phasesR[i])
    
    if channel == "Right":
        snd[:,1] = sum(sinArray,0)
    elif channel == "Left":
        snd[:,0] = sum(sinArray,0)
    elif channel == "Both":
        snd[:,1] = sum(sinArray,0)
        snd[:,0] = snd[:,1]
    else:
        raise ValueError("Invalid channel argument. Channel must one of 'Right', 'Left', or 'Both'")

    snd = gate(ramp, snd, fs)    
    return snd


def pinkNoiseFromSin2(compLevel=23, lowCmp=100, highCmp=1000, spacing=20, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Generate a pink noise by adding sinusoids spaced by a fixed
    interval in cents.

    This function should produce the same output of pinkNoiseFromSin,
    it simply uses a different algorithm that uses matrix operations
    instead of a for loop. It doesn't seem to be much faster though.

    Parameters
    ----------
    compLevel : float
        Level of each sinusoidal component in dB SPL.
    lowCmp : float
        Frequency of the lowest noise component in hertz.
    highCmp : float
        Frequency of the highest noise component in hertz.
    spacing : float
        Spacing between the frequencies of the sinusoidal components
        in hertz.
    duration : float
        Noise duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the noise will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
        
    Examples
    --------
    >>> noise = pinkNoiseFromSin2(compLevel=23, lowCmp=100, highCmp=1000,
        spacing=20, duration=180, ramp=10, channel='Both',
        fs=48000, maxLevel=100)
    
    """
    sDuration = duration / 1000 #convert from ms to sec
    sRamp = ramp / 1000

    totDur = sDuration + (2 * sRamp)
    nSamples = int(round(sDuration * fs))
    nRamp = int(round(sRamp * fs))
    nTot = nSamples + (nRamp * 2)
    timeAll = arange(0, nTot) / fs
    snd = zeros((nTot, 2))
    noisBandwidth = 1200*log2(highCmp/lowCmp) #in cents
    nComponents = int(floor(noisBandwidth/spacing))
    amp = 10**((compLevel - maxLevel) / 20)
    freqs = zeros((nComponents,1))
    freqs[0] = lowCmp
    for i in range(1, nComponents): #indexing starts from 1
        freqs[i] = freqs[i-1]*(2**(spacing/1200.))
    #freqs = freqs.reshape(nComponents,1)
    phasesR = numpy.random.uniform(0, 2*pi, (nComponents,1))
    #phasesR = phasesR.reshape(nComponents,1)
    sinMatrix = zeros((nComponents, nTot))
    timeMatrix = zeros((nComponents, nTot))
    timeMatrix[:] = timeAll

    #for i in range(0, nComponents):
    #    sinMatrix[i,] = amp* sin(2*pi*freqs[i] * timeAll + phasesR[i])

    sinMatrix = amp*sin(2*pi*freqs*timeMatrix+phasesR)
    
    if channel == "Right":
        snd[:,1] = sum(sinMatrix,0)
    elif channel == "Left":
        snd[:,0] = sum(sinMatrix,0)
    elif channel == "Both":
        snd[:,1] = sum(sinMatrix,0)
        snd[:,0] = snd[:,1]
    else:
        raise ValueError("Invalid channel argument. Channel must one of 'Right', 'Left', or 'Both'")

    snd = gate(ramp, snd, fs)    
    return snd


def pureTone(frequency=1000, phase=0, level=60, duration=980, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise a pure tone.

    Parameters
    ----------
    frequency : float
        Tone frequency in hertz.
    phase : float
        Starting phase in radians.
    level : float
        Tone level in dB SPL.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       

    Examples
    --------
    >>> pt = pureTone(frequency=440, phase=0, level=65, duration=180,
    ...     ramp=10, channel='Right', fs=48000, maxLevel=100)
    >>> pt.shape
    (9600, 2)
    
    """
    
    amp = 10**((level - maxLevel) / 20)
    duration = duration / 1000 #convert from ms to sec
    ramp = ramp / 1000

    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp) 

    snd = zeros((nTot, 2))
    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 1] = amp* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phase)
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phase)
    elif channel == "Both":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[0:nRamp] + phase)
        snd[nRamp:nRamp+nSamples, 0] = amp* sin(2*pi*frequency * timeAll[nRamp:nRamp+nSamples] + phase)
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * sin(2*pi*frequency * timeAll[nRamp+nSamples:len(timeAll)] + phase)
        snd[:, 1] = snd[:, 0]
    else:
        raise ValueError("Invalid channel argument. Channel must one of 'Right', 'Left', or 'Both'")

       

    return snd


def scale(level, sig):
    """
    Increase or decrease the amplitude of a sound signal.

    Parameters
    ----------
    level : float
        Desired increment or decrement in dB SPL.
    signal : array of floats
        Signal to scale.

    Returns
    -------
    sig : 2-dimensional array of floats
       
    Examples
    --------
    >>> noise = broadbandNoise(spectrumLevel=40, duration=180, ramp=10,
    ...     channel='Both', fs=48000, maxLevel=100)
    >>> noise = scale(level=-10, sig=noise) #reduce level by 10 dB

    """
    #10**(level/20) is the amplitude corresponding to level
    #by multiplying the amplitudes we're adding the decibels
    # 20*log10(a1*a2) = 20*log10(a1) + 20*log10(a2)
    sig = sig * 10**(level/20)
    return sig

def setLevel_(level, snd, maxLevel, channel="Both"):
    """
    Set the RMS level of a sound signal to a given value.

    Parameters
    ----------
    level : float
        The desired RMS level of the signal in dB SPL.
    snd : array of floats
        Signal whose level is to be set.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the level will be set.

    Returns
    -------
    sig : 2-dimensional array of floats
       
    Examples
    --------
    >>> import copy
    >>> pt = pureTone(frequency=1000, phase=0, level=60, duration=100,
    ...     ramp=0, channel="Both", fs=48000, maxLevel=100)
    >>> pt2 = copy.copy(pt) #this function modifies the argument so make a copy!
    >>> pt2 = setLevel_(level=40, snd=pt2, maxLevel=100, channel="Both") #set spectrum level to 20 dB SPL
    >>> levDiff = 20*log10(getRMS(pt)[1]/getRMS(pt2)[1])

    """
    if channel == "Both":
        chans = [0,1]
    if channel == "Right":
        chans = [1]
    elif channel == "Left":
        chans = [0]

    for ch in range(len(chans)):
        i = chans[ch]
        currAmplitude = sqrt(mean(snd[:,i]*snd[:,i]))*sqrt(2)
        currLevel = 20*log10(currAmplitude)+maxLevel
        snd[:,i] = snd[:,i] * 10**((level-currLevel)/20)

    return snd

def steepNoise(frequency1=440, frequency2=660, level=60, duration=180, ramp=10, channel="Both", fs=48000, maxLevel=101):
    """
    Synthetise band-limited noise from the addition of random-phase
    sinusoids.

    Parameters
    ----------
    frequency1 : float
        Start frequency of the noise.
    frequency2 : float
        End frequency of the noise.
    level : float
        Noise spectrum level.
    duration : float
        Tone duration (excluding ramps) in milliseconds.
    ramp : float
        Duration of the onset and offset ramps in milliseconds.
        The total duration of the sound will be duration+ramp*2.
    channel : string ('Right', 'Left' or 'Both')
        Channel in which the tone will be generated.
    fs : int
        Samplig frequency in Hz.
    maxLevel : float
        Level in dB SPL output by the soundcard for a sinusoid of amplitude 1.

    Returns
    -------
    snd : 2-dimensional array of floats
        The array has dimensions (nSamples, 2).
       
    Examples
    --------
    >>> nbNoise = steepNoise(frequency1=440, frequency2=660, level=65,
    ...     duration=180, ramp=10, channel='Right', fs=48000, maxLevel=100)
    
    """

    if channel not in ["Right", "Left", "Both"]:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left' or 'Both'")

    duration = duration/1000 #convert from ms to sec
    ramp = ramp/1000

    totDur = duration + (2 * ramp)
    nSamples = int(round(duration * fs))
    nRamp = int(round(ramp * fs))
    nTot = nSamples + (nRamp * 2)

    spacing = 1 / totDur
    components = 1 + floor((frequency2 - frequency1) / spacing) 
    amp =  10**((level - maxLevel) / 20) * sqrt((frequency2 - frequency1) / components)
    
    timeAll = arange(0, nTot) / fs
    timeRamp = arange(0, nRamp)
    snd = zeros((nTot, 2))

    noise= zeros(nTot)
    for f in arange(frequency1, frequency2+spacing, spacing):
        radFreq = 2 * pi * f 
        phase = numpy.random.random(1) * 2 * pi
        noise = noise + sin(phase + (radFreq * timeAll))

    if channel == "Right":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1] = amp * noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * noise[nRamp+nSamples:len(timeAll)]
    elif channel == "Left":
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0] = amp * noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * noise[nRamp+nSamples:len(timeAll)]
    elif channel == "Both":
        snd[0:nRamp, 1] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 1] = amp * noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 1] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * noise[nRamp+nSamples:len(timeAll)]
        snd[0:nRamp, 0] = amp * ((1-cos(pi * timeRamp/nRamp))/2) * noise[0:nRamp]
        snd[nRamp:nRamp+nSamples, 0] = amp * noise[nRamp:nRamp+nSamples]
        snd[nRamp+nSamples:len(timeAll), 0] = amp * ((1+cos(pi * timeRamp/nRamp))/2) * noise[nRamp+nSamples:len(timeAll)]
    else:
        raise ValueError("Invalid channel argument. Channel must be one of 'Right', 'Left' or 'Both'")

    return snd

 
   


