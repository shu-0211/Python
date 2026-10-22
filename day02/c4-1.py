# p.192
# 리스트란 ? 대괄호[] 에 자료를 쉼표로 구분하여 여러 자료들을 저장
# [요소, 요소, 요소] , 요소=element
# 인덱스란? 리스트내 요소들이 저장된 순서번호 , 0번 시작~


#
list_a = [ 273, 32, 103, "문자열" , True , False ]
print( list_a[2] )  #인덱스
print(list_a[1:3])  # 1~2 # [32,103]
list_a[2] = 7 # 요소 값 수정/변경
print(list_a[2])
print( list_a[-2] )
list_a[-2] = -8
print(list_a[-2])
print(list_a[1][1])
print(list_a[7])
list_1 = [ 1,2,3,4,5] # 1차원 리스트
list_2 = [ 1,[2,3,4],5] # 2차원리스트


# p.196
list_a = [ 1,2,3 ]
list_b = [ 4, 5, 6]
print(list_a + list_b)
print(len(list_a))
list_aa = [ [1] , [2] , [3] ]
print(list_a + list_aa)

list_a.append(4)
print(list_a)

list_a.insert( 0 , 5 )
print(list_a)

list_c = [1,2]
list_c + [3]
print(list_c)


# p.202 요소 삭제하기        del  쓰거나 .pop함수를 사용해서 요소 삭제 
list_a = [1,2,3,4,5]
del list_a[1]
print(list_a)
list_a.pop(2) # 2번인덱스 삭제

del list_a[0:2]     # del 키워드를 이용한 슬라이싱 삭제
print( list_a )     # [5]

list_a.remove(5) # 5를 값으로 가지는 요소 삭제
print( list_a )

# 리스트명.clear() 요소 삭제 
list_a.clear() # 전체 삭제

# p.204 슬라이싱, [ 시작인덱스 : 끝인덱스 : 단계 ]
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
print(numbers[0:5:2])
print(numbers[::-1])

# p.205 정렬 , 리스트명.sort() , 리스트명.sort() , 리스트명.sort(reverse = True)
list_e = [ 52, 273 , 103, 32 , 275 , 1, 7]
list_e.sort ()
print(list_e)
list_e.sort(reverse=True)
print(list_e)

# p.206 내부 확인 , 찾을 값 in 리스트
print( 52 in list_e)
print( 51 in list_e)
print( 52 not in list_e)
print( 51 not in list_e)

# p.208 리스트와 반복문 , 리스트내 요소들이 순차적인 인덱스 구조 
for element in list_e :
    print(element)
for char in "안녕하세요" : 
    print(char)
print('안')
print('녕')

i = 1
for i in range(1,10) :
    for j in range(1,10) :
        print(i ,"*",j,"=",i*j )