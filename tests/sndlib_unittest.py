 
import os, sys, unittest
sys.path.insert(0, os.path.abspath('../'))
from pychoacoustics.sndlib import*
from numpy import int16, int32, pi, unwrap
from scipy.io import wavfile
from pylab import*
from numpy.testing import dec, assert_array_equal
import random

random.seed(914)
numpy.random.seed(914)

dataPath = "../../pychoacoustics_data/test_data/"

def scipy_wavwrite(fname, fs, nbits, data):
    if nbits == 16:
        data = data*(2.**15)
        data = data.astype(int16)
    elif nbits == 24:
        print("error, cannot save 24 bits at the moment")
    elif nbits == 32:
        data = data*(2.**31)
        data = data.astype(int32)
        if nbits != 24:
            wavfile.write(fname, fs, data)

def read_wav(fName):
    fs, snd = wavfile.read(fName)
    if snd.dtype == "int16":
        snd = snd / (2**15)
    elif snd.dtype == "int32":
        snd = snd / (2**31)
    return snd, fs

class TestPureTone(unittest.TestCase):
    def testPureTone(self):
        snd = pureTone(frequency=1000, phase=0, level=50,
                       duration=80, ramp=10, channel="Both",
                       fs=48000, maxLevel=100)
        scipy_wavwrite(dataPath + 'current_wavs/pure_tone.wav', 48000, 32, snd)
        snd_stored, fs = read_wav(dataPath + 'stored_wavs/pure_tone.wav')
        snd_current, fs = read_wav(dataPath + 'current_wavs/pure_tone.wav')
        
        assert_array_equal(snd_current, snd_stored)

class TestHuggins(unittest.TestCase):
    def setUp(self):
        self.F0 = 440 
        self.lowHarm = 1
        self.highHarm = 1
        self.spectrumLevel = 40
        self.bandwidth = 50
        self.bandwidthUnit = "Hz" 
        self.dichoticDifference = "IPD Stepped"
        self.dichoticDifferenceValue = pi
        self.phaseRelationship = "NoSpi"
        self.noiseType = "White"
        self.stretch = 0
        self.duration = 980
        self.ramp = 10
        self.fs = 48000
        self.maxLevel = 101
        self.lowStop = 0.8
        self.highStop = 1.2
        self.lowFreq = 80
        self.highFreq = 1200
        self.nBits = 32
        self.storedWavDir = dataPath + 'stored_wavs/'
        self.currWavDir = dataPath + 'current_wavs/'
    def tearDown(self):
        for fPath in self.currFPaths:
            os.remove(fPath)
    def testHuggins1(self):
        currFName = 'huggins.wav'
        self.currFPaths = [self.currWavDir+currFName]
        snd = makeHugginsPitch(self.F0, self.lowHarm, self.highHarm, self.spectrumLevel,
                               self.bandwidth, self.bandwidthUnit, self.dichoticDifference,
                               self.dichoticDifferenceValue, self.phaseRelationship,
                               self.stretch, self.noiseType, self.duration, self.ramp, self.fs,
                               self.maxLevel)
        scipy_wavwrite(self.currFPaths[0], self.fs, self.nBits, snd)
        snd_stored, fs = read_wav(self.storedWavDir+currFName)
        snd_current, fs = read_wav(self.currFPaths[0])
        assert_array_equal(snd_current, snd_stored)
    def testHugginsF0s(self):
        self.currFPaths = []
        F0s = [440, 550, 660, 770, 880, 990]
        for i in range(len(F0s)):
            snd = makeHugginsPitch(F0s[i], self.lowHarm, self.highHarm, self.spectrumLevel,
                                   self.bandwidth, self.bandwidthUnit, self.dichoticDifference,
                                   self.dichoticDifferenceValue, self.phaseRelationship,
                                   self.stretch, self.noiseType, self.duration, self.ramp, self.fs,
                                   self.maxLevel)
            currFName = 'Huggins'+str(F0s[i])+'.wav'
            self.currFPaths.append(self.currWavDir + currFName)
            scipy_wavwrite(self.currFPaths[i], self.fs, self.nBits, snd)
            snd_stored, fs = read_wav(self.storedWavDir+currFName)
            snd_current, fs = read_wav(self.currFPaths[i])
            assert_array_equal(snd_current, snd_stored)
            
if __name__ == '__main__':
    unittest.main()
    #unittest.TextTestRunner().run(testHuggins)
