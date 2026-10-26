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

# 예2]

# 예3]
try:
    int(input_a)
except : 
    pass

# 예] 
try:                            # 예외가 발생할 가능성이 있는 코드
    int(input_a)
except :                        # 예외가 발생했을때 실행코드
    print("정수가 아닙니다.")
else:                           # 예외가 발생하지 않았을 때 실행코드
    print("정수가 맞습니다.")

# 예5] finally , 예외가 발생하든 발생하지 않든 무조건 실행 코드
try : 
    int(input_a)
except:
    print("정수가 아닙니다.")
finally :   # 무조건 실행되는 코드
    print("코드 끝")

# 예 6] finally 활용예
try : 
    file = open() # open( 파일명, 옵션 )파일 불러오기 함수 # W옵션 : 파일이 없으면 생성
    예외.발생해라() # 일부러 예외 발생 !!! ****
    # try 에서 만약에 예외가 발생하면 발생한 코드 이후는 실행 x
    
    # 파일.close() : 파일 닫기 
except : 
    print("예외가 발생 했습니다.")
finally : 
    file.close()

output = 10 + "개"
print(output)

cursor.close()
list = [1,2,3,4,5][10]