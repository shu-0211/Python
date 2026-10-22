# p.293 재귀함수 재귀란 자기자신을 호출하는 것
def factorial(n): 
    ouput = 1
    for i in range( 1, n+1):
        ouput *= i

    return ouput
print("3! :" ,factorial(3))

def factorial2(n):
    if n == 0 : 
        return 1
    else : 
        return n * factorial2(n-1)
print(factorial2(6))

# 구구단 반복문 
for i in range( 2, 10 , 1):
    for j in range( 2, 10 , 1):
        print( i * j)

# 구구단 재귀 
def 구구단( 단 = 2 , 곱 = 1):
    if 단 > 9 :
        return 
    if 곱 > 9 :
        구구단(단+1 , 1) 
        return 
    print(단 * 곱)
    구구단 ( 단 , 곱+1 )
구구단(2 , 2)


# ========================================================================
dictionary = {
    1: 1,
    2: 1
}
def fibonacci(n) :

    if n in dictionary:
        return dictionary[n]
    else:
        ouput = fibonacci(n-1) + fibonacci(n-2)
        dictionary[n] = ouput
        return ouput

print(fibonacci(100))
print(dictionary)