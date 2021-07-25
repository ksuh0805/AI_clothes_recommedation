import cv2


# input: split 할 file 디렉토리(file_dir), split할 이미지 다운로드할 디렉토리(down_dir)
# top_[filename], bottom_[filename] 형식으로 이미지 저장

# 실행할 때 필요한 파일 두개:
# 1) pose_deploy_linevec_faster_4_stages.prototxt (default: './')
# 2) pose_iter_160000.caffemodel (default: './')
def cut_img(file_d, down_dir: str):
    # MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
    BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                  "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                  "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
                  "Background": 15}

    # 각 파일 path
    protoFile = "./pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "./pose_iter_160000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    image = file_d
    imageHeight, imageWidth, _ = image.shape

    # network에 넣기위해 전처리
    inpBlob = cv2.dnn.blobFromImage(image, 1.0 / 255, (imageWidth, imageHeight), (0, 0, 0), swapRB=False, crop=False)

    # network에 넣어주기
    net.setInput(inpBlob)

    # 결과 받아오기
    output = net.forward()

    # output.shape[0] = 이미지 ID, [1] = 출력 맵의 높이, [2] = 너비
    H = output.shape[2]
    W = output.shape[3]

    # 키포인트 검출시 이미지에 그려줌
    points = []
    for i in range(0, 15):
        if i not in [8, 11]:
            continue

        # 해당 신체부위 신뢰도 얻음.
        probMap = output[0, i, :, :]

        # global 최대값 찾기
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # 원래 이미지에 맞게 점 위치 변경
        x = (imageWidth * point[0]) / W
        y = (imageHeight * point[1]) / H
        if prob > 0.1:
            points.append((int(x), int(y)))
        else:
            points.append(None)
    if points[0] is None and points[1] is None:
        return None, None
    border = min(points[0][1], points[1][1])
    img_top = image[:border, :]
    img_bottom = image[border:, :]
    # 이미지 저장
    # down_file = down_dir + file_dir.split('/')[-1]
    # print(down_file)
    return img_top, img_bottom
    # cv2.imwrite(down_dir + 'top_' + file_dir.split('/')[-1], img_top)
    # cv2.imwrite(down_dir + 'bottom_' + file_dir.split('/')[-1], img_bottom)

