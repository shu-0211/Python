# 동적페이지 라이브러리 설치
# pip insatll playwright    # 셀레니움과 비슷한 동적 페ㅣ지 조작 라이브러리 설치 
# playwright install        # 백그라운드용 브라우저 ( 크로미움 ) 설치 

import asyncio      # 비동기 라이브러리 
from playwright.async_api import async_playwright       # 비동기 동적 페이지 라이브러리


# 예제 3] 동적 페이지 크롤링 , 대기/이벤트 존재하는 상태 
# 1) 크롤링할 페이지 주소 가져온다. 파라미터 분석, ssc = 검색결과 탭메뉴 , query = 검색어
url ="https://search.naver.com/search.naver?ssc=tab.image.all&query=짱구"
item_list =[]
# 2) 비동기 함수 만들기 
# async def 함수명() : # 함수 선언하고 동기화 
async def run ( )  : 
    # 2-1) async_playwright() 실행 하고 종료 되기 전까지 동기화 처리 지원
    async with async_playwright() as p :
        # 2-2) 크로미움( 구글 회사 제공하는 백그라운드용 오픈소스 브라우저 )
        # await p.chromium.lanuch ( headless=True백그라운드모드 / False 뷰모드)
        browser = await p.chromium.launch(headless=False)
        # 2-3) 현재 실행된 크로미움의 새로운 페이지(빈 페이지) 열기
        page = await browser.new_page() 
        # 2-4) 빈페이즈에 특정한 URL주소 대입/이동
        await page.goto(url)

        # 3) 스크롤 내리기 , 2번
        for i in range(2) :
            await page.wait_for_timeout(3000) # page.wait_for_timeout( 밀리초 ) : 밀리초 만큼 대기함수 상태 
            # await page.evaluate( "JS코드 삽입")
            # window.scrollTo( ) : 스크롤 이동함수 
            # document.body.scrollHeight : 현재 페이지의 스크롤 세로 높이 
            await page.evaluate( "window.scrollTo( 0 , document.body.scrollHeight)")

        # 4) 특정 마크업 가져오기 , .query_selector 한개 추출 , query_selector_all 여러개 추출 
        items = await page.query_selector_all(".tile_item")    # 이미지와 사진이름 포함하는 마크업 여러개 
        print( items )

        # 5) 반복문 이용한 사진/제목 
        for item in items : 
            title = await item.query_selector( '.info_title')
            title = await title.inner_text() if title else '제목없음' # 특정한 마크업의 사이 텍스트 추출 ( .innerText )
            img = await item.query_selector('img._fe_image_tab_content_thumbnail_image')
            img = await img.get_attribute('src') if img else '이미지없음'  # 특정한 마크업의 속성값 추출
            item_list.append( {'제목' : title , "이미지링크" : img})
    return item_list

# *** asyncio.run( 동기화함수() ) ***
item_list = asyncio.run( run() )
print( item_list )