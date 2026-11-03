import asyncio
from playwright.async_api import async_playwright

# 예제4] 동적 크롤링 
# 1) 중고나라 홈페이지 제품 크롤링 , url = "https://web.joongna.com/search/"
async def run() :   # 함수 정의

    ####################
    keyword = input("중고 제품명 : ")
    min_price = input("최소 가격 : ")
    max_price = input("최대 가격 : ")

    # 2) async_playwright() 실행하고 
    async with async_playwright() as p : 
        # 3) 크로미움 실행
        browser = await p.chromium.launch( headless=False)
        # 4) 빈 페이지 실행 
        page = await browser.new_page()
        # 5) 특정 페이지 이동 
        await page.goto(f'https://web.joongna.com/search/{ keyword }')
        # 6) 3초 대기상태 
        await page.wait_for_timeout(3000)
        # 7) 입력받은 값으로 웹페이지에 채우기 ,
        # page.get_by_속성명( "속성값" )
        # DOM.fill( 값 )                    # 속성 값 대입 
        # page.get_by_placeholder( "최소가격").fill( ) : placeholder에 '최소 가격' 이면 입력받은 값으로 
        await page.get_by_placeholder("최소 가격").fill(min_price)     # html placeholder 이용하여 특정 마크업 식별
        await page.wait_for_timeout(1000)                             # 1초간 일시정지

        await page.get_by_placeholder("최대 가격").fill(max_price)     # html placeholder 이용하여 특정 마크업 식별
        await page.wait_for_timeout(1000)                             # 1초간 일시정지

        # 8) 특정한 마크업 클릭 이벤트 실행 , Dom.colick()S
        await page.wait_for_timeout( 3000 )

        # 9) 제품사진, 제품명, 제품가격 추출 , 
        # href^ : '/시작주소/' : 시작주소로 시작하는 모든 주소 식별
        items = await page.query_selector_all("div.rounded-none > a.w-full")
        print( items)
        for item in items : 
            title = await item.query_selector('.typo-body-sm-medium-14')
            title = await title.inner_text() if title else "제품명 없음"
            price = await item.query_selector('.typo-title-lg-semibold-18')
            price = await price.inner_text() if price else "제품 가격 없음"
            img = await item.query_selector('img')
            img = await img.get_attribute('src') if img else "이미지 없음"
            print( title , price , img ) 
        # 10) 안전하게 직저 브라우저 종료 
        await browser.close()


asyncio.run ( run())        # 함수 실행