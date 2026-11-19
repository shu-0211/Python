import pandas as pd
url = "https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt"
df = pd.read_table(url, names=['rating', 'review'])     # raing : 평점 , review : 리뷰
df = df[df['rating'] != 3]
df['label'] = (df['rating'] >= 4).astype(int)
# 전체 데이터 셋에서 특정 n개 샘플링
df_sample = df.sample(n=5000, random_state=42).reset_index(drop=True)
print( df_sample.shape )

# 1) 텍스트에서 전처리 = 정규표현식 자주 사용됨. vs 리엑트/JS 입력 유효성 검사 
import re               # 정규표현식 함수
cleaned_list = [ ]       # 정규표현식 통과한 목록
for text in df_sample['review'] : # 리뷰 들을 반복
    # re.sub(r'[표현식]')
    text = re.sub(r'[가-힣a-zA-Z0-9]', ' ' ,str(text))
    # .join ( 리스트 ) : 각 리스트 항목 사이에 특정 문자 연결 
    # .split() : 하나의 문자열 내 특정 문자로 분리하여 리스트 반환
    cleaned_text = ' '.join( text.split( ) )    # '대한 민국' -> 대한 민국
    cleaned_list.append( cleaned_text)

df_sample['cleaned_review'] = cleaned_list
print( df_sample.head(3) )


# 2) 한국어 형태소 분석기 , kiwi
# 설치 : pip install kiwipiepy
from kiwipiepy import Kiwi
kiwi = Kiwi()       # 한국어 형태소 분석기 객체 생성

for word in ['가성비' , '내돈내산' , '로켓배송'] :      # 3. 사전 학습에 없는 단어 추가 
    # kiwi.add_user_word( '새로운단어' , '품사키워드')
    kiwi.add_user_word( word , 'NNG')

# 4. 불용어 : 핵심 의미가 없는 형태소를 1차적으로 걸러내기 위해
from kiwipiepy.utils import Stopwords
kiwi_stopwords = Stopwords()
custom_stopwords = { '그냥' , '그저' , '모른다' }

# 5. kiwi 이용한 형태소 분석 함수 
def tokenize_kiwi ( text ) :
    # kiwi.tokenize( 분석할 문장 , stopwords=불용어 객체)
    tokens = kiwi.tokenize(text , stopwords=kiwi_stopwords)

    # 추출할 품사 키워드 , NNG 일반명사   / 일반명사 NNG, 고유명사 NNP, 동사 VV, 형용사 VA, 일반부사 MAG
    target_tags = { 'NNG' , 'NNP' , 'VV' , 'VA' , 'MAG' }
    result = []
    for t in tokens :       # 물영어 객체객체
        # t.tag : 품사 , t.from 형재 소문자열 반환
        if t.tag in target_tags and t.form not in custom_stopwords  :      # 내가 원하는 품사에 포함된 단어이면 
            if len(t.form) >1 or t.form in {'못' , '잘'}  :                 # 일부 제외한 한단어
                # 동사와 형용사 어간 뒤에 다 붙어있다. 좋고 좋아서 좋네요 -> 좋다
                word = t.form + '다' if t.tag in { 'VV' , 'VA'} else t.forms
                result.append(word)