from random import randint

# 색상 조합
def is_good_comb(top, bottom):
    color = {"black": 0, "white": 1, "beige": 2, "blue": 3, "red": 4, "pink": 5, "yellow": 6, "green": 7}
    comb = [[1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 0, 0, 1, 1]]

    return comb[color[bottom]][color[top]] # 바람직한 조합에 대해서 1, 아니면 0 return

# 데이터베이스에서 올바른 상/하의 이미지 가져오기
def last_item_list(u_name, db_top,db_bot,reco_res):
    num_rand = 3 # 랜덤 상의 몇번 선택할지

    # 데이터베이스 attribute
    item_id='item_id'
    color='color'
    item_shape='item_shape'
    uname='username'

    # exception flag-> 데이터베이스에 해당하는 옷이 없을 때 flag 1로 바꾸기
    exc_flag = 0

    # reco_res = "long_shirt/short_skirt" # 모델을 통해서 나온 output 형식

    reco = reco_res.split(sep='/')
    reco_top = reco[0] # 모델이 추천한 상의
    reco_bot = reco[1] # 모델이 추천한 하의

    last_top="" # 최종적으로 return 할 상의 item_id
    last_bot="" # 최종적으로 return 할 하의 item_id

    db_reco_top_list = [] # db에 저장된 특정 카테고리를 받을 상의 리스트 선언
    db_reco_bot_list = [] # db에 저장된 특정 카테고리를 받을 하의 리스트 선언

    for i in db_top: # top 데이터베이스에서 해당하는 user의 옷 데이터만 리스트로 가져오기
        top=db_top[i]
        if top[uname] == u_name:
            if reco_top == top[item_shape]:
                db_reco_top_list.append(top)

    for i in db_bot:# bottom 데이터베이스에서 해당하는 user의 옷 데이터만 리스트로 가져오기
        bot = db_bot[i]
        if bot[uname] == u_name:
            if reco_bot == bot[item_shape]:
                db_reco_bot_list.append(bot)

    for i in range(num_rand): # 최대 num_rand 횟수만큼 찾아보기
        if len(db_reco_top_list) == 0 or len(db_reco_bot_list) == 0:
            exc_flag = 1 # 데이터베이스에 해당하는 값이 없으면 flag 1로 바꾸고 탐색 종료
            break

        rand_idx = randint(0, len(db_reco_top_list)-1)
        top_color = db_reco_top_list[rand_idx][color] # 색 조합 판별
        for bot in db_reco_bot_list:
            res = is_good_comb(top_color,bot[color])
            if res == 1:
                last_top = db_reco_top_list[rand_idx][item_id]
                last_bot = bot[item_id]
                exc_flag = 0 # 적합한 옷을 찾았다면 flag 0 & 탐색 종료
                break
            exc_flag = 1

    last_style = [last_top, last_bot] # 최종 item_id
    if exc_flag == 1:
        last_style = ["geo","geo"] # 값이 없을 때 geo master로 넘어가기 위한 임의 list

    print(exc_flag)

    return last_style