# 85p.
print( type("안녕하세요") )     #<class 'str'>
print( type (123)) # <class 'int'>
print ( type (1.23)) # <class 'float'>
print ( type (True)) # <class 'bool'>
print ( type(None)) # <class 'NoneType'>
print(type([]))  # <class 'list'>
print(type({}))  # <class 'dict'>
print(type(()))  # <class 'tuple'>


# 86p. 문자열 만들기 
print("ABC") # 큰 따옴표로 감싸기 
print('ABC') # 작은 따옴표로 감싸기 
print( """ A
    B
C""" )

print("A'b'c")
print('a"b"c')
print("\"a\'b\nc\td\\e")

# 93p. 문자열 연산
# 1. + 연결연산자
print( "안녕" + "하세요")
# print("안녕" + 1) #주의할점 : 문자열과 숫자 연결 불가능 
print("안녕" * 3)

# 인덱싱 , 문자열은 배열/리스트 이므로 인덱스 존재한다.
# 인덱스란? 0부터 요소들이 저장된 순서, ** 음수도 가능 **
print("안녕하세요"[0])  # 안
print('안녕하세요'[2])  #하
# print("안녕하세요"[5]) # 오류
print("안녕하세요"[-3])
# print("안녕하세요"[-6])  # 오류


# 4. 슬라이싱 , 문자열 자르기 / 일부 추출 , [ 시작인덱스 : 끝 인덱스 -1]
print("안녕하세요"[0:2]) # 안녕
print("안녕하세요"[1:3]) # 녕하
print("안녕하세요"[2:4] ) #세요

# 시작인덱스 : 끝인덱스 , 끝 인덱스 새략시 마지막 인덱스
print("안녕하세요"[1:])
print("안녕하세요" [ :3 ])

#5. 문자열의 길이 , len (문자열)
print(len("안녕하세요"))