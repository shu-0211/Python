# 맷플롯립 :
# 개발자 : 코딩 , 분석가 : 차트해석능력
#설치 : pip install matplotlib
# 확인 
import matplotlib
print( matplotlib.__version__)

# 매슬롯립 그래프는 한글 포트 지원 안한다. 
# ######### 한글 폰트 설정 ##########
import matplotlib.pyplot as plt
plt.rc( 'font' , family='Malgun Gothic')
plt.rcParams['axes.unicode_minus']  = False

# 1] 선 차트
epochs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
train_loss = [0.9, 0.7, 0.55, 0.45, 0.38, 0.32, 0.28, 0.25, 0.23, 0.20]
val_loss = [0.95, 0.75, 0.60, 0.52, 0.48, 0.45, 0.44, 0.43, 0.44, 0.45]

# 1)plt.figure(figsize=(가로inch , 세로inlh)) 
plt.figure(figsize=(7 , 4))

# 2) 선 차트 : plt.plot( )plt.plot(x축값, y축값, label = "계열명" , coler="색상명" , linestyle = "선종류" , marker ="점모양" )
# plt.plot( epochs , train_loss , label = "Train Loss" , color ="blue" , linestyle = "-" ,marker = "o")
# plt.plot( epochs , val_loss , label="값 손실" , color ="red" , linestyle="--", marker ="s")

# plt.title("학습별 모델 손실 추세") # 3) 차트의 제목
# plt.xlabel("학습수")                # 4) x축 제목
# plt.ylabel("손실")                  # 5) y축 제목
# plt.grid(True)                      # 6) 구분선
# plt.legend()                        # 7) 범례 표시

# ===========================================================================
# # 2] 막대 차트(비교) plt.bar , 선 차트(추세)  plt.plot
# classes = ['Cat', 'Dog', 'Bird', 'Fish']
# counts = [120, 150, 80, 45]
# # 1) plt.bar( x값, y값, color = [색상] , width = 막대 크기 )
# bars = plt.bar( classes , counts, width = 0.5 , color = ['#222222' , '#444444' , '#666666' , '#888888'])

# # 2) 막대 값 레이블 , plt.bar_label( 막대 차트 변수 , padding = 막대와 레이블 간격 , fontsize = 폰트크기)
# plt.bar_label( bars , padding= 3, fontsize = 8)
# plt.title( '클래스별 샘플 수 ')
# plt.xlabel("클래스")
# plt.ylabel("샘플 수")
# plt.grid( True , alpha = 0.5 )      # alpha = "투명도"



# ============================================================================
# # 3] 산점도 ( 상관관계 )
# x = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]
# y = [2.3, 3.8, 5.1, 7.0, 7.8, 9.2, 10.5]

# # 1) 산점도 plt.scatter(x축값, y축값 , color ="색상" , s = 점크기 , alpha = 투명도)
# plt.scatter( x , y , color = "purple" , s = 50 , alpha = 0.5 )
# plt.title("공부시간과 시험점수의 상관관계") 
# plt.xlabel("공부시간") 
# plt.ylabel("시험점수")


# ==============================================================================
# # 4] 히스토그램 ( 연속형 수치/값 분포 )
# import numpy as np
# # 평균 170을 중심으로 표준편차 5만큼 퍼져 있는 종모양 ( 가우시안분포 )
# heights = np.random.normal(loc=170 , scale= 5 , size= 1000)
# # 1) 히스토그램  plt.hist( 값 , bins="구간 수" , color = "색상" , alpha = "투명도")
# plt.hist( heights , bins = 30 , edgecolor = "black" )

# plt.xlabel("키(cm)")
# plt.ylabel("빈도/분포수")


# ==========================================================================================
# # 5] 박스플롯( 분포 범위내 이상치 )
# import numpy as np
# heights = np.random.normal(loc=170, scale=5, size=1000)
# data_with_outliers = np.append(heights, [210, 215, 120])

# # 1. plt.boxplot( 값 )
# plt.boxplot( data_with_outliers )


# =======================================================
# 6] 다중 그래프 / 한 차트에 2개 이상 그래프 한창 표현
# fig (공간),  axs(축) = plt.subplots( 행개수 , 열개수 , figsize = (가로 , 세로 ) )   # 1줄에 차트 2개
fig, axs = plt.subplots( 1, 2 , figsize = (10 , 4) )    # 1줄(행) 차트 2개

# 1행 1열 차트    axs[인덱스].차트종류( )
axs[0].plot( [1,2,3] , [4,5,6] )
axs[0].set_title("서브1: 선그래프")
# 1행 2열 차트
axs[1].bar(['A','B','C'] , [30, 15, 40])
axs[1].set_title("서브2 : 막대그래프")
    
# plt # 맷플롯립 별칭
plt.show()  # 차트 실행