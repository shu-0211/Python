# httpx 란? 외부 api 통신하는 라이브러리 ,  공공데이터   , axios/client/httpx
# 설치 : pip install httpx 
# httpx 라이브러리에는 .json() 타입변환 하지만 xml 변환 지원하지 않는다. 
# xmltodict 란? xml 파싱 라이브러리 
#설치 2 : pip install xmltodict

import httpx
import pandas as pd

# [0] 공공데이터포털 본인 인증키 
service_key = "a15d3190788aca086d3b4dd16ecd0f2e87377ca9a382cc66309f944228ad62c7"


# [1]  공공데이터포털 json 형식의 자료 요청 , 대구광역시 중구 맛집 현황
def test1():
    # https://api.odcloud.kr/api/15052602/v1/uddi:855807e2-fe8a-4e47-8a5a-ce1894e410d7_201909031553?page=1&perPage=10&serviceKey=a15d3190788aca086d3b4dd16ecd0f2e87377ca9a382cc66309f944228ad62c7
    # [2] 신청한 API의 주소 및 파라미터 분석, page 현재페이지 , perPage = 페이지당 자료수 , serviceKey
    url = "https://api.odcloud.kr/api/15052602/v1/uddi:855807e2-fe8a-4e47-8a5a-ce1894e410d7_201909031553"
    url += "?page=1"
    url += "&perPage=147"
    url += f"&serviceKey={service_key}"

    # 3] httpx 이용하여 통신하기 , import httpx
    # httpx.HTTP 메소드명 ( 통신할 주소 )  , 통신 결과 반환 
    response = httpx.get( url )
    print( response )       # <Response [200 OK] > 성공했다는 뜻

    # 4] 응답 결과 JSON 변환 , .json()
    response_json = response.json()
    print( response_json )

    # 판다스에 저장하기 import pandas as pd 
    df = pd.DataFrame( response_json['data'] )  # {"currentCount" : 10 , "data" : [실질자료]}
    df.info() #확인
    print(df.info())

test1()
import xmltodict # xml 변환 라이브러리 
def test2() :
    # 1] 요청할 API 주소
    url = "https://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyFullDown"
    url += f"?serviceKey={service_key}"
    url += "&pageNo=1"
    url += "&numOfRows=100"

    # 2] httpx 이용한 api 요청
    response = httpx.get(url)

    # 3] 요청 응답 자료를 문자열로 변환하여 파이썬 dict 형식으로 변환
    response_dict = xmltodict.parse(response.text)

    # 4] <response> -> <body>  ->  <items>  ->  <item>
    df = pd.DataFrame( response_dict['response']['body']['items']['item'])
    df.info()
test2()