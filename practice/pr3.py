import pandas as pd
# Python Pandas Practice3
# # 문제 1: 딕셔너리를 활용한 데이터프레임 생성 및 속성 확인
# 아래 딕셔너리(도서관 재고 데이터)를 활용하여 DataFrame을 생성한 뒤,
# 데이터프레임의 행/열 크기(shape), 인덱스 목록(index), 컬럼 목록(columns) 및 요약 정보(info)를 출력하시오.
data_dict = {
    'BookTitle': ['Python Basic', 'Data Analysis', 'AI Agent'],
    'Stock': [15, 8, 23],
    'Location': ['Floor_1', 'Floor_2', 'Floor_1']
}
x = pd.DataFrame(data_dict)
print(x.shape)  
print( x.index )
print( x.columns)
print( x.info())

# 문제 2: loc와 iloc를 이용한 인덱싱 및 슬라이싱
# 아래 데이터프레임에서 loc를 사용하여 'C2'부터 'C3' 행까지의 'Menu'와 'Price' 열을 슬라이싱하여 추출하고,
# 동시에 iloc을 사용하여 1행 2열 위치의 카테고리('Bakery') 값을 추출하여 출력하시오.
df = pd.DataFrame({
    'Menu': ['Americano', 'Croissant', 'Latte', 'Cake'],
    'Price': [4500, 3800, 5000, 6500],
    'Category': ['Coffee', 'Bakery', 'Coffee', 'Dessert']
}, index=['C1', 'C2', 'C3', 'C4'])

print( df.loc[ 'C2' : 'C3' , 'Menu' : 'Price' ])
print( df.iloc[1,2] )



# 문제 3: 다중 조건 행 필터링 
# 아래 온라인 쇼핑몰 상품 데이터에서 평점('Rating')이 4.0 이상이면서 동시에
# 리뷰 수('ReviewCount')가 100회 이상인 상품들만 비트 연산자(&)를 사용하여 필터링하고 출력하시오.
df = pd.DataFrame({
    'Product': ['Keyboard', 'Mouse', 'Headset', 'Webcam'],
    'Rating': [4.5, 3.8, 4.2, 4.8],
    'ReviewCount': [150, 80, 210, 45]
}, index=['P1', 'P2', 'P3', 'P4'])

print( df[(df['Rating'] >= 4.0 ) & (df['ReviewCount'] >= 100)] )

# 문제 4: 다중 조건 행 필터링 
# 아래 도서 대여 데이터에서 대여 횟수('RentCount')가 20회 이상이거나 또는
# 반납 지연 일수('OverdueDays')가 5일 이상인 도서 데이터를 비트 연산자(|)를 사용하여 필터링하고 출력하시오.
df = pd.DataFrame({
    'Title': ['Book_A', 'Book_B', 'Book_C', 'Book_D'],
    'RentCount': [12, 22, 15, 25],
    'OverdueDays': [7, 2, 0, 6]
}, index=['B1', 'B2', 'B3', 'B4'])

print( df[(df['RentCount'] >= 20) | (df['OverdueDays'] >= 5)])

# 문제 5: 필터링 기준 기존 컬럼 값 수정 
# 아래 학생 평가 데이터에서 'FinalScore'가 90점 이상인 학생의 'Grade'를
# loc 조건식을 사용하여 'A+'로 일괄 수정하고 전체 데이터프레임을 출력하시오.
df = pd.DataFrame({
    'Student': ['Alice', 'Bob', 'Charlie', 'David'],
    'FinalScore': [78, 94, 88, 91],
    'Grade': ['B', 'A', 'B', 'A']
}, index=['S1', 'S2', 'S3', 'S4'])
print( df )
df.loc[df['FinalScore'] >= 90 , 'Grade'] = 'A+'
print( df )

# 문제 6: 필터링 기준 기존 컬럼 값 수정 
# 아래 매장 재고 데이터에서 재고 수량('Stock')이 10개 미만인 상품의 'Status' 컬럼 값을
# loc 조건식을 사용하여 기존 'Normal'에서 'Restock_Needed'로 일괄 변경하고 전체 결과를 출력하시오.
df = pd.DataFrame({
    'Item': ['Pen', 'Notebook', 'Eraser', 'Ruler'],
    'Stock': [25, 6, 40, 8],
    'Status': ['Normal', 'Normal', 'Normal', 'Normal']
}, index=['T1', 'T2', 'T3', 'T4'])
print(df)
df.loc[df['Stock'] < 10 , 'Status'] = 'Restock_Needed'
print(df)


# 문제 7: 필터링 기준 파생 컬럼 값 수정 
# 아래 회원 실적 데이터에 기본값이 'General'인 'Membership' 컬럼을 추가한 뒤,
# 'TotalSpent'가 300,000원 이상인 회원의 'Membership' 값을 loc 조건식을 사용하여 'VIP'로 변경하여 출력하시오.
df = pd.DataFrame({
    'Member': ['Kim', 'Lee', 'Park', 'Choi'],
    'TotalSpent': [150000, 320000, 450000, 210000]
}, index=['M1', 'M2', 'M3', 'M4'])
print( df )
df['Membership'] = 'General'
print( df )
df.loc[df['TotalSpent'] >= 300000 , 'Membership'] = 'VIP'
print( df )


# 문제 8: 컬럼명 변경 및 통계 집계
# 아래 매장 판매 데이터의 컬럼명 'Units'를 '판매수량'으로, 'Discount'를 '할인율'로 rename을 사용해 변경한 뒤,
# 변경된 '판매수량'의 총합(sum)과 'Grade' 컬럼의 고윳값별 빈도수(value_counts)를 각각 출력하시오.
df = pd.DataFrame({
    'Item': ['Pen', 'Notebook', 'Eraser', 'Ruler'],
    'Units': [120, 45, 80, 30],
    'Discount': [0.1, 0.05, 0.2, 0.0],
    'Grade': ['A', 'B', 'B', 'A']
})
print(df)
df = df.rename( columns = {'Units' : '판매수량' , 'Discount' : '할인율' })
print(df)
print(df['판매수량'].sum())
print( df['Grade'].value_counts())

# 문제 9: 데이터 연결 (Concat)
# 상반기 지점 실적(df_first)과 하반기 지점 실적(df_second)을 세로(행 방향, axis=0)로 연결하되,
# 기존 인덱스를 무시하고 새롭게 0부터 번호를 매기는 방식(ignore_index=True)으로 연결하여 출력하시오.
df_first = pd.DataFrame({'Code': ['S10', 'S20'], 'Revenue': [500, 750]})
df_second = pd.DataFrame({'Code': ['S30', 'S40'], 'Revenue': [620, 890]})

df = pd.concat([df_first,df_second],axis=0,ignore_index=True)
print(df)


# 문제 10: 데이터 병합 (Merge)
# 회원 기본 프로필(df_user)과 최근 주문 내역(df_order)을 'UID' 기준으로 병합하되,
# 양쪽 모두에 존재하는 주문 회원만 결합하는 방식(inner)과 전체 회원을 모두 유지하는 방식(outer)을
# 각각 수행하여 결측치(NaN) 포함 여부를 비교 출력하시오.
df_user = pd.DataFrame({'UID': [101, 102, 103], 'User': ['James', 'Emma', 'Lucas']})
df_order = pd.DataFrame({'UID': [102, 103, 104], 'Amount': [15000, 32000, 21000]})


df = pd.merge(df_user,df_order , on='UID' ,how='inner')
print(df)
print()
df = pd.merge(df_user,df_order , on='UID' ,how='outer')
print(df)