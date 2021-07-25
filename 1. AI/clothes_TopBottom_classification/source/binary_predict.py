#1. binary_predict
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # warning 메시지 제거
from keras.preprocessing import image
import numpy as np

# 이미지 전처리
def prep_img(img_path):
    image_w = 256
    image_h = 256
    pixels = image_w * image_h * 3

    img = image.load_img(img_path, target_size=(256, 256))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x.astype("float") / 256

    return x

# 상하의 분류모델
def is_top_clothes(model, img_path):
    preds = model.predict(prep_img(img_path))
    ans = ""
    res = -1
    if preds[0][0] > preds[0][1]:
        top = preds[0][0]/(preds[0][0]+preds[0][1])*100
        ans = str(round(top,5)) +"의 확률로 상의라고 판별되었습니다."
        res = [round(top, 5), 1] # res[0]: 확률 , res[1]:1 --> res[1]==1 이면 상의
    else:
        bottom = preds[0][1]/(preds[0][0]+preds[0][1])*100
        ans = str(round(bottom,5)) +"의 확률로 하의라고 판별되었습니다."
        res = [round(bottom,5),0]  # res[0]: 확률 , res[1]:0 --> res[1]==0 이면 하의

    print(ans)
    return res

# 색상 찾기
def what_color_is(model, img_path):
    preds = model.predict(prep_img(img_path))
    ans = ""

    color = {0:"black", 1:"white", 2:"beige", 3:"blue", 4:"red", 5:"pink", 6:"yellow", 7:"green"}
    max_idx = preds[0].argmax()

    sum_ = 0
    for i in preds[0]:
        sum_ = sum_+ i

    probability = preds[0][max_idx]/sum_*100

    ans = str(round(probability, 5))+"의 확률로 '" + color[max_idx] + "'라고 판별되었습니다."
    print(ans)
    list_ = [round(probability, 5),color[max_idx]] # list_[0]: 확률 , list_[1]: 색깔
    return list_