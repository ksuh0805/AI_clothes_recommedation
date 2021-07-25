#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import time
import pdb
from threading import Timer
from check import get_name, user_mod, closet_open,gene_call,cody_start, profile_end
from check_gender import get_gender
from check_age import get_age
from check_height import get_height
from check_weight import get_weight
from camera_01 import clothes_photo
from camera_02 import photo_continue
from detail import get_detail
import MicrophoneStream as MS
ser=serial.Serial(
	port='/dev/ttyGS0',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0
)

print(ser.portstr)

gene=gene_call()
ser.write(gene.encode())
print("done")

#기가지니한테 유저 정보를 입력 받아 서버로 전송
name=get_name()
ser.write(name.encode())

print("gender Start")
gender = get_gender()
ser.write(gender.encode())
print("age Start")	
age = get_age()
ser.write(age.encode())
print("height Start")
height = get_height()
ser.write(height.encode())
print("weight Start")
weight = get_weight()
ser.write(weight.encode())

# 프로필 등록이 완료되었습니다.
profile_end()

#새로운 옷 등록 여부 질문
closet = closet_open()
#옷 촬영 안내 가이드
cl_photo = clothes_photo()

#사진 촬영 안내 후 main3.py 실행
output_name = "camera_end.wav"
MS.play_file(output_name)




# # 
# closet = closet_open()
# ser.write(closet.encode())

# #rec/snap:사진찍기
# #con/yes:추가 옷 등록"
# #사진 등록이라면
# if closet == "rec/yes":
# 	while True:
# 		cl_photo = clothes_photo()
# 		ser.write(cl_photo.encode())
# 		rec = photo_continue()
# 		ser.write(rec.encode())
# 		#다시 찍지 않으면 탈출
# 		if rec == "con/no":
# 			break
			
# print("success")		
# codyCall = cody_start()
# ser.write(codyCall.encode())


# detail = get_detail()
# ser.write(detail.encode())
