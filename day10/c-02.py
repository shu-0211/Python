import requests
from bs4 import BeautifulSoup
# 동적 페이지 크롤링 (페이징처리)
# 예스 24 베스트 셀러 도서 정보 크롤링 / 페이징처리(반복문)
# 1) 크롤링할 주소 가져온다. 정리 / 분석 , cegory

# https://www.yes24.com/product/category/daybestseller?categoryNumber=001&pageNumber=1&pageSize=24&type=day
book_list = []
for page in range( 1, 4)    :
    url = f"https://www.yes24.com/product/category/daybestseller?categoryNumber=001&pageNumber=2"
    # 2) URL 요청
    response = requests.get(url)

    # 3) HTML 파싱
    soup = BeautifulSoup( response.text , "html.parser")

    # 4) 특정한 마크업 추출( 책제목, 가격 , 저자)
    books = soup.select(".item_info")
    print(books)

    # 5) 
    for book in books:
        title = book.select_one('.gd_name').get_text
        price = book.select_one('.yes_b').get_text()
        auth = book.select_one('.info_auth').get_text().strip().replace("\n","").replace("\r","")

    # 6) 리스트
    book_list.append( {"제목" : title , "가격" : price , "저자" : auth})
    print( book_list )