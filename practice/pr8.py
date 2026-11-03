# Practice8: API 데이터 수집
# 1. 개요 및 대상 API 정보
# API 이름: 행정안전부_착한가격업소 현황
# API URL: https://www.data.go.kr/data/3045247/fileData.do 

# 목표: httpx를 통해 공공데이터 API를 호출하고, pandas를 활용해 업소명, 주소, 가격 데이터를 구조화한 뒤 통계 분석을 수행합니다.
# 2. 상세 요구사항
# 2-1 (API 호출 및 파라미터 설정):
# 지정된 API URL에 인증키(serviceKey)를 포함하여 요청합니다.
# 임의의 100건의 데이터를 수집
# 2-2 (데이터프레임 적재):
# 응답받은 JSON 데이터 중 실제 행 목록인 data 배열을 추출하여 pandas.DataFrame으로 변환합니다.
import pandas as pd
import httpx
import matplotlib.pyplot as plt
import seaborn as sns
# 윈도우 기준 한글 폰트 설정 및 마이너스 부호 깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 시본 기본 테마 적용 (폰트 설정 유지)
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')
serviceKey = "a15d3190788aca086d3b4dd16ecd0f2e87377ca9a382cc66309f944228ad62c7"
def pratice():
    url = "https://api.odcloud.kr/api/3045247/v1/uddi:1c782e6f-9281-451d-aa04-a550074abc2d"
    url += "?page=1&perPage=100"
    url += f"&serviceKey={serviceKey}"

    response = httpx.get(url)
    # print(response)      # <Response [200 OK]> 확인 완료

    response_json = response.json()
    # print(response_json)

    # 판다스에저장
    df = pd.DataFrame( response_json['data'] )
    # print( df.info())

    # 가격 컬럼 데이터 숫자형으로 변환 
    df['가격'] = pd.to_numeric(df['가격'])
    # print(df['가격'].dtype)

    # 평균값 출력 
    print( df['가격'].mean())

    # 업종별 가격의 평균 출력
    new_df = df.groupby('업종')['가격'].mean()
    print( new_df)

    # seaborn의 barplot
    sns.barplot(data=df , x='업종' , y='가격')
    plt.show()
    # matplotlib barplot
    plt.bar( new_df.index , new_df.values )
    plt.show()


pratice()
# 2-3 (데이터 전처리 및 분석):
# 가격1 컬럼의 데이터를 숫자형(pd.to_numeric)으로 변환합니다.
# 수집된 100건 데이터 기준 가격1의 평균값을 산출하여 출력합니다.

# 2-4 (업종별 평균 가격 집계 및 시각화):
# groupby('업종')을 사용하여 업종별 가격1의 평균 가격을 계산합니다.
# seaborn의 barplot 및 matplotlib을 활용하여 업종별 평균 가격 비교 막대그래프를 시각화합니다.