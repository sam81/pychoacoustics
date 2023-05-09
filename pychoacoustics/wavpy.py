#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2013-2023 Samuele Carcagno <sam.carcagno@gmail.com>
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
Module for reading and writing WAV files. It is a simple but convenient wrapper to the wave module and the scipy.io.wavfile module.
"""
import platform, os, subprocess, struct, wave
import numpy as np
from scipy.io import wavfile
from tempfile import mkstemp
from numpy import float32, int16, int32

__version__ = "0.3.1"

class wav_header():
    def __init__(self, chunkID, chunkSize, chunk_fmt, subchunk1ID, subchunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample, subchunk2ID, subchunk2Size):
        self.chunkID = chunkID
        self.chunkSize = chunkSize
        self.chunk_fmt = chunk_fmt
        self.subchunk1ID = subchunk1ID
        self.subchunk1Size = subchunk1Size
        self.audioFormat = audioFormat
        self.numChannels = numChannels
        self.sampleRate = sampleRate
        self.byteRate = byteRate
        self.blockAlign = blockAlign
        self.bitsPerSample = bitsPerSample
        self.subchunk2ID = subchunk2ID
        self.subchunk2Size = subchunk2Size

def read_wav_header(fName):
    try:
        f = open(fName, "rb")
    except IOError:
        print("Could not open file. Check that that the file name\
        is correct")

    chunkID = bytes.decode(f.read(4), "ascii") #RIFF for WAV files
    if chunkID == "RIFF":
        is_big_endian = False
    elif chunkID == "RIFX":
        is_big_endian = True
    else:
        raise ValueError("File format not understood, only RIFF and RIFX formats are supported")
    chunkSize = struct.unpack(">i", f.read(4))[0] #size of the rest of the file (all file minus the 8 bits used so far)
    chunk_fmt = bytes.decode(f.read(4), 'ascii') #contains the letters WAVE

    if is_big_endian:
        fmt = '>'
    else:
        fmt = '<'

    subchunk1ID =  bytes.decode(f.read(4), "ascii") #contains the letters "fmt "
    subchunk1Size = struct.unpack(">i", f.read(4))[0] #f.read(4)
    # audioFormat  PCM = 1 (i.e. Linear quantization). Values other than 1 indicate some form of compression.
    audioFormat, numChannels = struct.unpack(fmt+"HH", f.read(4))
    sampleRate = struct.unpack(fmt+"I", f.read(4))[0]
    byteRate = struct.unpack(fmt+"I", f.read(4))[0] # == SampleRate * NumChannels * BitsPerSample/8
    #blockAlign  == NumChannels * BitsPerSample/8
    #bitsPerSample == bit depth
    blockAlign, bitsPerSample = struct.unpack(fmt+"HH", f.read(4))
    subchunk2ID = bytes.decode(f.read(4), "ascii") #Contains the letters "data"
    subchunk2Size = struct.unpack(fmt+"I", f.read(4))[0]

    wavHd = wav_header(chunkID, chunkSize, chunk_fmt, subchunk1ID, subchunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample, subchunk2ID, subchunk2Size)

    f.close()

    return wavHd


def wavread(fName, scale=True):
    """
    Read a WAV file into a numpy array.
    
    Parameters
    ----------
    fName : string
            Name of the WAV file to read
    scale : boolean
            Option valid only for the PCM wave format. If `True` the
            data will be returned as floaring point values ranging
            between -1 and 1. If `False` the data will be returned
            as the closest numpy integer type to the WAV bit depth,
            with values randing within the bit depth range.

    Returns
    -------
    snd : numpy array with the sound.
    
    fs : sampling frequency.
    
    nbits : bit depth.
        
    Examples
    --------
    >>> snd, fs, nbits = wavread("file.wav")
    """

    hd = read_wav_header(fName)
    nbits = hd.bitsPerSample
    
    if hd.audioFormat not in [1, 3, 65534]: # 1=PCM, 3=IEEE_FLOAT, 65534=EXTENSIBLE (some FLOAT WAV types seem to be stored like this)
        raise Exception("Sorry can only read PCM or IEEE_FLOAT formats.")

    if hd.bitsPerSample not in [16, 24, 32, 64]:
        raise Exception("Sorry can only read 16, 24, 32, or 64 bit WAVs.")
    
    if hd.bitsPerSample == 24: #use wave so that if `scale` is set to False values range from -2**23 to 2**23-1
        wh = wave.open(fName)
        nSamp = wh.getnframes() #nSamp = int(hd.subchunk2Size / (hd.numChannels*hd.bitsPerSample/8))
        fs = hd.sampleRate
        sampwidth = 3
        nChan = hd.numChannels
        snd_raw = wh.readframes(nSamp)
        raw_bytes = np.frombuffer(snd_raw, dtype=np.uint8)
        d8 = raw_bytes.reshape(nSamp, nChan, sampwidth)
        d8i32 = d8.astype(np.int32) #shift the packets of 8 into place, use bitwise OR `|` to reconstitute the full binary sequence
        snd_arr = (d8i32[:,:,0] << 8 | d8i32[:,:,1] << 16 | d8i32[:,:,2] << 24) >> 8
        if snd_arr.shape[1] == 1:
            snd_arr = np.squeeze(snd_arr)
        if scale == True:
            snd = snd_arr / (2**23)
        else:
            snd = snd_arr
    else:
        fs, snd = wavfile.read(fName)
        if hd.audioFormat == 1 and scale== True: ##scale
            if nbits == 16:
                snd = snd / (2**15)
            # elif nbits == 24:
            #     #snd = snd / (2**23)
            #     snd = snd / (2**31) #scipy converts it to 32-bit int
            elif nbits == 32:
                snd = snd / (2**31)
        
    return snd, fs, nbits


def wavwrite(data, fs, nbits, fName, wave_format="PCM", scale=True):
    """
    Write a numpy array as a WAV file.
    
    Parameters
    ----------
    data : array of floats
           The data to be written to the WAV file.
    fs : int
         Sampling frequency of the sound.
    nbits : int
         Bit depth of the WAV file (currently only values of 16 and 32 are supported)
    fName : string
            Name of the WAV file.
    scale : boolean
         Option valid only for the PCM wave format. If the data are floating point
         values ranging from -1 to 1 and scale is set to `True` they will be converted
         to the range of the appropriate integer type (according to the chosen bit depth).
         If scale is set to `False` it is assumed that the values are already in the range
         of the appropriate integer type (e.g. between -2**15 and 2**15-1 for 16 bits).
         Note that if `wave_format` is set to `IEEE_FLOAT` the data are never scaled.

    Examples
    --------
    >>> wavwrite(data, 48000, 32, "file.wav")
    """
    if wave_format not in ["PCM", "IEEE_FLOAT"]:
        raise Exception("Sorry can only PCM or IEEE_FLOAT formats at the moment.")
    
    if wave_format == "PCM":
        if nbits not in [16, 24, 32]:
            raise Exception("Sorry can only write 16, 24 or 32 bits PCM at the moment.")

        if nbits == 24: #not supported by scipy, use the wave module
            if data.ndim == 1:
                nChan = 1
            else:
                nChan = data.shape[1]
            if scale == True:
                d24_32 = data*(2**23)
                d24_32[np.where(d24_32>=2**23)] = 2**23-1
            else:
                d24_32 = data
            d24_32 = d24_32.astype(int32)
            #Shift first 0 bits, then 8, then 16, to get 24 bit little-endian.
            #`& 255 is a bit mask, it keeps the lower 8 bits and sets the rest to 0; 255 = 2^8-1`
            #We have a sequence of 32 binary values, We're interested only in the 24 rightmost values.
            #The idea is to chop it off into 3 8-units packets (once converted to uint8 only 8 units
            #will be stored)
            #Shifting by 0 and chopping off the 24 leftmost units gives the first packet
            #Shifting by 8 and chopping off the 24 leftmost units gives the second packet
            #Shifting by 16 and chopping off the 24 leftmost units gives the third packet
            d8_triplets = (d24_32.reshape(d24_32.shape + (1,)) >> np.array([0, 8, 16])) & 255  #the & 255 is probably superfluous because casting later to uint8 already keeps only the lowest 8 bits
            data = d8_triplets.astype(np.uint8).tobytes()
            wav_file = wave.open(fName, 'wb')
            wav_file.setnchannels(nChan)
            wav_file.setsampwidth(3)
            wav_file.setframerate(fs)
            wav_file.writeframes(data)
            wav_file.close()
        if nbits == 16:
            if scale == True:
                data = data*(2**15)
                data[np.where(data>=2**15)] = 2**15-1
            data = data.astype(int16)
            wavfile.write(fName, fs, data)
        elif nbits == 32:
            if scale == True:
                data = data*(2**31)
                data[np.where(data>=2**31)] = 2**31-1
            data = data.astype(int32)
            wavfile.write(fName, fs, data)
    elif wave_format == "IEEE_FLOAT":
        if nbits not in [32, 64]:
            raise Exception("Sorry can only write 32 or 64 bits IEEE_FLOAT files.")
        if nbits == 32:
             data = data.astype(np.float32)
        elif nbits == 64:
            data = data.astype(np.float64)

        wavfile.write(fName, fs, data)
            
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
    
    (hnl, fName) = mkstemp("tmp_snd.wav")
    wavwrite(snd, fs, nbits, fName)
    if platform.system() == 'Linux':
        playExec = "aplay"
    elif platform.system() == "Darwin":
        playExec = "afplay"
    else:
        print("Sorry your operating system is not currently supported")
    subprocess.call(playExec + " " + fName, shell=True)
    return
