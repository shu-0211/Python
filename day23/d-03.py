# [2] 신경망 DNN 이용한 이진분류

import pandas as pd 
url = 'https://raw.githubusercontent.com/arunk13/MSDA-Assignments/master/IS607Fall2015/Assignment3/student-mat.csv' 
df = pd.read_csv( url, sep=';' ) 
X = df[ ['studytime', 'absences', 'G1', 'G2'] ] 
Y = df['G3']                  

from sklearn.model_selection import train_test_split 
X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.2, random_state=42 )

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train_scaled = ss.fit_transform( X_train ) 
X_test_scaled = ss.transform( X_test )   

# 1) 딥러닝 하기 위한 파이토치 특성과 타킷 차원 일치화

X_train = torch.tensor( X_train_scaled, dtype=torch.float32 )
X_test = torch.tensor( X_test_scaled, dtype=torch.float32 )
Y_train = torch.tensor( Y_train.values, dtype=torch.float32 ).unsqueeze(1)
Y_test = torch.tensor( Y_test.values, dtype=torch.float32 ).unsqueeze(1)


# 2) 신경망DNN 레이어 컨테이너 설정
import torch.nn as nn
model = nn.Sequential(      # 활성함수 : 렐루 -> 음수 싹다 0으로 만듬 , 드롭아웃-> 학습 뉴런을 무작위로 꺼서 과적합을 막는 규제 기법
    nn.Linear( 4 , 32) , 
    nn.ReLU() , nn.Dropout( p=0.2 ),    # 매 순전파 마다 은닉층에  20% 무작위 비활성화 # 과적합 방지
    
    nn.Linear( 32, 16) ,
    nn.ReLU() , nn.Dropout( p=0.2 ),    # 매 순전파 마다 은닉층에  20% 무작위 비활성화 # 과적합 방지
                            
    nn.Linear( 16, 8 ) ,  # 앞전 레이어 16노드수 따라 다음 노드수 설정
    nn.ReLU(),nn.Dropout( p=0.2 ),
                            
    nn.Linear( 8 , 1 )  # 출력층 이므로 1노드로 끝낸다.
)


# 3) 손실함수: MSELoss()
crierion = nn.MSELoss()

# 4) 옵티마이저 ; optimizer = optim.AdamW( model.parameters(), lr=학습률)
import torch.optim as optim       # 파라미터 ( 가중치 / 편향 , y (예측값) = w(가중치)a(값) + b(편향) ) 
optimizer = optim.AdamW( model.parameters(), lr=0.01 )

# 5) 에포크(학습수) 단위 학습( 순전파 -> 오차계산 -> 역전파 -> 업데이트 )
for epoch in range( 10000 ) : 
  model.train()     # 1. 학습모드 실행 , 필수 **
  optimizer.zero_grad()     # 2. 이전 학습에 사용된 기울기 0으로 초기화 
  logits = model(X_train )  # 3. 순전파/ 학습
  loss = crierion( logits , Y_train )   # 손실계산  #( 예측값 , 정답지 )
  loss.backward( )    # 5. 역전파 : 오차 이용하여 가중치와 편향의 기울기 미분 계산 
  optimizer.step()    # 6. 업데이트 / 변경된 파라미터 ( 가중치 / 편향 )

  # ======================================================================== 
  if epoch % 100 == 0  : 
    print( epoch , " : loss : " , loss.item() )


# 6) 모델 평가. model.train()학습모드 , model.eval() 평가/추론모드
model.eval()
with torch.no_grad()  : 
  train_pred = model( X_train )
  test_pred = model ( X_test )
from sklearn.metrics import r2_score
print( r2_score( Y_train.numpy() , train_pred.numpy() ))
print( r2_score( Y_test.numpy() , test_pred.numpy() ))
# 7) 모델 추론
new_students = [ [4, 0, 16, 17] , [1, 10, 7, 5 ] ]
new_train = torch.tensor(ss.transform( new_students ) , dtype = torch.float32)

with torch.no_grad() :
  new_pred = model(new_train)
print( new_pred[0].item() )   # 첫번째 학생의 G3 점수 예측 16.504066467285156
print( new_pred[1].item() )   # 두번째 학생의 G3 점수 예측 6.330953598022461
