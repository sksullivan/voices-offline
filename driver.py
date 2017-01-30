from matplotlib import pyplot as plt
from audiolazy import *
import numpy as np
from scipy.signal import lfilter, hamming
import wave
import math
import sys

def process(sound):
# sound = wave.open(sys.argv[1],'r')
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


from flask import Flask
from flask_uwsgi_websocket import GeventWebSocket

app = Flask(__name__)
ws = GeventWebSocket(app)

@ws.route('/audio')
def audio(ws):
   first_message = True
   total_msg = ""
   sample_rate = 0

   while True:
      msg = ws.receive()

      if first_message and msg is not None: # the first message should be the sample rate
         sample_rate = getSampleRate(msg)
         first_message = False
         continue
      elif msg is not None:
         audio_as_int_array = numpy.frombuffer(msg, 'i2')
         doSomething(audio_as_int_array)
      else:
         break

if __name__ == '__main__':
    app.run(gevent=100)