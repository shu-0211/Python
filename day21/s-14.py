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
cleaned_list = []       # 정규표현식 통과한 목록
for text in df_sample['review'] : # 리뷰 들을 반복
    # re.sub(r'[표현식]')
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ' ,str(text))
    # .join ( 리스트 ) : 각 리스트 항목 사이에 특정 문자 연결 
    # .split() : 하나의 문자열 내 특정 문자로 분리하여 리스트 반환
    cleaned_text = ' '.join( text.split( ) )    # '대한 민국' -> 대한 민국
    cleaned_list.append( cleaned_text)

df_sample['cleaned_review'] = cleaned_list
print( df_sample.head(3) )
print( df_sample.shape )
#  (5000, 4)


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
        # t.tag : 품사 , t.form 형재 소문자열 반환
        if t.tag in target_tags and t.form not in custom_stopwords  :      # 내가 원하는 품사에 포함된 단어이면 
            if len(t.form) >1 or t.form in {'못' , '잘'}  :                 # 일부 제외한 한단어
                # 동사와 형용사 어간 뒤에 다 붙어있다. 좋고 좋아서 좋네요 -> 좋다
                word = t.form + '다' if t.tag in { 'VV' , 'VA'} else t.form
                result.append(word)
    return result

# 첫번째 리뷰만 토큰나이즈 실행
test_word = df_sample['cleaned_review'].iloc[0]
print( test_word )
print ( tokenize_kiwi( test_word ) )




#===========================
from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split(
    # x = 리뷰 , Y = 평점 
    df_sample['cleaned_review'], df_sample['label'],
    random_state=42 , test_size=0.2 ,stratify= df_sample['label'] 
)


# 7. 리뷰 --> 행렬(벡터) 변환
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(
    tokenizer=tokenize_kiwi,     # 생략시 공백/띄어쓰기 기준으로 분리 # 직접 만든함수
    token_pattern=None ,         # 실행중 발생 하는 로그 비활성화
)
X_train_tfidf = tfidf.fit_transform( X_train )  # 학습 -> 변환  # 학습용
X_test_tfidf = tfidf.transform( X_test )        # 테스트용
print( X_train_tfidf.shape )                    # (4000, 4105)
print( X_test_tfidf.shape )                     # (1000, 4105)

print( '추출한 피처 10개만 확인 ', tfidf.get_feature_names_out()[ : 10])
# 추출한 피처 10개만 확인  ['가게' '가겨' '가격' '가격대' '가관' '가구' '가까이' '가끔' '가늘다' '가능']
# (문제점) 오타 등으로 유사한 단어들을 분별 불가능해서 다른 단어로 취급,
# (해결) 유사도 거리 계산 ( 임베딩 / BERT )

# 8 긍정/부정   : 감정분석 
from sklearn.linear_model import LogisticRegression     # 실무적으로 LightGBM
model = LogisticRegression( C=1.0 , max_iter=1000 , random_state=42)
model.fit(X_train_tfidf , Y_train)      #분류 모델 학습
print( model.score( X_train_tfidf , Y_train))
print( model.score( X_test_tfidf , Y_test))
Y_pred = model.predict(X_test_tfidf )

from sklearn.metrics import f1_score
print( 'f1 : ', f1_score(Y_test , Y_pred))
# f1 :  0.8074921956295525
# 9. 예측하기
print (X_train_tfidf.toarray()[0])

new_reviews = [
    "배송도 정말 빠르고 가성비 최고입니다! 재구매 의사 있어요.",
    "마감 상태가 엉망이고 실밥이 다 터져서 왔네요. 최악입니다.",
    "그냥 가격만큼 하는 것 같아요. 특별히 좋지도 나쁘지도 않음."
]

# 정규표현식
cleaned_new = [ ] 
for text in new_reviews : 
    text = re.sub(r'[^가-힣a-zA-Z0-9\s]' ,  ' ',str(text) )
    cleaned_new.append(' '.join(text.split()))

# 정규 표현식 이후 토큰나이즈
new_tfidf =tfidf.transform(cleaned_new)

# 토큰나이즈 이후 모델추론
probs = model.predict_proba( new_tfidf)

# 0.6 이상이면 긍정 , 0.4 이하이면 부종 그외 중립
for i in range(len(new_reviews)) :      # 리뷰 수 만큼 반법
    pos = probs[i][1]                   # i 번째 추론 결과 확률( 0 인덱스 )
    if pos >= 0.6 :
        contents = '긍정'
    elif pos <= 0.4 :
        contents = '부정'
    else : 
        contents = '중립'

    
    print(f'리뷰 : ' , {new_reviews[i]})
    print(f'감성분석  , {contents} , 긍정확률: {pos} ,  부정확률:{probs[i][0]}')