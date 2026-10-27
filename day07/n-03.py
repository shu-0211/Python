import numpy as np 
# 1] 병합 , 
x = np.array( [ [1,2] , [3,4] ] )
y = np.array( [ [5,6] , [7,8] ] )
z = np.vstack( [x,y] ) # 세로로 붙이기 
print(z)
z = np.hstack( [x,y] ) # 가로로 붙이기
print(z)

# 2] 병합2 , concatednate( (배열1, 배열2) , )
z = np.concatenate( (x,y) , axis=0 )    # axios = 0 세로방향 , axios = 1가로방향
print(z) 
z = np.concatenate( (x,y) , axis=1 )    


# 3] 정렬 , .sort(배열) : 오름차순 , [ : : -1 ]
x = np.array( [3,1,4,2,5] )
print( np.sort( x ) )
print( np.sort(x)[ : : -1] )
print( x ) # 원본 변경 안됨.
x.sort() # 배열.sort
print( x ) # 원본 자체 변경됨


# 4] 값 자체를 정렬하지 않고 배열을 정렬 위치 순번 반환
scores = np.array( [75,95,60,88] )
z = np.argsort( scores ) # 오름차순 기준으로 정렬했을 때 각 위치 번호
print(z)

# 5] 필터링/조건식 , *for 사용안함(장점)  : 내부적으로는 for 사용*
x = np.array( [10,20,30,40,50] )
print( x > 30 ) # [False False False True True]
print( x[x>30]) # [40,50] / 인덱싱 안에서 조건식 사용하면 True값 추출 

y = np.array( [ [1,2,3] , [4,5,6] , [7,8,9] ] )
print( y % 2 == 0 )
print( y[y % 2 == 0])


# 6] 삼항연상자 , np.where ( 조건 , 참 , 거짓)
print( np.where( x > 30 , x, 0 ) )
print( np.where( y % 2 == 0 , 0 ,1 ) ) # 짝수이면 0 , 홀수이면 1

# 7] 다수 조건 , & | ~
a =y % 2 == 0
print( y [ (y % 2 == 0) & ( y % 4 == 0 ) ] ) # 짝수이면서 4배수
print( y[ a | (y % 4 == 0 ) ] )  # 짝수이거나 4배수
print( y [ ~a ] )               # 짝수가 아닌
# 주의할점 : C/JAVA에서 &비트(0/1)연산자 , numpy 에서는  &논리연산자
# 넘파이는 파이썬에서 실행되는 구조( 중복에 따른 오버라이딩 제한 )  bool VS bool_
# and 대신 &를 사용하는 이유는 파이썬이 and를 쓰고 사용하면 오버라이딩해야하니까
# 오버라이딩하는 대신 & 이걸 사용함. 