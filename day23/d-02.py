# [1] 신경망 ANN 이용한 이진분류

import pandas as pd

url = 'https://raw.githubusercontent.com/rickiepark/hg-mldl/master/wine.csv'
df = pd.read_csv( url )

X = df[ ['alcohol', 'sugar', 'pH'] ] #
Y = df['class']           # (0:레드와인, 1:화이트와인)

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42, stratify=Y)

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train_scaled = ss.fit_transform( X_train )
X_test_scaled = ss.transform( X_test )

# 1) 딥러닝 하기 위한 파이토치
print( X_train.shape ) # (5197, 3)
print( Y_train.shape ) # (5197,)
# torch.tensor(자료 , dtype=torch.비트 타입수 ) : 텐서타입으로 변환
import torch
X_train = torch.tensor( X_train_scaled, dtype=torch.float32 )
X_test = torch.tensor( X_test_scaled, dtype=torch.float32 )
# 특성 [ [] ] 과 타깃의 차원 수 일치화
Y_train = torch.tensor( Y_train.values , dtype = torch.float32 ).unsqueeze(1)
Y_test = torch.tensor( Y_test.values , dtype = torch.float32 ).unsqueeze(1)
print( X_train.shape ) # torch.Size([5197, 3])
print( Y_train.shape ) # torch.Size([5197, 1])

# 2) 신경망ANN 레이어 컨테이너 설정
import torch.nn as nn
#model = nn.Sequential( 입력층 -> 은닉층 -> 출력층 )
model = nn.Sequential(
    # nn.Linear( 피처수, 파생피처수)
    nn.Linear( 3, 16 ), # 입력층에서는 최초의 학습할 피처/특성 수
    nn.ReLU(), # 활성화함수, 음수값은 0으로 양수값은 그대로 통과( 음수이면 버리기)
    # nn.Linear( 앞전레이어의피처수, 결과수 )
    nn.Linear( 16 , 1) # 출력층
)

# 3) 손실함수 :
crierion = nn.BCEWithLogitsLoss()

# 4) 옵티마이저 : optimizer = optiom.AdamW(model.parameters() ,lr=학습률)
import torch.optim as optim
optimizer = optim.AdamW(model.parameters( ) , lr=0.01)

# 5) 에포크(학습수) 단위학습 (순전파 -> 역전파)
for epoch in range(1000) :
  model.train()   # 5-1 학습한다.
  optimizer.zero_grad()     # 5-2 이전 에포크의 계산된 기울기초기화
  logits = model(X_train)   # (순전파) 5-3 학습 자료 넣어서 학습
  loss = crierion( logits  ,Y_train ) # ( 손실)  5-4 정답과 비교해여 손실시례
  loss.backward()                   #(역전파) 5-5 각 가중치에 기울기를 계산
  optimizer.step()                  # (업데이트) 5-6 가중치 반영
  #===============================================================
  if epoch % 100 == 0 :
    print(epoch , ": loss : " , loss.item())


# 6) 모델 평가 , model.train() 학습모드 , model.eval() 평가 / 추론모드
model.eval()    # 추론/평가 모드로 전환
with torch.no_grad() : # 기울기 저장 안함
  train_pred = (torch.sigmoid(model(X_train)) > 0.5).float()
  test_pred = (torch.sigmoid(model(X_test)) > 0.5).float()

# 7) f1-score
from sklearn.metrics import f1_score
print( train_pred.numpy() )
print( f1_score( Y_train.numpy() , train_pred.numpy()  , average='macro') )
print( f1_score( Y_test.numpy() , test_pred.numpy()  , average='macro') )
