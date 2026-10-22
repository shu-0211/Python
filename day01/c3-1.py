# 비교연산자
# 논리연산자

# p.163 , if 조건문
# if 조건식 : 
#   (tab 들여쓰기)참이면
age = 10
if age >= 19 : 
    print('성인입니다.')
else :
    print('성인이 아닙니다.')

# if ~ elif ~ elif ~
point = 85
if point >= 90 :
    print('A')
elif point >= 80 :
    print("B")
elif point >= 70 :
    print('C')
else :
    print('재시험')

# if 중첩
x = 10
if x > 5 : 
    if x > 10 :
        print("10보다 크다")
    else : 
        print("5보다 크고 10보다 작거나 같다")
else : 
    print("5보다 작다")

x=10
y=2
if x>4:
    if y>2:
        print(x*y)
else : 
    print(x+y)
