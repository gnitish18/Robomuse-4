#!/usr/bin/env python
from os import environ, path
import sys, os
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from subprocess import call

MODELDIR = "../pocketsphinx-python/pocketsphinx/model/"
DATADIR = "../pocketsphinx-python/pocketsphinx/test/data/"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', 'lang_models/assistant.lm')
config.set_string('-dict', 'lang_models/assistant.dic')	

# This supresses all the loggin that you don't need
#config.set_string('-logfn', '/dev/null')

# Open file to read the data
# stream = open(os.path.join(DATADIR, "goforward.raw"), "rb")

# Alternatively you can read from microphone
import pyaudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()
print("Listening..")

# Process audio chunk by chunk. On keyphrase detected perform action and restart search
decoder = Decoder(config)
decoder.start_utt()
#stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()

hypothesis = decoder.hyp()
logmath = decoder.get_logmath()
print('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))

# Access N best decodings.
print('\n>>Best 10 hypothesis: ')
for best, i in zip(decoder.nbest(), range(10)):
    print (best.hypstr, best.score)

stream = open(path.join(DATADIR, 'goforward.mfc'), 'rb')
stream.read(4)
buf = stream.read(13780)
decoder.start_utt()
decoder.process_cep(buf, False, True)
decoder.end_utt()
hypothesis = decoder.hyp()
#print('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)

