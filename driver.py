#from matplotlib import pyplot as plt
from audiolazy import *
import numpy as np
from scipy.signal import lfilter, hamming
import wave
import math
import sys

sample_freq = 0
samples = np.array([])
target_sample_len = 65536

def first_two(arr):
	vals = []
	i=0
	while i < len(arr):
		if len(vals) >= 2:
			return vals
		elif arr[i] != 0:
			vals.append(arr[i])
		i += 1



def process(sound):
	global samples
	if len(samples) < target_sample_len:
		samples = np.concatenate((samples,sound))
		return
	#sound = wave.open("eee.wav",'r')
	#sample_freq = sound.getframerate()
	#raw_data = sound.readframes(-1)
	#raw_data = np.fromstring(raw_data,'Int16')
	#print np.shape(raw_data)

	sample_len = len(samples)
	windowed = samples * np.hamming(sample_len)
	high_passed = lfilter([1], [1., -0.63], windowed)

	f = lpc(high_passed, order=2+sample_freq/1000)
	roots = np.array(f.zeros)
	real_roots = roots[np.where(np.imag(roots)>=0)]
	angles = np.arctan2(np.imag(real_roots),np.real(real_roots))
	freqs = sorted(angles * (sample_freq / (2 * math.pi)))

	samples = np.array([])

	return first_two(freqs)


from flask import Flask
from flask_uwsgi_websocket import GeventWebSocket

app = Flask(__name__)
ws = GeventWebSocket(app)

@ws.route('/audio')
def audio(ws):
   global sample_freq
   first_message = True
   total_msg = ""
   sample_rate = 0

   while True:
      msg = ws.receive()

      if first_message and msg is not None: # the first message should be the sample rate
         sample_freq = int(msg.split(':')[1])
         first_message = False
         continue
      elif msg is not None:
	 print 'msg'
	 audio_as_int_array = np.frombuffer(msg, 'i2')
         formants = process(audio_as_int_array)
	 if formants != None:
		 ws.send(str(formants))
      else:
         break

#process(None)
if __name__ == '__main__':
    app.run(gevent=100,host='0.0.0.0')
