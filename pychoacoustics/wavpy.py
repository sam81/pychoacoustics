#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2013-2015 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of wavpy

#    wavpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    wavpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with wavpy.  If not, see <http://www.gnu.org/licenses/>.

"""
Module for reading and writing WAV files. It is a simple but convenient wrapper to the scipy.io.wavfile module.
"""
from __future__ import division
from scipy.io import wavfile
from tempfile import mkstemp
import platform, os, subprocess
from numpy import int16, int32

def wavread(fname):
    fs, snd = wavfile.read(fname)
    if snd.dtype == "int16":
        snd = snd / (2.**15)
        nbits = 16
    elif snd.dtype == "int32":
        snd = snd / (2.**31)
        nbits = 32
    return snd, fs, nbits


def wavwrite(data, fs, nbits, fname):
    if nbits not in [16, 32]:
        print("Sorry can only write 16 or 32 bits at the moment! Exiting")
        return

    if nbits == 16:
        data = data*(2.**15)
        data = data.astype(int16)
    elif nbits == 32:
        data = data*(2.**31)
        data = data.astype(int32)

    wavfile.write(fname, fs, data)

    return

def aplay(snd, fs=48000, nbits=32):
     (hnl, fname) = mkstemp("tmp_snd.wav")
     wavwrite(snd, fs, nbits, fname)
     subprocess.call("aplay" + " " + fname, shell=True)
     return
