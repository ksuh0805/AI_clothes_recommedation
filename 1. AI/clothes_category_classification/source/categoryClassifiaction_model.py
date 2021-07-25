from __future__ import print_function, division

import torch
import torch.utils.data
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import datasets, models, transforms
import os
import copy

import time
import datetime


def main():

    start = time.time()

    # 이미지 데이터 전처리
    data_transforms = {
        'train': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean(r,b,g), stdv(r,b,g)
        ]),
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # mean(r,b,g), stdv(r,b,g)
        ]),
    }

    # Split된 train, test data load.
    data_dir = 'color'
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}

    # 학습시 batch_size = 5로 설정.
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=5,
                                                  shuffle=True, num_workers=2)
                   for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}

    # GPU에 할당.
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # 모델 Training
    def train_model(model, criterion, optimizer, scheduler, num_epochs=25):

        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0

        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            for phase in ['train', 'val']:
                if phase == 'train':
                    model.train()
                else:
                    model.eval()

                running_loss = 0.0
                running_corrects = 0

                # Iterate
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)

                    optimizer.zero_grad()

                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)

                        if phase == 'train':
                            loss.backward()
                            optimizer.step()

                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]

                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))

                # deep copy the model
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

        print('Best val Acc: {:4f}'.format(best_acc))

        # load best model weights
        model.load_state_dict(best_model_wts)
        return model

    model_ft = models.densenet201(pretrained=True)          # Pretrained with imagenet & densenet201
    num_ftrs = model_ft.classifier.in_features
    model_ft.fc = nn.Linear(num_ftrs, 8)                    # 직접 8개로 분류하도록 수정
    model_ft = model_ft.to(device)                          # GPU에 할당
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)            # SGD with lr=0.001, momentum=0.9
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

    # Train_model
    model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                           num_epochs=20)

    sec = time.time() - start
    times = str(datetime.timedelta(seconds=sec)).split(".")
    times = times[0]
    print(times)

    # save model
    torch.save(model_ft, "top.pt")


if __name__ == '__main__':
    torch.multiprocessing.freeze_support()
    main()