# Python Pandas Practice4
# 1. 데이터 준비 및 구조 (Columns) 
# 링크: https://drive.google.com/file/d/1X22ll4NXhnCJp0tTYYqdRyCiS7VUAvUX/view?usp=sharing (다운로드)
# - 파일명 : ecommerce_orders_cs_data.csv (인코딩: utf-8-sig)
# - 컬럼 구성 (총 8개 열)
#   [0] Order_ID    : 주문 고유번호 (문자열, 중복 데이터 포함)
#   [1] Customer_ID : 고객 식별자 (정수형 -> 문자열 변환 필요)
#   [2] Order_Date  : 주문 일자 (YYYY-MM-DD 형식의 문자열)
#   [3] Category    : 상품 카테고리 (빈 문자열 '' 및 스페이스 공백 '   ' 결측치 포함)
#   [4] Price       : 개당 가격 (원, 결측치 NaN 포함)
#   [5] Quantity    : 주문 수량 (음수 및 999 등 비정상 이상치 포함)
#   [6] Payment     : 결제 수단 (신용카드, 간편결제, 계좌이체)
#   [7] Status      : 주문 상태 ('배송완료', '반품요청', '취소')

import pandas as pd

# [기본 제공 코드] CSV 파일 로드 및 구조 확인
df = pd.read_csv('./practice/ecommerce_orders_cs_data.csv', encoding='utf-8-sig')

print("--- [데이터 기본 구조 확인] ---")
print(df.info())
print("\n--- [상위 5건 데이터] ---")
print(df.head())


# 2. 단계별 미션
# [Step 1] 데이터 무결성 검증 및 기본 정제
# - 중복된 주문 행을 제거하고, 연속된 번호로 인덱스를 재정렬(reset_index)하세요.
df = df.drop_duplicates().reset_index( drop=True )
print(df.info())
# - 산술 연산 대상이 아닌 'Customer_ID' 컬럼의 타입을 문자열(str)로 변환하세요.
df['Customer_ID'] = df['Customer_ID'].astype(str)
print(df.info())



# [Step 2] 텍스트 공백 정제 및 결측치 대체
# - 'Category' 컬럼의 빈 문자열('')과 스페이스 공백('   ')을 결측치(None)로 일괄 치환하세요.
# - 다음 기준에 따라 결측치를 대체하세요.
print(df['Category'])
df['Category'] = df['Category'].str.strip().replace("",None)
print()
print(df['Category'])
#   * 'Category' 컬럼 : 가장 빈도가 높은 '최빈값(mode)'으로 대체
df['Category'] = df['Category'].fillna(df['Category'].mode()[0])
#   * 'Price' 컬럼    : 이상치 영향을 최소화하기 위해 '중앙값(median)'으로 대체
df['Price'] = df['Price'].fillna(df['Price'].median())

# [Step 3] 이상치 보정 
# - 주문 수량('Quantity') 컬럼에 포함된 비정상 데이터(-1, 999 등)를 정상 유효 범위인 1개 이상 10개 이하로 경계 조정(clip)하세요.
df['Quantity'] = df['Quantity'].clip( lower = 1 , upper=10)


# [Step 4] 비즈니스 파생변수 생성
# - 'Price'와 'Quantity'를 곱하여 총 주문 금액인 'Total_Amount' 파생 컬럼을 생성하세요.
df['Total_Amount'] = df['Price'] * df['Quantity']
print( df.info())
# - 'Order_Date'를 날짜형(datetime)으로 변환한 뒤, 연도('Order_Year')와 월('Order_Month') 파생 컬럼을 각각 추출하세요.
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
print(df.info())
df['Order_Year'] = df['Order_Date'].dt.year
print(df.info())
df['Order_Month'] = df['Order_Date'].dt.month
print(df.info())
# - `mask` 메서드를 활용하여 'Total_Amount'가 300,000원 이상인 주문 건을 'VIP', 나머지를 'Normal'로 분류하는 'VIP_Flag' 파생 컬럼을 생성하세요.
df['VIP_Flag'] = 'Normal'
print(df['VIP_Flag'])
df['VIP_Flag'] = df['VIP_Flag'].mask(df['Total_Amount'] >= 3000000 , 'VIP')
print(df['VIP_Flag'])

# [Step 5] 집계 및 정렬 
# - 카테고리('Category')별로 그룹화하여 다음 4가지 지표를 한 번에 다중 집계(agg)하세요.
#   * 주문건수 : 'Order_ID'의 개수(count)
#   * 총매출   : 'Total_Amount'의 합계(sum)
#   * 평균단가 : 'Price'의 평균(mean)
# - 집계된 결과 테이블을 '총매출' 기준 내림차순(ascending=False)으로 정렬하여 출력하세요.
new_df = df.groupby('Category').agg(
    주문건수 = ('Order_ID', 'count'),
    총매출 = ('Total_Amount' , 'sum'),
    평균단가 = ('Price' , 'mean')
    )
new_df = new_df.sort_values(by='총매출' , ascending = False)
print(new_df.info())
print( new_df )

# [Step 6] One-Hot Encoding
# - 머신러닝 모델 입력을 위해 명목형 범주 변수인 'Payment'와 'VIP_Flag'를 원-핫 인코딩(get_dummies)하세요.
# - 단, 결과값이 True/False가 아닌 1과 0의 정수형(dtype=int)으로 생성되도록 옵션을 지정하세요.
new_df = pd.get_dummies( df , columns=['Payment', 'VIP_Flag' ],dtype=int)
print(new_df)
# ==============================================================================