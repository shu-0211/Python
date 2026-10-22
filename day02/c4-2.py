# p.217딕셔너리 
# 딕셔너리란 { } 선언하고 키 : 값 형태로 쉼표로 연결
# { key:value , key:value , key:value }
# key 중복 x / value 중복 o
# js:JSON , JAVA : MAP/DTO , DB : RECORD

# 1. 선언 
dict_a = { 
    "name": "어벤저스 엔드게임",
    "type": "히어로 무비" }

# 2. 값 호출 , 딕셔너리명['key']
print(dict_a["name"])
print(dict_a["type"])

# 3. 속성 값 추가 , 딕셔너리명 [ '새로운 키' ] = 새로운 값
dict_a['price'] = 5000
print(dict_a)

# 4. 속성값 수정
dict_a['type'] = '호러 무비'
print(dict_a)

# 5. 속성 삭제 , del 딕셔너리 [ 'key' ]
del dict_a['price']
print(dict_a)

# 6. 딕셔너리 내부 'key'확인 , 찾을키 in 딕셔너리명 
print('price' in dict_a)
print('name' in dict_a)

# 7. 속성값 호출 , 방법1: 딕셔너리명['key'] , 방법2: 딕셔너리명.get(key)
# 차이점 : 방법1은 존재하지 않으면 예외발생, 방법2는 존재하지 않으면 None반환
print(dict_a.get('name'))
print(dict_a.get('price'))
print(dict_a['price'])


# 8. for 반복문과 딕셔너리 , 
dictionary = { 
    "name": "7D 건조 망고",
    "type": "당절임",
    "ingredient": ["망고", "설탕","메타중아황산나트륨", "치자황색소"],
    "origin": "필리핀"
}
for key in dictionary :
    print(key , ":" , dictionary[key])


numbers = [1,2,3,4,5,6,7,8,9]
output = [[], [], []]

for number in numbers:
    output[((number % 3) + 2) % 3].append(number)

print(output)