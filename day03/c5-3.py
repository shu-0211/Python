# p.317 
# 튜플이란? 여러 자료들을 저장하는 리스트와 비슷한 자료형
# 특징: 초기화 이후 수정 불가능 
# 사용처 : 읽기모드용(VO : value Object ) , 수정없는 자료 ( 리스트보다 성능 좋다( 메모리 효율 ))
#  
# ( 요소 , 요소 , 요소 )

# 1. 튜플선언
tuple_test = ( 10 , 20 , 30 )

# 2. 요소값 호출
print( tuple_test[0] , tuple_test[2] )

# 3. 요소값 수정 
tuple_test[0] = 40  # 튜플은 수정 불가능 

# 4. 요소 하나인 경우
tuple_test2 = (273 , )
print( tuple_test2)  # 뒤에 , 쉼표 없으면 일반값 취급

# 5. 튜플은 소괄호 생략해도 된다.
( a , b ) = ( 10 , 20 )
print( a , b)
a , b = 10 , 20
print(a,b)

# 스왑
a , b = 10 , 20
print( a , b)

# 리액트(js) 에서 비슷한 문법 존재 -> 구조분해 ( useState , props)
# name , age = { name : "유재석" , age : 10 }
# name , age = [ "유재석" , 10] 
c , d = [ 30 , 40 ]
print( c , d )

# 6. 함수 / 연산 결과는 항상 1개 
def test() : 
    return 10, 20  # 결과는 1개 ( 10과 20을 묶은 튜플 1개)
print(test())

# 7. 콜백 함수 : 함수 그 자체를 매개변수로 전달하여 전달받은 곳에서 전달받은 함수 호출
# 리액트 : onClick( 회원가입() ) [x] ---> onClick(회원가입) [0]
def call_100_items(func):
    func()
def print_hello():
    print("안녕하세요")
# call_100_items(print_hello())
call_100_items(print_hello)

#=================================================
# p.323
# java : 리스트.stream.forEach( ) , 리스트.stream.map( ) , 리스트.stream.filter()
# react : 리스트.stream.forEach( ) , 리스트.stream.map( ) , 리스트.stream.filter()
# python : for x in 리스트 , map(코드, 리스트) , filter(코드, 리스트)
# forEach 단순반복(return 없다) , map 반복+반환(return 있다) , filter 반복+(참이면)반환

#예제 
def power(item) :
    return item * item
def under_3(item) : 
    return item < 3

list_a = [1,2,3,4,5]
output_a = map(power,list_a)
print(list(output_a))
# JS map : list_a.map(power) , list_a.map( x -> return x*x)

output_b = filter(under_3,list_a)
print(list(output_b))
# js filter: list_a.filter(under_3) , list_a.filter(x -> return x < 3 )


# ==================================================================================
# p.324 람다(화살표함수)? 코드 줄이기
# lambda 매개변수 : 리턴값 PY : def 함수명() : 
# JAVA 람다 : ( ) -> { }        JAVA : public void 함수명(){}
# JS 람다 : ( ) => { }          JS : function 함수명(){}
power = lambda item : item*item
output_a = map( power , list_a )

# 인라인 람다 
output_a = map( lambda item : item*item , list_a )
# =================================================================
aaqa = int(3.7)
print(aaqa)

numbers = [ 1,2,3,4,5,6 ]
print("::".join(map(str,numbers)))

numbers = list(range(1 , 10+1 ) )
print(list(filter(lambda i : (i**2) < 50 ,numbers)))

앉힐수있는최소사람수 = 2
앉힐수있는최대사람수 = 10
전체사람의수 = 100
memo = {}

def 문제(남은사람수, 최소사람수):
    key = str([남은사람수, 최소사람수])

    # 종료조건
    if key in memo : 
        return memo[key]

    if 남은사람수 < 0 :
        return 0

    if 남은사람수 == 0 :
        return 1

    # 재귀처리
    if 남은사람수 > 10 :
        return 11 * 문제(남은사람수 -10 , 최소사람수)
    if 남은사람수 % 2 == 1 : 
        문제(남은사람수-1,최소사람수)
    
    


    # 메모화처리 
    memo[key] =1

    # 종료
    return 

