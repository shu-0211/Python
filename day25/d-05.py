# CNN실습시 필수: 코랩 오른쪽 상단에 -> 연결v 클릭하여 -> 런타임 유형 변경
    # T4 GPU( 그래픽 사용 ) 클릭 -> 저장 -> 연결

# 0) 실습에 필요한 데이터셋( SVHN 칼라의 0 부터 9 까지의 이미지 )
# https://ufldl.stanford.edu/housenumbers/
from torchvision import datasets
raw_train = datasets.SVHN( root='./data', split='train', download=True )
raw_test = datasets.SVHN( root='./data', split='test', download=True )

# 미니 배치 사용 

from torch.nn.modules.activation import ReLU
from torch.nn.modules.linear import Linear
from torch.nn.modules.pooling import MaxPool2d
# 0) GPU 연산 장치 설정
import torch # 'cuda' : 엔비디아 그래픽 드라이버 이름
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print( device )
# 1) 파이토치의 텐서 타입으로 변경
# 샘플로 2만개만 사용
# 연산속도 위한 cpu가 아닌 gpu 처리 .to( device )
# 0~255(밝기정도) 값들 0 ~ 1 정규화 # Y(타깃/정답) 제외
X_train = torch.tensor( raw_train.data[:20000], dtype=torch.float32).to( device ) / 255.0
Y_train = torch.tensor( raw_train.labels[:20000], dtype=torch.long).to( device )
X_test = torch.tensor( raw_test.data[:2000], dtype=torch.float32).to( device ) / 255.0
Y_test = torch.tensor( raw_test.labels[:2000], dtype=torch.long).to( device )

#===============================================================

from torch.utils.data import TensorDataset, DataLoader

# 1) 특성과 정답 1:1 매핑하여 묶음
train_dataset = TensorDataset( X_train, Y_train)

# 2- 묶은 데이터셋을 지정한 배치 크기 단위로 자르고 랜덤으로 병렬 로딩
train_loader = DataLoader( dataset=train_dataset, batch_size=128, shuffle=True )


#================================================================

# 2) 합성곱 신경망 레이어 컨테이너 설정
import torch.nn as nn
model = nn.Sequential(
    # (1) 레이어1: 합성곱 -> 렐루 -> 풀링
    # nn.Conv2d(in_channels=채널수(흑백1칼라3), out_channels=특징/특성 맵/개수
    # kernel_size=3(필터3*3) 5(5*5) , padding=패딩깊이(1)
    # 만약에 32픽셀 이미지 이라면 , (16,32,32 ) ( 특성수, 가로픽셀, 세로픽셀 )
    nn.Conv2d( in_channels=3, out_channels=16, kernel_size=3, padding=1),
    nn.ReLU(),
    # 만약에 앞전 합성곱 결과 특성맵 (16,32,32 ) 가정에 풀링 이후(stride가 2 이므로) ->  (16,16,16 )
    nn.MaxPool2d( kernel_size=2 , stride=2 ),
    # (2) 레이어2:레이어 추가 하여 중요한 특성 추가적으로 추출
    # 중간레이어는 앞전 레이어의 out_channels 특성 수와 일치
    nn.Conv2d( in_channels=16 , out_channels=32, kernel_size=3 , padding=1 ),
    # (16,16,16 ) -> (32,8,8)
    nn.ReLU(),
    nn.MaxPool2d( kernel_size=2, stride=2),
    # (3) 출력/분류기 레이어
    nn.Flatten() , # 32 * 8 * 8 (3차원) -> 2048(1차원) 으로 평탄화
    nn.Linear( in_features=32*8*8, out_features=64 ),
    nn.ReLU(),
    nn.Linear( in_features=64, out_features=10 )  # 최종 분류 레이어( 분류할 정답지/클래스 수 )
).to( device ) # GPU 연산 하라는 설정

# 3) 손실함수: 다중분류 이므로 소프트맥스
criterion = nn.CrossEntropyLoss()

# 4) 옵티마이저 ; optimizer = optim.AdamW( model.parameters(), lr=학습률)
import torch.optim as optim
optimizer = optim.AdamW( model.parameters() , lr = 0.005 )

