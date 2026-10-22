# 함수? 코드의 집합
    # 값 저장 - 변수 , 코드 저장 - 함수 
    # 값여러개 저장 = 리스트/딕셔너리/튜플
# 매개변수? 함수를 호출할 떄는 괄호 내부에 여러가지를 넣는 변수
# 리턴값? 함수를 호출해서 최종적으로 나오는 결과
# def 함수명(매개변수명) : 
# 실행문 


# 1. 기본적인 함수 
def print_3_times():
    print("안녕하세요")
    print("안녕하세요")
    print("안녕하세요")
print_3_times()

print("Hello","World")  # , sep="")
# VS 
for i in range( 0 , 3 , 1) : 
    print("안녕하세요")

# 2. 매개변수? 매개(중매 - 서로 다른곳에서 연결)    /인수/인자값 -> 매개변수
def print_n_times( value , n ) :
    for i in range(n) :
        print(value)
print_n_times( "안녕하세요" , 5 )

# p.278 가변 매개변수
# def 함수명( 매개변수 , 매개변수 , *가변매개변수)
# 조건1 : 가변매개변수가 가장 뒤로 정의한다 # 조건2 : 1번만 사용한다. 
def print_n_times2( n, *values):
    for i in range(n) : 
        for value in values : 
            print(value)
            print()
print_n_times2( 3 , "안녕하세요" , "즐거운" , "파이썬")
print_n_times2( 2 , "안녕하세요" , "즐거운")

# p.280 
# 기본 매개변수가 가변 매개변수보다 앞에 올때 , 오류
# 가변 매개변수가 기본 매개변수보다 앞에 올때 , 기본 매개변수 인자값 없다. 
print("안녕하세요") 
print("안녕하세요" , end = "\n" ) # end 매개변수는 출력 후 무엇을 할지 # \n 기본값 = 기본매개변수
print("안녕하세요" , end = "" ) # 키워드 매개변수란? 인수 대입시  매개변수명 지정
def print_n_times4(*values , n = 2 ) :
    for i in range(n) :
        for value in values : 
            print(value)
            print()
print_n_times4( "안녕하세요" , "즐거운" , "파이썬" , n=3)
print_n_times4( "안녕하세요" , "즐거운" , "파이썬" , 3)


# 리턴이란 
def myFunc(x,y):
    return x + y

z = myFunc(3,5)
def return_test() :
    print("A위치 입니다.")
    return # 리턴/함수종료/함수끝 #break 반복문탈출/종료
    print("B위치입니다.")
return_test()   # B위치 출력 안됨

# 2] 자료와 함께 리턴하기 
def return_test2() : 
    return 100
value = return_test2()
print(value)

# p.287
def sum_all(start,end):
    output = 0
    for i in range(start, end +1):
        output += i
    return output
print("0 to 100 :" , sum_all(0,100))
print("0 to 1000 :" , sum_all(0,1000))
print("50 to 100 :" , sum_all(50,100))
print("500 to 1000 :" , sum_all(500,1000))


def sum_all(start = 0 , end = 100 , step = 1):
    output = 0 
    for i in range(start, end + 1 , step) : 
        output += i
    return output

print("A." , sum_all(0,100,10))
print("B." , sum_all(end=100))
print("C." , sum_all(end=100, step= 2))
print("A." , sum_all(99,102,2))