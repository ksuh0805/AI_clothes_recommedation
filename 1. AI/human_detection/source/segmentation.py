import torch
from torchvision import transforms
import numpy as np
from pose_detection import cut_img
from PIL import Image
import cv2

# model load
model = torch.hub.load('pytorch/vision:v0.7.0', 'deeplabv3_resnet101', pretrained=True)
model.eval()

# 이미지 투명화

def transparency(url, type, single):            # single: 1 = True, 0 = False
    if single == 0:
        img = cv2.cvtColor(url, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
    else:
        img = url
    img = img.convert("RGBA")

    datas = img.getdata()

    newData = []

    for items in datas:
        if items[0] == 255 and items[1] == 255 and items[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(items)

    img.putdata(newData)
    img.show()
    img.save('./' + type + '_trans.png', "PNG")

# image reshape & crop
def crop_detect_segment(img_name):
    im = Image.open(img_name + '.jpg').convert('RGB')

    # crop image
    im = im.crop((330, 400, 630, 1300))   # change by image size

    # resize image
    width, height = im.size
    input_image = im.resize((width//2, height//2))
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    # human detection
    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")

    # plot the semantic segmentation predictions of 21 classes in each color
    r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(input_image.size)
    r.putpalette(colors)

    # image segmentation
    masking_val = np.array(r)
    present_img = np.array(input_image)
    width, height = masking_val.shape
    for i in range(width):
        for j in range(height):
            if masking_val[i][j] == 0:
                present_img[i][j][0] = 255
                present_img[i][j][1] = 255
                present_img[i][j][2] = 255
    im = Image.fromarray(present_img)
    imcv = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)

    # pose detection
    img_top, img_bottom = cut_img(imcv, './')

    # 상의 또는 하의 하나의 이미지가 들어온 경우 또는 상하의 한번에 들어온 이미지의 경우,
    if img_top is None and img_bottom is None:          # 단일 아이템인 경우
        im = im.crop((330, 400, 630, 1300))           # 단일 아이템이면 상체부분에 맞게 crop 설정 필요.
        im.save(img_name + '_crop.jpg')
        transparency(im, img_name, 1)
    else:                                               # 전신사진의 경우
        cv2.imwrite(img_name + '_top.jpg', img_top)
        cv2.imwrite(img_name + '_bottom.jpg', img_bottom)
        transparency(img_top, img_name + '_top', 0)
        transparency(img_bottom, img_name + '_bottom', 0)