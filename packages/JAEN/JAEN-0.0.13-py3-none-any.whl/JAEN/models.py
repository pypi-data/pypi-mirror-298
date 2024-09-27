import os
import torch
import torch.nn as nn

# CNN 모델 정의
class CNN(nn.Module):
    def __init__(self, pretrained=True):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(256 * 7 * 7, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)
        
        # pretrained가 True일 경우, 모델 가중치 로드
        if pretrained:
            self.load_pretrained_weights()

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = self.pool1(x)
        x = torch.relu(self.conv3(x))
        x = torch.relu(self.conv4(x))
        x = self.pool2(x)
        x = x.view(-1, 256 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    # 사전 학습된 가중치 로드 함수
    def load_pretrained_weights(self):
        current_dir = os.path.dirname(__file__)  # 현재 파일의 디렉토리 경로
        model_path = os.path.join(current_dir, 'data', 'models.pth')  # 모델 가중치 파일 경로
        
        if os.path.exists(model_path):
            self.load_state_dict(torch.load(model_path))  # 가중치 불러오기
            print("Pretrained weights loaded successfully.")
        else:
            raise FileNotFoundError(f"Model weights not found at {model_path}.")
