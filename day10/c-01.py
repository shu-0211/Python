# 웹 크롤링 : 웹페이지 존재하는 데이터들을 수집하는기술
# HTML/CSS 기초 지식
# 파이썬 크롤링 라이브러리 : 정적( request/BeautifulSoup )  , 동적( Seleium , Playwright)등

# 확인 
    # 1. 크롤링할 페이지의 도메인주소/robots.txt
    # https://www.jobkorea.co.kr/robots.txt
    # User-agent:사용자/브라우저/AI , Disallow: 불가능 , Allow: 불가능

    # 2. 개발자도구(F12) -> CTRL + SHIFT + C -> 크롤링 요소 선택 -> 선택자/식별자

    # 설치1 : pip install requests
    # 설치2 : pip install beautifulsoup4

# 1] 네이버 검색 정보 크롤링( 정적 )
# 1. 크롤링 주소가져오기, *파라미터 정리* , ? 쿼리스트링
url = f"https://search.naver.com/search.naver?&query=안양날씨"
# 2. requests 라이브러리로 해당 주소 요청하기 
import requests
# requests.get( 요청할 주소)
response = requests.get( url ) # <Response [200] > # HOMEㄷ
print(response.text)    # 요청한 주소의 BTML


# 3. 요청성공왔으면 요청한 페이지 HTML 파싱하기

from bs4 import BeautifulSoup   # 요청된 RJD 

soup = BeautifulSoup(response.text , "html.parser")
print(soup)
# 3. 요청성공왔으면 요청한 페이지 HTML 파싱하기

# 4. 파싱한 이유 : 특정한 식별자(마크업)의 텍스트/정보추출
# soup.select(선택자): 여러개 출추
text = soup.select_one(".temperate_text")

# 5. 마크업 사이의 텍스트 추출
# 추추출한ㄹ한 DOM_get_TEs
print