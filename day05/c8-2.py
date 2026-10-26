# 상속이란? 어떤 클래스를 기반으로 그 속성과 기능을 물려받아 새로운 클래스 만드는 것
# isinstance( 인스턴스 , 클래스명 )
# 예1 
class Student : 
    def __init__(self):
        pass
student = Student()
class Human:
    def __init__(self):
        pass
print(isinstance(student , Student)) #true
print(isinstance(student , Human))   #false

# 예2]
class Student2 : 
    count = 0

    # p.486 클래스함수
    @classmethod #클래스 함수 정의하는 데코레이터/어노테이션
    def print(cls): # 매개변수에 cls 관례적으로 선언
        for student in cls.students :
            print(str(student))

    def __init__(self , name , korean , math , english , science ):
        self.name= name
        self.korean = korean
        self.math = math
        self.engish = english
        self.science = science
        Student2.count += 1 # 클래스변수 호출방법 : 클래스명.변수명

    def get_sum(self):
        return self.korean + self.math +\
            self.english + self.science 

    def get_average(self):
        return self.get_sum() / 4

    def to_string(self):
        return "{} \t {} \t {}".format(self.name , self.get_sum() , self.get_average)

    # 특수한 이름의 메소드 
    def __str__(self) :
        return "{} \t {} \t {}".format(self.name , self.get_sum() , self.get_average)


    def __delete__(self, instance):
        print("{} - 파괴되었습니다.".format(self.name))

    def __eq__(self, value):
        return self.get_sum() == value.get_sum()

    def __ne__(self, value):
        return self.get_sum() != value.get_sum()

    def __gt__(self, value):
        return self.get_sum() > value.get_sum()

    def __ge__(self, value):
            return self.get_sum() >= value.get_sum()
    def __lt__(self, value):
        return self.get_sum() < value.get_sum()
    def __le____(self, value):
        return self.get_sum() <= value.get_sum()

            

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


# 특수한 이름의 메소드 호출
print(str(students[0]))
print(students[0] == students[1])   # 쥬소값 다른데 #==대신에 __eq__함수가 실행된다
# 원래 객체는 다른데 , 우리가 __eq__ 메소드에서 같다 기준을 총합계로 정의하였기때문엗\
print( students[0] != students) 
# 원래객체는 다른데. 우리가 __ne__ 메소드에서 다른다 기준을 총합계 정의 했으므로 #flase

print(Student2.count)

# 클래스명.클래스함수
Student2.print()


# 파이썬은 부모클래스가 여러개 가능 