# 5) 에포크(학습수) 단위 학습( 순전파 -> 오차계산 -> 역전파 -> 업데이트 )
for epoch in range( 100 ) :
    model.train()                           # 1- 학습모드
    ############# 미니 배치 단위 학습 ####################
    total_loss = 0.0
    for bach_X , bach_Y in train_loader :
      optimizer.zero_grad()                   # 2- 이전기울기 초기화
      logits = model(bach_X)                # 3- 순전파(학습)
      loss=criterion( logits, bach_Y )        # 4- 오차(학습과 정답 차이)
      loss.backward()                         # 5- 역전파(오차 이용한 기울기/미분 가중치/편향 기울기로 재설정 )
      optimizer.step()                        # 6- 가중치/편향 업데이트
      total_loss += loss.item()
    total_loss = total_loss / len( train_loader ) # 평균 오차
    ####################################################################################
    if epoch % 10 == 0 :
        print( epoch,": loss: ", loss.item() )

# 6) 모델 평가. model.train()학습모드 , model.eval() 평가/추론모드
model.eval()
with torch.no_grad() :
    test_logits = model( X_test ) # 테스트용 학습하기( 기울기 업데이트 안함 )
    test_pred = torch.argmax( test_logits , dim=1 ) # 확률중 가장 높은값 추출 ( 소프트맥스 )
    # 강아지?고양이?사자? [ 0.6 , 0.2.5 , 0.1.5  ]
from sklearn.metrics import accuracy_score # 정확도 # sklearn 에서 텐서 사용불가
# 텐서값들을 cpu로 변환후 넘파이로 변환
print( accuracy_score( Y_test.cpu().numpy() , test_pred.cpu().numpy()  ) ) # 0.7575 # 전체 실행마다 다름


# 1) 구글 코랩에서 업로드 
from google.colab import files 
upload = files.upload ()        # 1. 코랩 업로드 가능 
image_path = list(upload.keys())[0]  # 2. 업로드된 파일에 첫번째 파일경로 
print( image_path )
# 2. 사전학습된 ResNet50 모델 사용 , torchvision
import torch 
from torchvision import models
weights = models.ResNet50_Weights.DEFAULT   # ResNet50 모델의 가중치 기본값
model = models.resnet50( weights = weights )   # 해당 모델의 기본값 가중치 대입
# 3. 이미지 전처리(업로드한 이미지들이 차원이 다르다) 흑백은 1차원 , png(raba) 등등
preprocess = weights.transforms()        # 전처리 파이프라인 제공
from PIL import Image                             # 이미지 처리 제공
img = Image.open( image_path).convert('RGB')      # 강제로 칼라 이미지 변경 # ( 3, 가로, 세로 )
input_tensor = preprocess(img).unsqueeze(0)     # 배치 위한 배치 차춴추가 4차원변경
# .unsqueeze(0)  : 0번째 위치(맨 앞)에 크기가 1인 새로운 차원을 추가하는 함수


# 3. 사전학습된 모델로 추론
model.eval()            # 모델 학습이 아닌 추론 평가모드 
with torch.no_grad() :
  pred = model( input_tensor )
  preds = torch.nn.functional.softmax(pred[0] , dim = 0 ) # 다중분류 1000개

# 4. 확률이 큰 5개 클래스 추출 , torch.topk( 확률분호 , k )
top5_pred , top5_index = torch.topk( preds , 5 )
for i in range(5) :
  class_name = weights.meta['categories'][top5_index[i].item()]   # 사전모델 가중치에서 메타 정보 클래스 속서명
  print(class_name)


# [4] 합서곱 신경망 CNN + 미니배치 + 사전학습 ResNet50 전이학습
from torch.nn.modules.activation import ReLU
from torch.nn.modules.linear import Linear
from torch.nn.modules.pooling import MaxPool2d
# 0) GPU 연산 장치 설정
import torch # 'cuda' : 엔비디아 그래픽 드라이버 이름
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print( device )
# 1) 파이토치의 텐서 타입으로 변경
# 샘플로 2만개만 사용
# 연산속도 위한 cpu가 아닌 gpu 처리 .to( device )
# 0~255(밝기정도) 값들 0 ~ 1 정규화 # Y(타깃/정답) 제외
X_train = torch.tensor( raw_train.data[:20000], dtype=torch.float32).to( device ) / 255.0
Y_train = torch.tensor( raw_train.labels[:20000], dtype=torch.long).to( device )
X_test = torch.tensor( raw_test.data[:2000], dtype=torch.float32).to( device ) / 255.0
Y_test = torch.tensor( raw_test.labels[:2000], dtype=torch.long).to( device )

