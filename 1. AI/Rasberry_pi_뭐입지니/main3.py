import MicrophoneStream as MS
from detail import get_detail

detail = get_detail()

if detail=="sty/casual":
    MS.play_file("casual_resp.wav")
    # 캐주얼 스타일에 대한 추천 정보입니다. 추천 결과가 없다면 주변 매장에서 찾아보세요
elif detail=="sty/business":
    MS.play_file("business_resp.wav")
    # 캐주얼 스타일에 대한 추천 정보입니다. 추천 결과가 없다면 주변 매장에서 찾아보세요
elif detail=="sty/sports":
    MS.play_file("sports_resp.wav")
    # 캐주얼 스타일에 대한 추천 정보입니다. 추천 결과가 없다면 주변 매장에서 찾아보세요

# 필요한 wav
#  "camera_end.wav"--> 사진 촬영이 완료되었습니다. 분석 결과를 잠시 기다려주세요
#  casual/business/sports_resp.wav 각각 
# 4개정도?
