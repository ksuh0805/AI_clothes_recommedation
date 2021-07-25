import torch.utils.data
from PIL import Image
from torch.autograd import Variable
from torchvision import transforms
import time

class Classify:
    def __init__(self, mod):
        self.mod = mod

    def predict(self, img):
        # model load
        model = torch.load(self.mod, map_location=torch.device('cpu'))
        model.eval()

        # 이미지 데이터 전처리
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean(r,b,g), stdv(r,b,g)
        ])

        # 이미지 분류 예측
        input_image = Image.open(img)
        image_tensor = preprocess(input_image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        output = model(input)
        index = output.data.cpu().numpy().argmax()
        #softval = f.softmax(output, dim=1).cpu().detach().numpy()[0][index]
        #if softval >= 0.1:
        #    return index
        #else:
        #    return None
        return index

start = time.time()
pre = Classify("bottom.pt")           # 상의, 하의에 맞게 모델 설정
print(pre.predict('camera_test_bottom.jpg'))  # 이미지 경로 설정.
sec = time.time() - start
print("Time taken to analyze:", sec, "seconds")



# 하의 카테고리: {0: "long_blouse", 1: "long_shirt", 2: "long_sports", 3: "long_tee",
#                4: "short_blouse", 5: "short_shirt", 6: "short_sports", 7: "short_tee"}

# 상의 카테고리 = {0: "leggings", 1: "long_chino", 2: "long_denim", 3: "long_skirt",
#                 4: "short_chino", 5: "short_denim", 6: "short_skirt", 7: "sweats"}
