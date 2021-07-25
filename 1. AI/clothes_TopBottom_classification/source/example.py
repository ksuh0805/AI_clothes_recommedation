from keras.models import load_model
from binary_predict import is_top_clothes
# 라이브러리 임포트 하는 과정에서 시간이 오래 걸립니다!

model = load_model('./binary_class_cloth_more.h5')  # .h5 파일 경로

img_path = './business_item_0034.jpg' # 이미지 경로

res = is_top_clothes(model, img_path)
print(res)
# 상의면 1, 하의면 0 리턴
