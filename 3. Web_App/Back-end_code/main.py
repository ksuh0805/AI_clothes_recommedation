# pip install flask
# pip install opencv-python
import os
import serial
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # warning 메시지 제거
import joblib
from flask import Flask, request, render_template, url_for, session
import requests
import json
from models.category_classification_model import recommend2
from keras.models import load_model
# 상의인지 하의인지 구분해주는 모델 - 옷 등록할때 필요
from models.binary_predict import is_top_clothes, what_color_is
from models.cate_predict import define_category
import torch
from models.select_clothes import last_item_list
import pymysql
#from models.segmentation import crop_detect_segment

# 시리얼 통신 포트
ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

# Flask 함수 구현

app = Flask(__name__)

file = 'static/src/images/image.jpg'
if os.path.isfile(file):
    os.remove(file)

category = ["long_blouse/long_chino","short_tee/short_skirt","long_sports/sweats","short_sports/leggings",
       "short_shirt/long_chino","long_shirt/long_chino","short_blouse/long_chino","short_tee/short_chino",
       "long_sports/leggings","short_sports/sweats","long_tee/long_denim","long_tee/long_skirt",
       "short_tee/long_denim","short_tee/long_skirt",
        "short_tee/long_chino","long_tee/long_chino","short_tee/short_denim"]
weatherCa = ["sunny","cloudy","rainy"]
styleCa = ["business","casual","sports"]
sexCa = ["male","female"]
boShapeCa = ["thin","normal","fat"]


# features 전역변수 초기화
u_name = "user000"
u_gender = "male"
u_height = "170"
u_weight = "70"
u_age = 20
u_bodyshape = 'normal'
u_weather = ""
u_temp = ""
u_style = "casual"
top_path = ""
bot_path = ""

#모델 경로 지정
# model_route = "models/rfr_model_nhw.pkl"

model_reco = joblib.load("models/rfr_model_lnhw.pkl")
model_binary = load_model('models/binary_class_cloth_more.h5')
model_color = load_model('models/color_classify_lastlast.h5')
# model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)        # 따로 빼고
#model = torch.load('models/best_deeplabv3_resnet50_voc_os16.pth',map_location=torch.device('cpu'))
model_cate_top = torch.load('models/top.pt', map_location=torch.device('cpu'))
model_cate_bottom = torch.load('models/bottom.pt', map_location=torch.device('cpu'))
ser.close()
@app.route('/')
def root():
    return render_template('index.html')

# 이름을 입력받는 함수
@app.route('/check_name')
def check_name():
    global ser
    ser.open()

    # 지니 콜이 들어오면 반복문 탈출
    while True:
        if ser.readable():
            res = ser.readline().decode()
            print(res)
            if res == "gene_call":
                break
    # global ser
    # ser.close()
    return render_template('/check_name.html')

# 성별을 입력받는 함수
@app.route('/check_gender')
def check_gender():
    global u_name
    global ser
    # ser.open()
    while True:
        if ser.readable():
            res = ser.readline().decode()

            if res:
                print(res)
                break

    # 인풋값을 스플릿해서 전역변수에 저장
    res = res.split(sep="/")
    u_name = res[1]
    print(u_name)

    return render_template('/check_gender.html')

# 사용자 정보를 수정하는 함수
@app.route('/check_modify')
def check_modify():

    global ser
    res = ""
    while True:
        if ser.readable():
            res = ser.readline().decode()

            if res=='yes' or res=="no":
                res1=res
                print(res1)
                break

    return render_template('/check_modify.html', res1=res1)

    # if res == "yes":
    #     return render_template('/check_gender.html')
    # elif res == "no":
    #     return render_template('/check_end.html')

# 나이를 입력받는 함수
@app.route('/check_age')
def check_age():
    global ser
    global u_gender
    while True:
        if ser.readable():
            res = ser.readline().decode()
            print(res)
            if res:
                break
    # 인풋값을 스플릿해서 전역변수에 저장
    res = res.split(sep="/")
    u_gender = res[1]

    return render_template('/check_age.html')

# 몸무게를 입력받는 함수
@app.route('/check_weight')
def check_weight():
    global ser
    global u_height
    while True:
        if ser.readable():
            res = ser.readline().decode()
            print(res)
            if res:
                break
    # 인풋값을 스플릿해서 전역변수에 저장
    res = res.split(sep="/")
    u_height = res[1]
    return render_template('/check_weight.html')

# 키를 입력받는 함수
@app.route('/check_height')
def check_height():
    global ser
    global u_age

    while True:
        if ser.readable():
            res = ser.readline().decode()
            print(res)
            if res:
                break
    # 인풋값을 스플릿해서 전역변수에 저장
    res = res.split(sep="/")
    u_age = res[1]
    return render_template('/check_height.html')

# 입력받은 사용자 프로필 정보를 저장하는 함수
@app.route('/check_end')
def check_end():
    global ser
    global u_weight

    global u_age
    global u_name
    global u_gender
    global u_height

    while True:
        if ser.readable():
            res = ser.readline().decode()
            print(res)
            if res:
                break

    res = res.split(sep="/")
    u_weight = res[1]
    # global ser
    #
    # while True:
    #     if ser.readable():
    #         res = ser.readline().decode()
    #         print(res)
    #         if res == "gene_call":
    #             break

    return render_template('/check_end.html', name=u_name, gender=u_gender, age=u_age, height=u_height, weight=u_weight)

