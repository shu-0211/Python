# [1] 합성곱 신경망 CNN


# CNN 실습시 필수 : 코랩 오른쪽 상단에 -> 연결 ->  클릭하여 런타임 유형 변경 -> T4 GPU 그래픽사용 클릭 -> 저장 -> 연결
# 이 실습에 필요한 데이터셋 ( 0부터 9까지 이미지)


from torchvision import datasets
raw_train = datasets.SVHN( root='./data', split='train', download=True )
raw_test = datasets.SVHN( root='./data', split='test', download=True )

# 0) GPU 연산 장치 설정
import torch # 'cuda' : 엔비디아 그래픽 드라이버 이름
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)
# 1) 딥러닝 하기 위한 파이토치 특성과 타깃 차원 일치화
# 샘플로 2만개 사용  # 연산속도 위한 cpu가 아닌 gpu 처리 .to(device)
X_train = torch.tensor(raw_train.data[:20000] , dtype=torch.float32).to(device) / 255.0
Y_train = torch.tensor(raw_train.labels[:20000], dtype=torch.long).to(device)

X_test = torch.tensor( raw_test.data[:2000] , dtype=torch.float32).to(device) / 255.0
Y_test = torch.tensor( raw_test.labels[:2000], dtype=torch.long).to(device)


# 2) 합성곱 신경망 레이어 컨테이너 설정
import torch.nn as nn
model = nn.Sequential(
    # (1) 입력층 : 합성곱 -> 렐루 -> 풀링
    # nn.Conv2d(in_channels=채널수(흑백1칼라3), out_channels=특징/특성 맵/개수
    # kernel_size=3(필터3*3) 5(5*5) , padding=패딩깊이(1)
    nn.Conv2d( in_channels=3 , out_channels = 16 , kernel_size=3 , padding=1 ),
    nn.ReLU(),
    # 만약에 앞전 합성곱 결과 특성맵 ( 16 ,32 , 32 )( 특성수 , 가로픽셀 , 세로픽셀 )( 16,16,16 )
    nn.MaxPool2d( kernel_size=2 , stride = 2 ),
    # (2) 은닉층
    nn.Conv2d( in_channels=16 , out_channels = 32 , kernel_size=3 , padding=1 ),
    nn.ReLU(),nn.MaxPool2d( kernel_size=2 , stride = 2 ),
    # (3) 출력/분류기 레이어
    nn.Flatten(),       # 32 * 8 * 8 ( 3차원) -> 2048(1차원)으로 평탄화
    nn.Linear( in_features=32*8*8 , out_features=64 ),
    nn.ReLU(),
    nn.Linear( in_features=64 , out_features=10 )
).to(device)

# 3) 손실함수: MSELoss() 회귀
crierion = nn.CrossEntropyLoss()

# 4) 옵티마이저 ; optimizer = optim.AdamW( model.parameters(), lr=학습률)
import torch.optim as optim
optimizer = optim.AdamW( model.parameters(), lr=0.005)

# 5) 에포크(학습수) 단위 학습( 순전파 -> 오차계산 -> 역전파 -> 업데이트 )
for epoch in range( 100 ) :
    model.train()                           # 1- 학습모드
    optimizer.zero_grad()                   # 2- 이전기울기 초기화
    logits = model( X_train)                # 3- 순전파(학습)
    loss=crierion( logits, Y_train )        # 4- 오차(학습과 정답 차이)
    loss.backward()                         # 5- 역전파(오차 이용한 기울기/미분 가중치/편향 기울기로 재설정 )
    optimizer.step()                        # 6- 가중치/편향 업데이트
    if epoch % 10 == 0 :
        print( epoch,": loss: ", loss.item() )
  

# 6) 모델 평가. model.train()학습모드 , model.eval() 평가/추론모드
model.eval()
with torch.no_grad() : 
  test_logits = model(X_test)     #테스트용 학습하기 ( 기울기 업데이트 안함)
  test_pred = torch.argmax( test_logits , dim=1)      # 확률중 가장 높은값 추출 ( 소프트 맥스 )

from sklearn.metrics import accuracy_score    # 정확도 , sklearn에서  xpstj tkdydqnfrk 
# 텐서값들을 Cpu로 변환후 넘파이로 변환
print( accuracy_score(Y_test.cpu().numpy() , test_pred.cpu().numpy() ) )

# 7) 모델 추론 # [ [ 공부시간,결석,G1,G2 ] ]
