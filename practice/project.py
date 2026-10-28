import numpy as np
# [기본 제공 코드] CSV 파일 로드 (헤더 제외, 콤마 구분)
data = np.genfromtxt('./practice/pred_food.csv', delimiter=',', skip_header=1, dtype=str, encoding='utf-8-sig')
np.set_printoptions(precision=2, floatmode='fixed')
# 데이터 구조 확인: [ID, Visits, Stay_Time, Cart_Items, Purchase_Amount]
print(f"데이터 형태: {data.shape}")

print(data[:])
# 음식이름 0행 / GI 1행 / 탄수화물 3행

# step1
print(np.mean(data[:, 3].astype(float)))
print(np.max(data[:, 3].astype(float)))

# step2
high = data[(data[:,1].astype(float) >= 70) | (data[:,3].astype(float) >=50)]


# step3
GL = data[:, 1].astype(float) * data[:, 3].astype(float) / 100
print(GL)
max_GL = np.argmax(GL)
print(max_GL)
print(data[max_GL])

# step4
temp = np.column_stack((GL, data[:, 1].astype(float)))
result = temp[ (temp[: , 0] >= 20) & (temp[: , 1] >= 70) ]
print(len(result) / len(data) * 100 , "%" , sep="")


# step5
condition = (temp[:, 0] >= 20) & (temp[:, 1] >= 70)
print(np.column_stack((data[condition, 0], temp[condition])))