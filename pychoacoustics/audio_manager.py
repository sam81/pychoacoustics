# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from tempfile import mkstemp
import platform, os, subprocess 
from numpy import ceil, concatenate, floor, float32, int16, int32, mean, sqrt, transpose, zeros
import numpy as np
#from .multirate import resample
from .nnresample.nnresample import resample
from .pyqtver import*

if pyqtversion == 5:
    from PyQt5.QtCore import QThread
elif pyqtversion == 6:
    from PyQt6.QtCore import QThread
import sys, time

if platform.system() == "Windows":
    import winsound

if platform.system() == "Linux":
    try:
        import alsaaudio
    except ImportError:
        pass
try:
    import pyaudio
except ImportError:
    pass

def decimalToBinary(x, n):
    """Convert an integer in decimal format to binary string representation
    x: decimal integer
    n: number of positions
    """
    res = bin(x)
    res = res[2:len(res)] #strip the 0b header
    padSize = n - len(res)
    res = '0'*padSize + res

    return res

class audioManager():
    def __init__(self, parent):
        self.parent = parent
        self.prm = parent.prm
        if self.prm["pref"]["sound"]["wavmanager"] == "scipy":
            from .wavpy import wavread, wavwrite
        elif self.prm["pref"]["sound"]["wavmanager"] == "soundfile":
            from .wavpy_sndf import wavread, wavwrite
        self.wavwrite = wavwrite
        self.wavread = wavread
        self.initializeAudio()
            
    def initializeAudio(self):
        print("Initializing audio")
        self.playCmd = self.prm['pref']['sound']['playCommand']
        
        try: #if alsaaudio device was open close it
            self.device.close()
        except:
            print(sys.exc_info())

        try: #if paManager was open close it
            self.paManager.terminate() #actually closing the stream introduces offset clicks!
        except:
            pass

        if self.playCmd == "alsaaudio":
            try:
                self.device = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, mode=alsaaudio.PCM_NORMAL, device=self.prm["pref"]["sound"]["alsaaudioDevice"])
                print("Opening preferred alsaaudio device")
            except:
                self.device = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, mode=alsaaudio.PCM_NORMAL, device=self.listAlsaaudioPlaybackCards()[0])
                print("Opening first alsaaudio device")
        elif self.playCmd == "pyaudio":
            self.paManager = pyaudio.PyAudio()

            
    def playSound(self, snd, fs, nbits, writewav, fname):
        #wavmanager = self.prm["pref"]["sound"]["wavmanager"]
        playCmd = str(self.playCmd)
        enc = "pcm"+ str(nbits)
        if writewav == True:
            fname = fname
        else:
            (hnl, fname) = mkstemp("tmp_snd.wav")

        if playCmd in ['alsaaudio', 'pyaudio']:#write wav before appending zeros in this case
            if writewav == True:
                self.wavwrite(snd, fs, nbits, fname)

        if self.prm["pref"]["sound"]["appendSilence"] > 0:
            duration = self.prm["pref"]["sound"]["appendSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * fs))
            silenceToAppend = zeros((nSamples, 2))
            snd = concatenate((snd, silenceToAppend), axis=0)
            
        #prep params for alsaaudio or pyaudio
        if playCmd in ['alsaaudio', 'pyaudio']:
            nSamples = snd.shape[0]
            nChannels = snd.shape[1]
            bufferSize = self.prm["pref"]["sound"]["bufferSize"]
            if bufferSize < 1:
                bufferSize = nSamples
                nSeg = 1
            else:
                nSeg = int(ceil(nSamples/bufferSize))
                padSize = (nSeg*bufferSize) - nSamples
                pad = zeros((padSize, nChannels))
                snd = concatenate((snd, pad), axis=0)
            if nbits == 16:
                data = snd*(2**15)
                data[np.where(data>=2**15)] = 2**15-1
                data = data.astype(int16)
            elif nbits == 24:
                d24_32 = snd*(2**23)
                d24_32[np.where(d24_32>=2**23)] = 2**23-1
                d24_32 = d24_32.astype(int32)
                #Shift first 0 bits, then 8, then 16, to get 24 bit little-endian.
                d8_triplets = (d24_32.reshape(d24_32.shape + (1,)) >> np.array([0, 8, 16])) & 255  
                data = d8_triplets.astype(np.uint8)
            elif nbits == 32:
                data = snd*(2**31)
                data[np.where(data>=2**31)] = 2**31-1
                data = data.astype(int32)
        
        if playCmd == "alsaaudio":
            device = self.device
            device.setchannels(nChannels)
            device.setrate(fs)
            device.setperiodsize(bufferSize)
            if nbits == 16:
                device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            elif nbits == 24:
                device.setformat(alsaaudio.PCM_FORMAT_S24_3LE)
            elif nbits == 32:
                device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
            for i in range(nSeg):
                thisData = data[i*bufferSize:((i*bufferSize)+bufferSize)][:]
                device.write(thisData)
        elif playCmd == "pyaudio":
            if nbits == 16:
                sampleFormat = pyaudio.paInt16
            elif nbits == 24:
                sampleFormat = pyaudio.paInt24
            elif nbits == 32:
                sampleFormat = pyaudio.paInt32
            try:
                self.paStream.start_stream()
            except:
                self.paStream = self.paManager.open(format=sampleFormat,
                                             channels = nChannels,
                                             rate = fs,
                                             output = True,
                                             input_device_index = None,
                                             output_device_index=self.prm["pref"]["sound"]["pyaudioDevice"],
                                             frames_per_buffer=bufferSize)
                self.paStream.start_stream()
            for i in range(nSeg):
                thisData = data[i*bufferSize:((i*bufferSize)+bufferSize)][:]
                self.paStream.write(thisData, num_frames=bufferSize)
            #self.paStream.stop_stream()
            #stream.close()
          
        else:
            self.wavwrite(snd, fs, nbits, fname)
         
            if platform.system() == "Windows":
                if playCmd == "winsound":
                    winsound.PlaySound(fname, winsound.SND_FILENAME)
                else:
                    subprocess.call(playCmd + " " + fname, shell=True)
                if writewav == False:
                    os.close(hnl)
                    os.remove(fname)
            else:
                subprocess.call(playCmd + " " + fname, shell=True)
                if writewav == False:
                    os.close(hnl)
                    os.remove(fname)
        return

    def playSoundWithTrigger(self, snd, fs, nbits, writewav, fname, triggerNumber):
        if writewav == True:
            fname = fname
        else:
            (hnl, fname) = mkstemp("tmp_snd.wav")

        (hnl1, snd_fname) = mkstemp("snd.wav")
        (hnl2, trigon_fname) = mkstemp("trig-on.wav")
        (hnl3, trigoff_fname) = mkstemp("trig-off.wav")
            
        self.wavwrite(snd, fs, nbits, snd_fname)
        playCmd = self.playCmd
        if playCmd == "winsound": #does not really play with trigger for the moment
            winsound.PlaySound(snd_fname, winsound.SND_FILENAME)
        else:
            nSamp = snd.shape[0]
            triggerDur = self.prm["pref"]["general"]["triggerDur"] 
            nSamplesTrigger = ceil(triggerDur * fs) 
            chOff = zeros((nSamp, 1))
            chOn  = zeros((nSamp, 1)) 
            chOn[0:nSamplesTrigger,:] = 0.5
            self.wavwrite(chOff, fs, nbits, trigoff_fname)
            self.wavwrite(chOn, fs, nbits, trigon_fname)
            # self.scipy_wavwrite(trigoff_fname, fs, nbits, chOff)
            # self.scipy_wavwrite(trigon_fname, fs, nbits, chOn)
            triggerCode = decimalToBinary(triggerNumber, 8)
            triggerCode = triggerCode[::-1] #reverse it
            soxCmd = "sox -M " + snd_fname
            for i in range(6):
                if triggerCode[i] == '1':
                    wavToCat = " " + trigoff_fname 
                else:
                    wavToCat = " " + trigon_fname 
                soxCmd = soxCmd + wavToCat
      
            
            soxCmd = soxCmd + " " + fname
            subprocess.call(soxCmd, shell=True)
            os.close(hnl1)
            os.close(hnl2)
            os.close(hnl3)
            os.remove(trigoff_fname)
            os.remove(trigon_fname)
            os.remove(snd_fname)
            subprocess.call(playCmd + " " + fname, stdout=self.prm['cmdOutFileHandle'], stderr=self.prm['cmdOutFileHandle'], shell=True)
            if writewav == False:
                os.close(hnl)
                os.remove(fname)


    def loadWavFile(self, fName, desiredLevel, maxLevel, channel, desiredSampleRate=None):

        snd, orig_fs, nbits = self.wavread(fName)

        if snd.ndim == 1:
            snd = snd.reshape(snd.shape[0], 1)
            snd = concatenate((snd,snd), axis=1)
        rms1 = sqrt(mean(snd[:,0]*snd[:,0]))
        rms2 = sqrt(mean(snd[:,1]*snd[:,1]))
        if rms1 > 0:
            normSnd1 = snd[:,0] / (rms1 * sqrt(2))
        else:
            normSnd1 = snd[:,0]
        if rms2 > 0:
            normSnd2 = snd[:,1] / (rms2 * sqrt(2))
        else:
            normSnd2 = snd[:,1]
        desiredAmp = 10**((desiredLevel - maxLevel)/20)

        snd[:,0] = desiredAmp * normSnd1
        snd[:,1] = desiredAmp * normSnd2

        if channel == "Right":
            snd[:, 0] = zeros(len(snd[:,0]))
        elif channel == "Left":
            snd[:, 1] = zeros(len(snd[:,1]))
        elif channel == "Original":
            pass

        if desiredSampleRate != None and desiredSampleRate != orig_fs:
            print("Resampling")
            ch0 = resample(snd[:,0], desiredSampleRate, orig_fs)
            ch1 = resample(snd[:,1], desiredSampleRate, orig_fs)
            snd = zeros((ch0.shape[0],2))
            snd[:,0] = ch0; snd[:,1] = ch1
            fs = desiredSampleRate
        else:
            fs = orig_fs

        return snd, fs, nbits


    def listAlsaaudioPlaybackCards(self):
   
        playbackCardList = alsaaudio.pcms(alsaaudio.PCM_PLAYBACK)
        return playbackCardList
        
    
class threadedAudioPlayer(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.prm = self.parent().prm
        self.audioManager = audioManager(self)
        self.exiting = False
        if self.prm["pref"]["sound"]["wavmanager"] == "scipy":
            from .wavpy import wavread, wavwrite
        elif self.prm["pref"]["sound"]["wavmanager"] == "soundfile":
            from .wavpy_sndf import wavread, wavwrite
        self.wavwrite = wavwrite
        self.wavread = wavread
    def playThreadedSound(self, snd, sampRate, nbits, playCmd, writewav, fName):
        self.snd = snd
        self.sampRate = sampRate
        self.nbits = nbits
        self.playCmd = playCmd

        if writewav == True: #write the sound before appending zeros
            self.wavwrite(snd, sampRate, nbits, fName)
        
        if self.prm["pref"]["sound"]["appendSilence"] > 0:
            duration = self.prm["pref"]["sound"]["appendSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * sampRate))
            silenceToAppend = zeros((nSamples, 2))
            self.snd = concatenate((self.snd, silenceToAppend), axis=0)

        if self.playCmd in ['alsaaudio', 'pyaudio']:
            nSamples = self.snd.shape[0]
            nChannels = self.snd.shape[1]
            self.bufferSize = self.prm["pref"]["sound"]["bufferSize"]
            if self.bufferSize < 1:
                self.bufferSize = nSamples
                self.nSeg = 1
            else:
                self.nSeg = int(ceil(nSamples/self.bufferSize))
                padSize = (self.nSeg*self.bufferSize) - nSamples
                pad = zeros((padSize, nChannels))
                self.snd = concatenate((self.snd, pad), axis=0)
            if self.nbits == 16:
                self.data = self.snd*(2**15)
                self.data[np.where(self.data>=2**15)] = 2**15-1
                self.data = self.data.astype(int16)
            elif nbits == 24:
                d24_32 = (self.snd*(2**23))
                d24_32[np.where(d24_32>=2**23)] = 2**23-1
                d24_32 = d24_32.astype(int32)
                #Shift first 0 bits, then 8, then 16, to get 24 bit little-endian.
                d8_triplets = (d24_32.reshape(d24_32.shape + (1,)) >> np.array([0, 8, 16])) & 255  
                self.data = d8_triplets.astype(np.uint8)
            elif self.nbits == 32:
                self.data = self.snd*(2**31)
                self.data[np.where(self.data>=2**31)] = 2**31-1
                self.data = self.data.astype(int32)

        if playCmd == "alsaaudio":
            self.device = alsaaudio.PCM(type=alsaaudio.PCM_PLAYBACK, mode=alsaaudio.PCM_NORMAL, device=self.prm["pref"]["sound"]["alsaaudioDevice"])
            self.device.setchannels(nChannels)
            self.device.setrate(sampRate)
            self.device.setperiodsize(self.bufferSize)
            if self.nbits == 16:
                self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            elif nbits == 24:
                self.device.setformat(alsaaudio.PCM_FORMAT_S24_3LE)
            elif self.nbits == 32:
                self.device.setformat(alsaaudio.PCM_FORMAT_S32_LE)

        elif playCmd == "pyaudio":
            paManager = pyaudio.PyAudio()
            if self.nbits == 16:
                sampleFormat = pyaudio.paInt16
            elif nbits == 24:
                sampleFormat = pyaudio.paInt24
            elif nbits == 32:
                sampleFormat = pyaudio.paInt32
            
            self.stream = paManager.open(format=sampleFormat,
                channels = nChannels,
                rate = sampRate,
                output = True,
                input_device_index=None,
                output_device_index=self.prm["pref"]["sound"]["pyaudioDevice"],
                frames_per_buffer=self.bufferSize)
                
        #QThread.start(self)
        self.start()
        
    def run(self):
        i = 0
        while self.exiting == False and self.nSeg > 0:
            if self.playCmd == "alsaaudio":
                thisData = self.data[i*self.bufferSize:((i*self.bufferSize)+self.bufferSize)][:]
                self.device.write(thisData)
            elif self.playCmd == "pyaudio":
                thisData = self.data[i*self.bufferSize:((i*self.bufferSize)+self.bufferSize)][:]
                self.stream.write(thisData, num_frames=self.bufferSize)
            i = i+1
            self.nSeg = self.nSeg -1

            #stream.close()
            #paManager.terminate() #actually closing the stream introduces offset clicks!

    def __del__(self):
        #the thread will finish before being terminated
        self.exiting = True
        self.wait()
        self.terminate()



class threadedExternalAudioPlayer(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.prm = self.parent().prm
        self.audioManager = audioManager(self)
        self.exiting = False
    def playThreadedSound(self, sound, sampRate, bits, cmd, writewav, fName):
        self.sound = sound
        self.sampRate = sampRate
        self.bits = bits
        self.cmd = cmd
        self.writewav = writewav
        self.fName = fName
        
        self.start()
    def run(self):
        self.audioManager.playSound(self.sound, self.sampRate, self.bits, self.writewav, self.fName)
     
    def __del__(self):
        #the thread will finish before being terminated
        self.wait()
        self.terminate()
