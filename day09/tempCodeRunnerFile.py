plt.plot( epochs , train_loss , label = "Train Loss" , color ="blue" , linestyle = "-" ,marker = "o")
# plt.plot( epochs , val_loss , label="값 손실" , color ="red" , linestyle="--", marker ="s")

# plt.title("학습별 모델 손실 추세") # 3) 차트의 제목
# plt.xlabel("학습수")                # 4) x축 제목
# plt.ylabel("손실")                  # 5) y축 제목
# plt.grid(True)                      # 6) 구분선
# plt.legend()                        # 7) 범례 표시