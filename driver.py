from matplotlib import pyplot as plt
from audiolazy import *
import numpy as np
from scipy.signal import lfilter, hamming
import wave
import math

sound = wave.open("eee.wav",'r')
sample_freq = sound.getframerate()
raw_data = sound.readframes(-1)
raw_data = np.fromstring(raw_data,'Int16')

sample_len = len(raw_data)
windowed = raw_data * np.hamming(sample_len)
high_passed = lfilter([1], [1., -0.63], windowed)

f = lpc(high_passed, order=2+sample_freq/1000)
roots = np.array(f.zeros)
real_roots = roots[np.where(np.imag(roots)>=0)]
angles = np.arctan2(np.imag(real_roots),np.real(real_roots))
freqs = sorted(angles * (sample_freq / (2 * math.pi)))
print freqs


plt.waitforbuttonpress()
