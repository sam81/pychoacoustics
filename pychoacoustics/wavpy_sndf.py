#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of wavpy_sndf

#    wavpy_sndf is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    wavpy_sndf is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with wavpy_sndf.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for reading and writing WAV files. It is a simple but convenient wrapper to the soundfile module.
"""

import numpy as np
import soundfile as sndf
from tempfile import mkstemp
import platform, os, subprocess

if platform.system() == "Windows":
    import winsound

def wavread(fName):
    sndObj = sndf.SoundFile(fName, mode='r')
    #nbits = int(sndObj.subtype.split("_")[1])
    subtype = sndObj.subtype
    if subtype == "PCM_S8":
        nbits = 8
    elif subtype == "PCM_U8":
        nbits = 8
    elif subtype == "PCM_16":
        nbits = 16
    elif subtype == "PCM_24":
        nbits = 24
    elif subtype == "PCM_32":
        nbits = 32
    elif subtype == "FLOAT":
        nbits = 32
    elif subtype == "DOUBLE":
        nbits = 64
    else:
        nbits = "NA"
        
    fs = sndObj.samplerate
    snd = sndObj.read()
    sndObj.close()

    return snd, fs, nbits

def wavwrite(data, fs, nbits, fName, wave_format="PCM"):
    if nbits == 16:
        subtype = "PCM_16"
    elif nbits == 24:
        subtype = "PCM_24"
    elif nbits == 32:
        if wave_format == "PCM":
            subtype = "PCM_32"
        elif wave_format == "IEEE_FLOAT":
            subtype = "FLOAT"
    elif nbits == 64:
        subtype = "DOUBLE"
        
    sndf.write(fName, data, fs, subtype=subtype)

    return

def sound(snd, fs=48000, nbits=32):
    """
    Play out a numpy array through the soundcard.
    
    Parameters
    ----------
    snd : array of floats
         The sound to be played.
    fs : int
         Sampling frequency of the sound.
    nbits : int
         Desired bit depth.

    Examples
    --------
    >>> sound(snd, fs=48000, nbits=32)
    """
    
    (hnl, fname) = mkstemp("tmp_snd.wav")
    wavwrite(snd, fs, nbits, fname)
    if platform.system() == 'Linux':
        playExec = "aplay"
    elif platform.system() == "Darwin":
        playExec = "afplay"
    elif platform.system() == "Windows":
        winsound.PlaySound(fname, winsound.SND_FILENAME)
    else:
        print("Sorry your operating system is not currently supported")
    subprocess.call(playExec + " " + fname, shell=True)
    return
