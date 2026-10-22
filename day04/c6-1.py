# 구문 오류 : 실행전 오류 , 실행 자체 불가능
# 런타임 오류 : 실행 중 오류, 예외 
# 예외 처리 : 예외를 해결하는 모든것을

# 조건문 또는 try 
# 예1] 조건문 예외 
input_a = input("정수입력: ")
# int( ) 정수로 변환 함수
# int( input_a ) # ValueError:
if input_a.isdigit():
    int ( input_a )
else:
    print("정수가 아닙니다.")