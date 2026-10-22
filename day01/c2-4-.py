# p.135 , "문자열".format()
string_a = "age:{}".format(10)
print(string_a)
string_b = "{} {} {}".format(1,"안녕",True)
print(string_b)
# 주의할점 : {}개수와 값의 개수는 일치해야한다.

# p.137 ~ p.140 생략
# p.141, 대소문자 변환
a = "Hello"
print(a.upper()) # HELLO
print(a.lower()) # hello

# p.142, 양쪽 여백/공백 제거 // 크롤링, 전처리 에서 많이 씀
a = " hello python  "
print(a.strip())

# p.143 , isxxx 구성 확인 , 반환타입 : True/False
print("HELLO".isalpha())
print("HELLO".isdigit())

# p.144 , find() vs indexOf()
output_a = "안녕안녕하세요".find("안녕")
print(output_a)
print(output_a)     # 0 : 인덱스 
output_b = "안녕안녕하세요".rfind("안녕")
print(output_b)     # 2 : 오른쪽 부터 찾음
output_c = "안녕안녕하세요".find("hello")
print(output_c)      # -1 없다.

# p.145 , 찾을값 in "문자열" , 없으면 False 있으면 True
print( "안녕" in "안녕하세요") # True
print( "hello" in "안녕하세요") # False

a = "10 20 30 40 50".split(" ")
print(a)
print(a[1])

# p.146 , f-문자열
num = 10
a1 = "age:{}".format(num+1)    # 숫자 10
a2 = f"age:{num +1}"            # 숫자 10
a3 = "age:num+1"               # 문자열 10 
print(type(a1))