import pandas as pd
df = pd.read_csv( './train.csv')

# Python 데이터분석 Practice6: 종합예제1
# 문제1 [ 타이타닉 생존 데이터 분석]
# 출처: Kaggle - Titanic: Machine Learning from Disaster

# [2. 가설]
# 가설 1: 여성과 아동의 생존율이 남성보다 월등히 높을 것이다. (사회적 보호 )
# 가설 2: 높은 객실 등급(1등석)을 이용한 승객일수록 생존율이 높을 것이다. (경제적 지위와 안전의 상관관계)
# 가설 3: 특정 항구(사우샘프턴 등)에서 탑승한 승객은 객실 등급 분포에 따라 생존율 차이가 발생할 것이다.

# [3. 자료수집 ]
# 3-1 : https://www.kaggle.com/competitions/titanic/overview
# 3-2 : train.csv 파일 판다스로 불러오기 

# [4. 데이터 전처리]
# 수치형 결측치 보정: '나이(Age)' 컬럼의 결측치는 이상치에 강건한(Robust) 분석을 위해 중앙값(Median)으로 대체해야 한다.
# 범주형 결측치 보정: '승선 항구(Embarked)' 컬럼의 결측치는 가장 빈번하게 등장하는 최빈값(Mode)으로 대체해야 한다.

# [5. 데이터 시각화 및 분석]
# 5-1 : 생존 분포 분석: 전체 생존자와 사망자의 비중을 파악할 수 있는 막대그래프 를 생성한다.
import matplotlib.pyplot as plt
import seaborn as sns

# 윈도우 기준 한글 폰트 설정 및 마이너스 부호 깨짐 방지
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 시본 기본 테마 적용 (폰트 설정 유지)
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')


# 5-2 : 연령대별 상세 분석:나이에 따른 생존/사망 분포를 히스토그램으로 시각화한다.데이터의 흐름을 파악할 수 있도록 커널 밀도 추정 곡선(KDE)을 포함한다.
# 5-4 (성별): sns.countplot을 사용하여 성별(Sex)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-5 (객실 등급): sns.countplot을 사용하여 객실 등급(Pclass)에 따른 생존 여부(Survived)별 인원수를 시각화한다.
# 5-6 (승선 항구): sns.countplot을 사용하여 승선 항구(Embarked)에 따른 생존 여부(Survived)별 인원수를 시각화한다.




# # 문제2[ 서울시 공공자전거 대여이력 분석]
# 출처: 서울 열린데이터 광장

# [2. 가설]
# 가설 1: 출퇴근 시간대(08시, 18시 전후)의 자전거 대여량이 다른 시간대에 비해 압도적으로 높을 것이다.
# 가설 2: 특정 지하철역 인근이나 유동인구가 많은 지역의 대여소가 대여량 상위권을 차지할 것이다.
# 가설 3: 이용시간과 이용거리 사이에는 강한 양의 상관관계가 존재할 것이다.

# [3. 자료수집]
# 3-1 : https://data.seoul.go.kr/dataList/OA-15182/F/1/datasetView.do
# https://drive.google.com/file/d/1tXfjwXu5HQUyKupqWeEiNk7ZlN0Xf7xw/view
# 3-2 : 2025년 1월, 2월 대여이력 CSV 파일 로드 (encoding='cp949')

import pandas as pd
data1 = pd.read_csv('./서울특별시 공공자전거 대여이력 정보_2501.csv', encoding='cp949')
data2 = pd.read_csv('./서울특별시 공공자전거 대여이력 정보_2502.csv', encoding='cp949')

# [4. 데이터 전처리 및 병합]
# 4-1 (병합): pd.concat을 사용하여 분리된 월별 데이터를 하나로 통합하고 인덱스를 재부여한다.

# 4-2 (정제): 결측치의 문자열 표현('\N')을 None으로 치환하고, 성별 데이터를 대문자로 통일 및 결측치를 'U'로 보정한다.
df['이용시간(분)'] = df.to_numeric( df['이용시간(분)'] , erros = "coerce" ).fillna(0)

# 4-3 (형변환): 이용시간, 거리 등 주요 수치형 변수는 pd.to_numeric으로 변환하고, 날짜 데이터는 pd.to_datetime으로 객체화한다.
# 4-4 (파생변수): 대여일시에서 시간(Hour) 정보를 추출하여 '대여 시간대' 열을 새롭게 생성한다.

# [5. 데이터 시각화 및 분석]
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(font='Malgun Gothic', rc={'axes.unicode_minus': False}, style='whitegrid')


# 5-1 (성별 분포): sns.countplot을 사용하여 성별에 따른 따릉이 이용 비중을 시각화한다.
# 5-2 (시간대 분석): sns.barplot을 사용하여 24시간 중 어느 시간대에 대여가 집중되는지 분석한다.
# 5-3 (인기 대여소): value_counts().head(10)를 활용하여 가장 활발한 상위 10개 대여소를 가로 막대 그래프로 시각화한다.
# 5-4 (상관관계): sns.heatmap을 통해 이용시간, 이용거리, 시간대 등 수치 데이터 간의 밀접도를 분석한다.
