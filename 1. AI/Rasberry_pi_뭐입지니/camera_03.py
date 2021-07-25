from __future__ import print_function
from ctypes import *

import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import audioop
import os
import user_auth as UA
import time
import ex1_kwstest as kws
import ex2_getVoice2Text as gv2t
import ex4_getText2VoiceStream as tts
import MicrophoneStream as MS
import check

HOST = 'gate.gigagenie.ai'
PORT = 4080
RATE = 16000
CHUNK = 512

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def main():
	while(1):
		output_name = "camera_03.wav"
		MS.play_file(output_name)
		
		recog = gv2t.getVoice2Text() 
		\
		print('Recognized Text: '+ recog)
		
		if ("찍") in recog:
			print(recog)
			break
		else:
			unknown_file = "unknown.wav"
			MS.play_file(unknown_file)


if __name__ == '__main__':
    main()
