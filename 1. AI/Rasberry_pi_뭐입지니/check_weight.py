
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

def get_weight():
	output_name = "weight.wav"
	#tts.getText2VoiceStream("몸무게가 어떻게 되나요?", output_name)
	MS.play_file(output_name)
	while(1):
		
		weight = gv2t.getVoice2Text()
		print('Recognized Text: '+ weight)
		
		if compare_num(weight):
			return "weight/"+weight
			# weight 값을 서버에 전송.
		else:
			unknown_file = "unknown.wav"
			MS.play_file(unknown_file)
		
		# weight 값을 서버로 전송
		# check_height 페이지로 이동
		
def compare_num(value):
	try :
		int(value)
		return True
	except ValueError:
		return False
