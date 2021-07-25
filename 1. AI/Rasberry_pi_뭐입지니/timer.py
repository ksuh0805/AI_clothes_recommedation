
from __future__ import print_function


import time
import ex2_getVoice2Text as gv2t
import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import RPi.GPIO as GPIO
import MicrophoneStream as MS

import threading

def main():
		
	KWSID = ['기가지니', '친구야', '지니야', '자기야']
	
	while 1:
		recog = kws.test(KWSID[0])
		if recog == 200:
			print('KWS Detected ...\n Start STT...')
			tts.getText2VoiceStream("채연아!!!!!!!!!!!!!!!!!!!!!", "result_TTS.wav")
			MS.play_file("result_TTS.wav")
			time.sleep(5)
			
			tts.getText2VoiceStream("채연이가 대답했습니다.", "result_TTS.wav")
			MS.play_file("result_TTS.wav")
			time.sleep(2)
			
		else:
			print('KWS Not Detected...')
		
if __name__ == '__main__':
	try:
		main()
	finally:
		GPIO.cleanup()
			

