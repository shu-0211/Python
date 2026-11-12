# 비즈니스 로직 == 머신러닝 모델 예측
import pandas as pd 
class ItemService : 
    # 생성자 
    def __init__(self):
        # self.변수명 = 값 # 맴버변수 선어 
        self.df = pd.DataFrame([
            {'id':1,'name':'콜라','price':1000},
            {'id':2,'name':'사이다','price':1500}
        ])

    # 함수 
    def items(self): 
        # df.to_dict(orient='records')
        # 행 마다 딕셔너리 반환 하여 리스트 반환 함수
        return self.df.to_dict(orient='records')

    # 저장
    def save(self , item) :
        # 1. 저장할 딕셔너리를 df 변경 
        saveDf = pd.DataFrame( [item] )
        # 2. 기존 df에 연결 , .pd.concat( [df1,df2] )
        self.df = pd.concat(
            [self.df , saveDf ],
            ignore_index= True )
        return True

    # 수정
    def update(self , item ) :
        uid = item.get('id')    # 1. 수정할 id 조회 
        # 2. 현재 데이터프레임에 입력받은 수정할 id가 없으면
        if uid not in self.df['id'].values : 
            return "수정할 상품이 없습니다."
        # 3. 현재 df에 입력받은 수정할 id가 같다면 index 조회 
        idx = self.df[self.df['id'] == uid].index

        # 4. 찾은 인덱스에 값 수정 
        # item.keys()   : 딕셔너리.keys() => [속성명 , 속성명]
        # item.values()   : 딕셔너리.values() => [속성값 , 속성값]
        self.df.loc[ idx , item.keys() ] = item.values()
        return True

    def delete( self , id) : 
        if id not in self.df['id'].values : 
            return False
        # 존재하면 해당 id의 행 제외 
        self.df = self.df[self.df['id'] != id ]

#########################################
# 서비스 객체 생성
item_service = ItemService()
