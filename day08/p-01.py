# 판다스 : 데이터 조작 및 분석( 표형태 ) 라이브러리 
# 설치 : pip install pandas
# 호출
import pandas as pd
print(pd.__version__)

# 1] 데이터프레임 : 2차원(표)
data_list = [ [ 'ant' , 25 , 'seoul'] , 
             ['bee' , 30 , 'busan'] , 
             ['cat' , 35 , 'incheon'] ] # 2차원 리스트 

x = pd.DataFrame(data_list)
print(x)

# 2] 데이터프레임2 , pd.DataFrame( 딕셔너리 ) , 키(열이름)
data_dict = { 
  'name' : ['ant','bee','cat'] , 
  'age' : [25,30,35] , 
  'city' : ['seoul','busan','incheon'] } # 딕셔너리

df = pd.DataFrame(data_dict)
print( df )

# 3] 컬럼 값 추출 , df['열이름'] , 레코드 
ages = df['age']
print(ages)  # Series(1차원)
print( type(ages))          # <class 'pandas.Series'>
print( type(ages.values))   # <class 'numpy.ndarray'>



# 4] 데이터프레임3 : 넘파이 
import numpy as np
data_np = np.array(data_list)   # 넘파이 자료
df = pd.DataFrame( data_np , columns=['name' , 'age' ,'city' ] , index=[ 'A' , 'B' , 'C' ])
print( df )


# 5] 주요 속성 
print( df.shape )       # 행/열 크기 # ( 3,3 )
print( df.columns )     # 컬럼 목록 Index(['name', 'age', 'city'], dtype='str')
print( df.index )       # 컬럼 목록 Index(['name', 'age', 'city'], dtype='str')
print( df.values )      # 값만 2차원 리스트로 추출
print( df.head(2) )     # 상위 n개만 반환
print( df.tail(2) )     # 하위 n개만 반환
df.info()               # 


# 6] 인덱싱 = df.iloc(인덱스) / (슬라이싱) 
print( df.iloc[1])
print( df.iloc[1,2] )
print( df.loc['B'] )    # 1행 = B행
print( df.loc['B' , 'city'] )   # B행 city열 #busan


# 7] 슬라이싱 , [시작인덱스:끝인덱스] , [행슬라이싱,열슬라이싱]
print( df.iloc[0:2 , 0: 1])
print( df.loc[ 'A' : 'C' , 'name' : 'age' ])


# 8] 열 추가 , df[새로운열] = 새로운 값
df['score'] = [ 100, 80 , 95 ]
print(df)  


# 9] 값 수정 , df[수정할열] = 새로운값
df[ 'age' ] = [ 31, 52, 40 ]
print(df) 
df.loc['B' , 'age' ] = 70 # B행 age열
print(df) 
df.iloc[0,0] = 'apple'
print(df)


# 10] 여러개 수정
df.loc[ ['A','B'] , 'score'] = [ 50 , 60 ]
print(df)


# 11] 필터링(조건)
# print(df[''])
print(df[ df['score'] > 70 ])

cont = df['age'] >= 40
print(df[ (df['score'] > 70) & cont ] )
print(df[ (df['score'] > 70) | cont ] )

# 필터링 이용하여 새로운 열 **
df['passed'] = False
df.loc[ df['score'] > 70 , 'passed' ] = True
print(df) 


# 12] 컬럼명 변경 , df.rename( columns= { '기존컬럼명' : '새로운컬럼명' } ) 
df = df.rename( columns= { 'city' : '도시' , 'age' : '나이' } ) 
df.info()


# 13] 집계 
print( df.describe() )
print( df['나이'].sum())
print( df['passed'].value_counts()) # 자료 빈도 수

# 14] 합치기/병합
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Score': [90, 80, 85]})
print(df1)
df2 = pd.DataFrame({'ID': [4, 5, 6], 'Score': [75, 95, 88]})
print(df2)

# 세로 연결 axios
new_df = pd.concat( [df1 , df2 ] , axis = 0 , ignore_index=True )
print( new_df )

new_df = pd.concat( [df1 , df2 ] , axis = 1 , ignore_index=True )
print(new_df)

# 병합 : 교집합(공통 컬럼) ,
df_info = pd.DataFrame({'ID': [1, 2, 3], 'Name': ['Ant', 'Bee', 'Cat']})
df_score = pd.DataFrame({'ID': [2, 3, 4], 'Score': [88, 92, 85]})
new_df = pd.merge(df_info ,df_score , on='ID' , how='inner')
print(df)
new_df = pd.merge(df_info ,df_score , on='ID' , how='outer')
print(df)       # NaN : 정의가 없는 자료 # 숫자가 아니다. 


# 정렬   df.sort_values( by='컬럼명' , ascending = True(기본값)오름차순 / False 내림차순 )
df = pd.DataFrame({
  'name': ['Ant', 'Bee', 'Cat', 'Dog' ,'Cow'],
  'age': [27, 27, 22, 32 , 22],
  'score': [88, 95, 85, 90 , 90] 
})

new_df = df.sort_values( by='age' , ascending = False )
print(new_df)

# 다중정렬은 [ ] 리스트 사용, * age 기준으로 1차 정렬후 동일한 age끼리 score 기준으로 2차 정렬
new_df = df.sort_values( by = ['age' , 'score' ] , ascending = [True,True])
print( new_df )

# 컬럼명도 정렬이 가능하다. 
new_df = df.sort_index( axis = 1 , ascending = True)
print( new_df )