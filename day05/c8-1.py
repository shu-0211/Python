# 절차지향 프로그래밍 : 데이터를 순서대로 처리하고 하향식 순차 실행 흐름 , C
# 객체지향 프로그래밍 : 객체들에 상호작용으로 프로그래밍 설계 , JAVA/PYTHON/JS
# 관점지향 프로그래밍 : 공통되는 기능(로그/검증/보안 등) 들을 분리하여 프로그래밍 설계 , Spring
# 추상화 : 핵심적인 개념 또는 기능 간추려 내는 것
# [ 리스트 ] ,{ 딕셔너리 } 객체이다. 
# 클래스 : 추상화한 데이터들을 구조화 한것(설계도)
# 객체 : 세상에 존재하는 모든 데이터들을 추상화(실체 x)
# 인스턴스 : 추상화한것을 객체 만든것(실체o)
# 인스턴스화 : 컴퓨터내 객체 정보 저장 , JAVA : NEW 생성자() , PY : 생성자 ()
# 생성자 : 클래스 기반으로 인스턴스 만드는 함수                 -> 인스턴스 초기화 함수

class Student : 
    pass
student = Student() # Java : new Student( ) , PY : Student( )
student = [
    Student(),
    Student(),
    Student(),
    Student(),
    Student(),
    Student()
]


# 2. 생성자 
# class Student : 
#     def __init__(self , 맴버변수1):
#         self.맴버변수1 = 맴버변수1
class Student2 : 
    def __init__(self , name , korean , math , english , science ):
        self.name= name
        self.korean = korean
        self.math = math
        self.engish = english
        self.science = science

    def get_sum(self):
        return self.korean + self.math +\
            self.english + self.science 

    def get_average(self):
        return self.get_sum() / 4

    def to_string(self):
        return "{} \t {} \t {}".format(self.name , self.get_sum() , self.get_average)

    # 일반함수와 메소드 차이? 일반함수는 클래스 밖에서 독립선언/ 메소드는 클래스 안에서 선언

    def __delete__(self, instance):
        print("{} - 파괴되었습니다.".format(self.name))
# 생성자 이용한 인스턴스 생성 , py : 클래스명 ( 인수 , 인수 , 인수 )
# Student2 s = new Student( "유재석" , 10 , 20 , 30 , 40 )
students = [
    Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85),
    Student2("윤인성" , 87 , 98 , 88 , 85)
]
print(students[0].korean)