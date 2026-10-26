
# 예외 객체 란 ? 발생한 예외 정보 갖는 객체 
# 예외 클래스 : Exception ( 예외 최상위 클래스)
# except 예외 클래스명 as 변수명 : 
# as 키워드 : 클래스의 객체변수 생성
# 그외 모든 예외 처리 : 여러개 except에서 Exception은 항상 마지막에 위치
# 주의할점 : Exception 앞에 위치하면 아래 excetp 예외가 작동 안함. -> 상속개념
# raise : 강제로 예외발생 , 주로 CURD 실패 500 의미
# p.383
list_number = [ 52, 273, 32, 72, 100 ]

try : 
    number_input = int(input("정수입력"))       # 타입 예외
    print(list_number[number_input])            # 인덱스 예외
    raise NotImplementedError
except ValueError as e:                         # 타입 변환 예외 catch( Exception e){}
    print(e)
except IndexError as e:
    print(e)
except Exception as e :                         # 그외 ( 최상위 )예외 항상 마지막
    print(e)


# =============================================
# 발표 준비 