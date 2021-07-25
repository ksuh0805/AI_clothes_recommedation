from __future__ import print_function


import time
import ex2_getVoice2Text as gv2t
import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import RPi.GPIO as GPIO
import MicrophoneStream as MS

GPIO.setmode(GPIO.BOARD)
GPIO.setup(31, GPIO.OUT)

def ledcontrol(result):
	text =result
	if text.find("불 켜")>=0:
		print("불이 켜집니다.")
		GPIO.output(31, GPIO.HIGH)
		return("불이 켜집니다.")
		
	elif text.find("불 꺼")>=0:
		print("불이 꺼집니다.")
		GPIO.output(31, GPIO.LOW)
		return("불이 꺼집니다.")
		
	else:
		return("정확한 명령을 말해주세요")
		
def main():
		#Example7 KWS+STT
		
	KWSID = ['기가지니', '친구야', '지니야', '자기야']
	
	while 1:
		recog = kws.test(KWSID[0])
		if recog == 200:
			print('KWS Detected ...\n Start STT...')
			text = gv2t.getVoice2Text()
			print('Recognized Text: '+text)
			tts.getText2VoiceStream(ledControl(text), "result_TTS.wav")
			MS.play_file("result_TTS.wav")
			time.sleep(2)
			
		else:
			print('KWS Not Detected...')
		
	if __name__ == '__main__':
		try:
			main()
		finally:
			GPIO.cleanup()
			