################## 미니 배치 설정 #########################
from torch.utils.data import  TensorDataset, DataLoader
# 1- 특성과 정답 1:1 매핑하여 묶음
train_dataset = TensorDataset( X_train, Y_train )
# 2- 묶은 데이터셋을 지정한 배치 크기 단위로 자르고 랜덤으로 병렬 로딩
train_loader = DataLoader( dataset=train_dataset, batch_size=128, shuffle=True )
######################################################

# 2) 기존 CNN 설정 지우고 사전학습으로 교체
################## 사전학습모델 #########################
import torch.nn as nn
import torchvision.models as models #
model = models.resnet50( weights= 'DEFAULT')      # 사전학습 모델에 저장된 가중치 
in_features = model.fc.in_features # 사전모델 학습의 특성맵 수 
# 다음 레이어 연결시 이전 레이어 특성맵의 수를 알아야한다.
model.fc = nn.Sequential(
    nn.Linear( in_features=in_features, out_features=128 ),
    nn.ReLU(), nn.Dropout( p=0.2 ) ,

    # 출력층
    nn.Linear(in_features=128 ,out_features=10 )
) 
model = model.to(device)  # GPU 사용하라는 함수 

# 3) 손실함수: 다중분류 이므로 소프트맥스
criterion = nn.CrossEntropyLoss()
# 4) 옵티마이저 ; optimizer = optim.AdamW( model.parameters(), lr=학습률)
import torch.optim as optim

#################### 사전학습 모델은 학습률 촘촘히 #######################

optimizer = optim.AdamW( model.parameters() , lr = 0.0001 )
# 5) 에포크(학습수) 단위 학습( 순전파 -> 오차계산 -> 역전파 -> 업데이트 )
for epoch in range( 5 ) :
    model.train()                           # 1- 학습모드
    ################## 미니 배치 단위 학습 #########################
    total_loss = 0.0
    for bach_X, bach_Y in train_loader :
        optimizer.zero_grad()                   # 2- 이전기울기 초기화
        logits = model( bach_X )                # 3- 순전파(학습)
        loss=criterion( logits, bach_Y )        # 4- 오차(학습과 정답 차이)
        loss.backward()                         # 5- 역전파(오차 이용한 기울기/미분 가중치/편향 기울기로 재설정 )
        optimizer.step()                        # 6- 가중치/편향 업데이트
        total_loss += loss.item()
    total_loss = total_loss / len( train_loader ) # 평균 오차
    #################################################################
    if epoch % 1 == 0 :
        print( epoch,": loss: ", total_loss )

# 6) 모델 평가. model.train()학습모드 , model.eval() 평가/추론모드
model.eval()
with torch.no_grad() :
    test_logits = model( X_test ) # 테스트용 학습하기( 기울기 업데이트 안함 )
    test_pred = torch.argmax( test_logits , dim=1 ) # 확률중 가장 높은값 추출 ( 소프트맥스 )
    # 강아지?고양이?사자? [ 0.6 , 0.2.5 , 0.1.5  ]
from sklearn.metrics import accuracy_score # 정확도 # sklearn 에서 텐서 사용불가
# 텐서값들을 cpu로 변환후 넘파이로 변환
print( accuracy_score( Y_test.cpu().numpy() , test_pred.cpu().numpy()  ) ) # 0.7575 # 전체 실행마다 다름

# 7) 모델 가중치 저장 , torch.save(model.state_dict() , '모델명.pth')
torch.save(model.state_dict() , 'resnet50_custom.pth')
print('가중치 저장성공')      # 머신러닝 pkl , 딥러닝 가중치 : pth , 딥러닝 모델 onnx => 스프링에서 실행됨. 