# 입력받은 사용자 프로필 정보를 DB에 저장하는 함수
@app.route('/closet', methods=['GET', 'POST'])
def closet():

    # global ser
    #
    # while True:
    #     if ser.readable():
    #         res1 = ser.readline().decode()
    #         print(res1)
    #         if res1 == "gene_call":
    #             break

    global u_name
    global u_gender
    global u_height
    global u_weight
    global u_age

    if request.method == "POST":
        # 이미 동일한 이름이 있을 경우

        # -> DB에서 같은 이름 프로필정보 불러오기
        conn = pymysql.connect(host='localhost', user='root', password='1234', db='flask_test', charset='utf8')
        cursor = conn.cursor()

        sql = "UPDATE userprofile SET age=%s,gender=%s,height=%s,weight=%s,bodyform=%s WHERE username=%s"
        res = cursor.execute(sql, (u_age,u_gender,u_height,u_weight,'normal',u_name))

        conn.commit()
        conn.close()

        # AI 모델링과의 연동
        # global ser
        # res = ""
        # while True:
        #     if ser.readable():
        #         res = ser.readline().decode()
        #
        #         if res == 'rec/yes' or res == "rec/no":
        #             res1 = res
        #             print(res1)
        #             break

    return render_template('/closet.html')

@app.route('/closet_check')
def closet_check():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='flask_test', charset='utf8')
    cursor = conn.cursor()

    sql_1 = "select item_id from top"
    res_1 = cursor.execute(sql_1)
    rows_1 = cursor.fetchall()
    for result_1 in rows_1:
        pass

    sql_2 = "select item_id from bottom"
    cursor.execute(sql_2)
    rows_2 = cursor.fetchall()
    for result_2 in rows_2:
        pass

    conn.commit()
    conn.close()

    return render_template('/closet_check.html')

@app.route('/camera_01')
def camera_01():
    return render_template('/camera_01.html')

@app.route('/indicator')
def template():
    return render_template('/indicator.html')

# 이미지 파일을 받아서 분류 후 데이터베이스에 저장
@app.route('/camera_02')
def camera_02():
    global u_name
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='flask_test', charset='utf8')
    cursor = conn.cursor()

    filename = "image"
    path = "C://Users/ehdgn/PycharmProjects/KT_Backend/static/src/images/" + str(filename) + ".jpg"
    #single_pred = crop_detect_segment(model, filename, path)
    #if single_pred[0]:
    res_bin = is_top_clothes(model_binary, path) #res_bin[0] : 확률 1 : 여부
    res_color = what_color_is(model_color, path) #res_color[0] : 확률 1 : 색깔
    res_cate = define_category({1: model_cate_top, 0: model_cate_bottom}[res_bin[1]], res_bin[1], path) # res_cate[0]: 확률값, 1: 카테고리

    if res_bin[1] == 1:
        #single_pred[1].save("C://Users/ehdgn/PycharmProjects/KT_Backend/static/src/images/" + filename + "_top.jpg")
        topbot = "상의"
        sql = "INSERT INTO top VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, ('image', u_name, res_color[1], res_cate[1]))
        # Top table 이름 색상 카테고리
    else:
        #single_pred[1].save("C://Users/ehdgn/PycharmProjects/KT_Backend/static/src/images/" + filename + "_bottom.jpg")
        topbot = "하의"
        sql = "INSERT INTO bottom VALUES (%s,%s,%s,%s)"
        cursor.execute(sql, ('image', u_name, res_color[1], res_cate[1]))
        # Bottom table

    return render_template('/camera_02.html', topbot=topbot, topbot_pro=res_bin[0], color=res_color[1], color_pro=res_color[0], cate=res_cate[1], cate_pro=round(res_cate[0] * 100, 5))

    # else:
    #     top_path_new = "C://Users/ehdgn/PycharmProjects/KT_Backend/static/src/images/" + str(filename) + "_top.jpg"
    #     bottom_path_new = "C://Users/ehdgn/PycharmProjects/KT_Backend/static/src/images/" + str(filename) + "_bottom.jpg"
    #     top_color = what_color_is(model_color, top_path_new)  # res_color[0] : 확률 1 : 색깔
    #     bottom_color = what_color_is(model_color, bottom_path_new)  # res_color[0] : 확률 1 : 색깔
    #     top_cate = define_category(model_cate_top, 1, top_path_new)  # res_cate[0]: 확률값, 1: 카테고리
    #     bottom_cate = define_category(model_cate_bottom, 0, bottom_path_new)  # res_cate[0]: 확률값, 1: 카테고리
    #
    #     sql = "INSERT INTO top VALUES (%s,%s,%s,%s)"
    #     res = cursor.execute(sql, ('image_top', u_name, top_color[1], top_cate[1]))
    #     sql = "INSERT INTO bottom VALUES (%s,%s,%s,%s)"
    #     res = cursor.execute(sql, ('image_bottom', u_name, bottom_color[1], bottom_cate[1]))

        # return render_template('/camera_02.html', topbot="상의", topbot_pro="90", color=top_color[1],
        #                        color_pro=top_color[0], cate=top_cate[1], cate_pro=round(top_cate[0] * 100, 5))
    # slicing
    # 파일이름바꿔@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


