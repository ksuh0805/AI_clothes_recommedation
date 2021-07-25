#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ctypes import *

import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import audioop
import os
import user_auth as UA
import ex1_kwstest as kws
import ex2_getVoice2Text as gv2t
import ex4_getText2VoiceStream as tts
import MicrophoneStream as MS


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

def gene_call():
	KWSID = ['기가지니', '지니야', '친구야', '자기야']
	recog=kws.test(KWSID[1])
	if recog == 200:
			print('KWS Dectected ...\n Start STT...')
			return "gene_call"
	else:
		print('KWS Not Dectected ...')
	
	
def get_name():
	#Example7 KWS+STT
	
	KWSID = ['기가지니', '지니야', '친구야', '자기야']

	# 기가지니 : "이름을 말해주세요"
	output_file = "start.wav"
	MS.play_file(output_file) 
	while 1:

		# 이름 말하기.
		name = gv2t.getVoice2Text()
		print('Recognized Text: '+ name)
			
		# 이름이 none값이 아닌경우
		if "아빠" in name :
			name = "name/father"
			return name # rander templete도 구현하기.
		elif "엄마" in name:
			name = "name/mother"
			return name
		elif "딸" in name:
			name = "name/daughter"
			return name
		elif "아들" in name or "adele" in name:
			name = "name/son"
			return name
		else :
			unknown_file = "unknown.wav"
			MS.play_file(unknown_file)
			
		

def user_mod():
		
		MS.play_file("modifyQuery.wav")
		while 1:
			isMod = gv2t.getVoice2Text()
			if isMod == "네" or isMod == "내" or isMod=="예" or isMod=="yeah" or isMod=="응":
				return "yes"
			elif "아니" in isMod or "no" in isMod:
				return "no"
			else:
				unknown_file = "unknown.wav"
				MS.play_file(unknown_file)	
		

def profile_end():
	# 프로필 등록이 완료되었습니다.
	output_file = "profile_end.wav"
	MS.play_file(output_file) 

def closet_open():
	# 기가지니 : "새로운 옷을 등록하시겠어요?"
	output_file = "closet.wav"
	MS.play_file(output_file) 
	while 1:

		# 등록 여부 말하기.
		closet = gv2t.getVoice2Text()
			
		# 이름이 none값이 아닌경우
		if closet == "네" or closet == "내" or closet=="예" or closet=="yeah" or closet=="응":
			return "rec/yes"# rander templete도 구현하기
		elif "아니" in closet or "no" in closet:
			return "rec/no"
		else :
			unknown_file = "unknown.wav"
			MS.play_file(unknown_file)
			
def cody_start():
	while 1:
		output_file = "codyStart.wav"
		MS.play_file(output_file) 
		
		# 등록 여부 말하기.
		cody = gv2t.getVoice2Text()
			
		# 이름이 none값이 아닌경우
		if "그" in cody :
			return "cody_call"# rander templete도 구현하기
		else :
			unknown_file = "unknown.wav"
			MS.play_file(unknown_file)
