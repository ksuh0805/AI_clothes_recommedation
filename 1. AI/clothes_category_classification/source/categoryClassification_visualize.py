import matplotlib.pyplot as plt
from PIL import Image
from model_test import Classify

width=5
height=5
rows = 2
cols = 4
axes = []
fig = plt.figure()

tb = input()               # top 또는 bottom을 입력시 적용됨...!
for a in range(rows*cols):
    img = ({'top': "./test_img_top/" + str(a+1) + ".jpg", 'bottom': "./test_img_bottom/" + str(a + 1) + ".jpg"}[tb])      # 이미지 경로 설정.
    b = Image.open(img)
    model = ({'top': 'top.pt', 'bottom': 'bottom.pt'}[tb])
    predict = Classify(model)
    prediction = predict.predict(img)
    k = fig.add_subplot(rows, cols, a+1)
    axes.append(k)
    if tb == 'top':
        subplot_title = ({0: "L_Blouse", 1: "L_Shirt", 2: "L_Sports-wear", 3: "L_Tee-shirt", 4: "S_Blouse", 5: "S_Shirt", 6: "S_Sports-wear", 7: "S_Tee-shirt"}[prediction])
    else:
        subplot_title = ({0: "Leggings", 1: "L_Chino", 2: "L_Denim", 3: "L_Skirt", 4: "S_Chino", 5: "S_Denim", 6: "S_Skirt", 7: "Sweats"}[prediction])
    axes[-1].set_title(subplot_title)
    k.axis('off')
    plt.imshow(b)
fig.tight_layout()
plt.show()