@app.route('/camera_03')
def camera_03():
    return render_template('/camera_03.html')

# 위치 정보 가져오는 함수
def latlon() :
    # ip 기반의 위도 경도 반환 API
    key = '7622bba5d9247cd03af5c3e4c76800bb'
    send_url = 'http://api.ipstack.com/check?access_key=' + key

    spot = []

    r = requests.get(send_url)
    j = json.loads(r.text)

    # 위도 경도 값을 전역변수에 저장
    u_lat = j['latitude']
    u_lon = j['longitude']

    spot.append(u_lat)
    spot.append(u_lon)

    return spot

@app.route('/detail')
def detail():
    global u_temp
    global u_weather
    global u_style
    lat = latlon()[0]
    lon = latlon()[1]

    # 위도 경도를 기반으로 날씨 정보 반환하는 API
    w_key = '9224dde938857fba3d6eb23f9ddc9529'
    w_url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + w_key

    w_r = requests.get(w_url)
    w_j = json.loads(w_r.text)

    # 섭씨로 변환
    k2c = lambda k: k - 273.15

    # 기온과 날씨 값을 전역변수에 저장
    temp = k2c(w_j['main']['temp'])
    weather = w_j["weather"][0]["main"]

    # 프론트에 맞게 데이터 변환
    if weather == 'Rain' or weather == 'Thunderstorm' or weather == 'Drizzle' or weather == 'Mist':
        f_weather = '비오는'
    elif weather == 'Clear':
        f_weather = '맑은'
    elif weather == 'Clouds' or weather == 'Atmosphere':
        f_weather = '구름 많은'
    else:
        f_weather = weather

    # AI 라벨에 맞게 데이터 변환
    if weather == 'Rain' or weather == 'Thunderstorm' or weather == 'Drizzle' or weather == 'Mist':
        u_weather = 'rainy'
    elif weather == 'Clear':
        u_weather = 'sunny'
    elif weather == 'Clouds' or weather == 'Atmosphere':
        u_weather = 'cloudy'
    else:
        u_weather = weather

    u_temp=round(float(temp), 1)

    return render_template('/detail.html', temp=round(float(temp), 1), weather=f_weather)

@app.route('/result', methods=['GET', 'POST'])
def result():
    global u_style
    global u_bodyshape
    global top_path
    global bot_path
    global u_temp
    global u_weather
    global u_name

    # 프로필정보
    if request.method == "POST":
        data = request.get_json()
        print(data)
        u_style = data['style']
    print(u_style)

    # 온도 날씨 스타일
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='flask_test', charset='utf8')
    cursor = conn.cursor()

    dict_1 = {}
    i = 0
    sql_1 = "SELECT * FROM top"
    cursor.execute(sql_1)
    rows_1 = cursor.fetchall()
    # payload = []
    for result_1 in rows_1:
        dict_1[i] = {'item_id': result_1[0], 'username': result_1[1], 'color': result_1[2], 'item_shape': result_1[3]}
        i = i + 1

    dict_2 = {}
    i = 0
    sql_2 = "SELECT * FROM bottom"
    cursor.execute(sql_2)
    rows_2 = cursor.fetchall()

    # 옷정보를 저장
    for result_2 in rows_2:
        dict_2[i] = {'item_id': result_2[0], 'username': result_2[1], 'color': result_2[2], 'item_shape': result_2[3]}
        i = i+1
        
    # 적합한 코디 추천 쌍을 리턴합니다.
    reco_res = recommend2(model_reco, u_temp, u_weather, u_age, u_gender, u_height, u_weight, u_bodyshape, u_style)

    # 적합한 상의 코디 이미지를 불러옵니다.
    t_path = last_item_list(u_name, dict_1, dict_2, reco_res[0])[0]
    print("상의" + t_path)
    top_path = "../static/src/images/" + str(t_path) + ".jpg"

    # 적합한 하의 코디 이미지를 불러옵니다.
    b_path = last_item_list(u_name, dict_1, dict_2, reco_res[0])[1]
    print("하의" + b_path)
    bot_path = "../static/src/images/" + str(b_path) + ".jpg"

    per = reco_res[1] * 100

    conn.commit()
    conn.close()

    return render_template('/result.html', top_img=top_path, bottom_img=bot_path, per=round(per,3), reco_res=reco_res[0], t_path=t_path)

@app.route('/result_no')
def result_no():

    global u_gender
    global u_style

    if u_gender == "남자":
        u_gender = 'male'

    # 취향에 맞는 옷이 있는 매장을 추천해주기 위해 변수값 전달
    gs = u_gender + "_" + u_style

    return render_template('/result_no.html', sexCategory=gs)

if __name__ == '__main__':
    app.debug = True
    app.run()