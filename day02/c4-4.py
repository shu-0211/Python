# p.251
numbers = [ 103, 52, 273 , 32 , 77 ]
print(min(numbers))
print(max(numbers))
print(sum(numbers))

# p.252 revered
number_reversed = reversed(numbers)
print(list(number_reversed))
print(next(number_reversed))

# int () , float(), str() , list() : 특정 타입으로 변환 함수

# 이터러블 : 요소들을 하나씩 차례로 꺼내기 가능한 객체 의미
# 이터레이터 : 이터러블 중에서 하나씩 차례로 빼낼 수 있는 요소
# 이터레이터 포함된 타입 : 리스트 / 딕셔너리 / 문자열 / 튜플 등
# 이터레이터 하나씩 꺼내는 함수 = next( ) 함수 ---> 이터러블 

# p.254 enumerate ( 리스트 ) , (인덱스, 값) , ( 인덱스 , 값 )  
numbers = [ 103, 52, 273 , 32, 77 ]
print( enumerate(numbers))
print(list(enumerate(numbers)))
for index, value in enumerate(numbers):   
    print(index,value)

# p. 256  items (딕셔너리) , [ (key,value), (key,value)]
dict_a = { "name" : "유재석" , "age" : 10 }
for key , value in dict_a.items() : 
    print(key,value)


# p.258 리스트 내포 , 인덱스 자리에 반복문 사용가능 
# 0부터 20까지 2씩 증가한 자료들을 리스트에 저장 
# 방법1]
array = []
for i in range(0 , 21 , 2) : 
    array.append(i)

# 방법 2] 리스트 변수 = [ 값 for 반복변수 in range() ]
array = [ i for i in range(0,21,2)]

# 활용 : 10 제외한 , 리스트 변수 = [값 for 반복변수 in range() if 조건식]
array = [ i for i in range(0,21,2) if i != 10 ]


# p.263 , .join() 
# 방법1] """ 여러줄"""
print(""" 안녕하세요1
안녕하세요2""")
# 방법2] \n 제어문자 
print( "안녕하세요1\n안녕하세요2")
#방법 3] ("문자열" "문자열" "문자열") # 튜플차이 
print( ("안녕하세요1\n" "안녕하세요2"))
#방법 4] 특정문자열.join (리스트), 리스트 요소 사이마다 특정문자열삽입
print("\n".join(["안녕하세요1" , "안녕하세요2"]))
print("-".join("유재석"))
print("-".join("대상혁"))

# ===================================================
#               문제 풀이 
# ===================================================

pets=[
    {"name": "구름"},
    {"nffame": "누름"}
]

for key in pets : 
    for key,value in key.items():
        print(key,value)

numbers = [1,2,6,8,4,3,2,1,9,5,4,9,7,2,1,3,5,4,8,9,7,2,3]
counter={}
for i in range(1,10):
    counter["{}".format(i)] = numbers.count(i)
print(counter)


counter["속성명"] = 키값

print(list(range(3,10,3)))



limit = 10000
i = 1
sum = 0
while True:
    sum += i
    i += 1
    if sum > limit :
        break
print("{}를 더할 때 {}을 넘으며 그때의 값은 {}입니다.".format(i-1,limit,sum))


list = []

max_value = 0 
a = 0 
b = 0 
for i in range( 1,101):
    j = 100 -i
    if i * j > max_value : 
        max_value = i*j
        a = i
        b = j

print("최대가 되는 경우: {} * {} = {}".format(a,b,max_value))


list = []
sum = 0 
for i in range( 1, 101 ) : 
    a = "{:b}".format(i)
    b = a.count("{}".format(0))
    if b == 1 : 
        list.append(i)

for i in list : 
    sum += i

print(sum)

