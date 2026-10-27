import numpy as np
# [기본 제공 코드] CSV 파일 로드 (헤더 제외, 콤마 구분)
data = np.genfromtxt('./practice/customer_purchase_data.csv', delimiter=',', skip_header=1)
# 데이터 구조 확인: [ID, Visits, Stay_Time, Cart_Items, Purchase_Amount]
print(f"데이터 형태: {data.shape}")


# ==============================================================================  


# Python NumPy Practice2

# 1. 데이터 준비 및 구조 (Columns)
# - 샘플 데이터 다운로드 : https://drive.google.com/file/d/1SqzLBPZufZQpl-N39-9mE_zmQ_Dx_9DA/view?usp=sharing
# - 파일명 : customer_purchase_data.csv
# - 컬럼 구성 (총 5개 열, 인덱스 0 ~ 4)
# [0] ID       : 고객ID
# [1] Visits     : 방문 횟수
# [2] Stay_Time   : 평균 체류 시간(분)
# [3] Cart_Items   : 장바구니 담은 횟수
# [4] Purchase_Amount : 최종 구매 금액($)

# 2. 단계별 미션 
# [Step 1] 데이터 기초 통계 분석 (Indexing & Statistics)
# - 전체 데이터(data)에서 '구매 금액(마지막 열, 4번 열)'만 추출하여 `sales` 배열을 생성하세요.
# - 고객들의 '평균 구매 금액'과 '총 매출액(합계)'을 계산하여 출력하세요.
#
sales = data[:,[3,-1]]
print( np.max(sales[:,-1]))
print(np.average(sales[:, -1]))





# [Step 2] 충성 고객 필터링
# - 조건: '방문 횟수(1번 열)가 20회 이상' 이거나(|) '구매 금액(4번 열)이 2000달러 이상'인 고객을 '충성 고객'으로 분류하세요.
# - 위 조건에 해당하는 충성 고객들의 '고객ID(0번 열)'만 추출하여 출력하세요.
#
# [Step 3] 구매 전환율 및 효율성 계산
# - '구매 금액(4번 열) / 방문 횟수(1번 열)'를 계산하여 방문당 평균 매출인 `arpv` 배열을 생성하세요.
# - 방문당 평균 매출(`arpv`)이 가장 높은 고객의 인덱스를 찾고, 해당 고객의 '고객ID(0번 열)'를 출력하세요.
#
# [Step 4] 휴면 고객 및 이탈 위험군 식별
# - 조건: '방문 횟수(1번 열)가 3회 이하' 이면서(&) '장바구니 담은 횟수(3번 열)가 1회 이하'인 고객을 '이탈 위험 고객'으로 분류하세요.
# - 이 조건에 해당하는 고객들의 전체 데이터(행)를 추출하고, 대상 고객이 총 몇 명인지 출력하세요.
#
# [Step 5] 고객 등급 정규화 및 VVIP 선정
# - 구매 금액(`sales`) 데이터를 0과 1 사이의 값으로 정규화(Min-Max Scaling) 하세요. * 공식 : ( x - 최솟값 ) / ( 최댓값 - 최솟값 )
# - 정규화된 값이 0.9 이상(상위 10% 수준)인 고객을 'VVIP'로 정의하고, 해당 VVIP 고객들의 모든 정보(Row 전체)를 추출하여 출력하세요.
# -- 추출된 VVIP 고객 데이터를 '구매 금액(4번 열)' 기준 내림차순(높은 금액 순)으로 정렬하여 상위 5명의 정보를 출력하세요.