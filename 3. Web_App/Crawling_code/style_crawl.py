# BeautifulSoup4 사용 musinsa.com 스타일별 코디 이미지 및 아이템 정보 크롤링
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve


# parameters: url_link: 스타일별 링크, style_category: 스타일 카테고리명
# 스타일 코디 이미지와 상/하의 악세서리 등 아이템 링크, 이미지 수집
def url_crawl_download(url_link: str, style_category: str):
    item_key_num = 0
    url_request = Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})
    style_list_url = urlopen(url_request).read()
    style_list_page = BeautifulSoup(style_list_url, 'html.parser')

    style_code_list = [style_code
                       for style_code in style_list_page.findAll('a', {'class': 'style-list-item__link'})]

    style_list = []
    # 스타일 상세페이지 진입 위한 스타일 코드 리스트 만들기
    for style_code in style_code_list:
        code = ''.join(filter(str.isdigit, style_code['onclick']))
        style_list.append(code)

    # 각 스타일별 상세페이지 진입
    for i, style in enumerate(style_list[:31]):
        style_url = 'https://store.musinsa.com/app/styles/views/' + style
        style_url_request = Request(
            style_url, headers={'User-Agent': 'Mozilla/5.0'})
        style_url_open = urlopen(style_url_request).read()
        style_page = BeautifulSoup(style_url_open, 'html.parser')

        # 스타일 상세페이지에서 얻어와야 하는 것
        # 1) 스타일 코디 이미지
        # 2) 스타일 상품 정보 (url, 스타일 category, 색상), 색상은 나중에 수기 입력해 줘야할듯...
        # ** 성별은 수기 입력해줘야 할듯...

        # 1) 스타일 코디 이미지 다운로드 및 파일에 정보 입력
        style_img = [img
                     for img in style_page.findAll('img', {'class': 'detail_img'})]
        style_img_url = style_img[0]['src']
        style_key = style_category + '_' + str(i).zfill(3)
        down_dir = './img/'
        urlretrieve(style_img_url, down_dir + style_key + '.jpg')
        style_f = open('style_list.txt', 'a', encoding='utf-8')
        style_f.write(style_key + '\t' + style_category + '\n')
        style_f.close()

        # 2) 스타일 상품 정보 파일에 쓰기
        style_items = [item
                       for item in style_page.findAll('a', {'class': 'brand_item'})]
        item_f = open('item_list.txt', 'a', encoding='utf-8')
        for item in style_items:
            item_url = 'https://store.musinsa.com' + item['href']
            item_url_request = Request(
                item_url, headers={'User-Agent': 'Mozilla/5.0'})
            item_url_open = urlopen(item_url_request).read()
            item_page = BeautifulSoup(item_url_open, 'html.parser')
            item_type = item_page.select_one('.item_categories > a').get_text()
            item_key = style_category + '_' + 'item' + \
                '_' + str(item_key_num).zfill(4)
            item_f.write(item_key + '\t' + style_category + '\t' +
                         item_url + '\t' + item_type + '\t' + style_key + '\n')
            item_key_num += 1
        item_f.close()


# 스타일별 링크
casual = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=american_casual&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
easy_casual = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=easy_casual&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
street = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=street_casual&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
formal = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=formal_office&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
sports = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=sports&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
retro = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=retro&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
girlish = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=girlish&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
chic = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=chic&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
golf = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=golf&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
romantic = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=romantic&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
business = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=office&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
dandy = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=dandy&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
sports_casual = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=sport_casual&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
semi_formal = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=semi_formal&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'
campus = 'https://store.musinsa.com/app/styles/lists?use_yn_360=&style_type=campus&brand=&model=&tag_no=&max_rt=&min_rt=&display_cnt=60&list_kind=big&sort=date&page=1'

# 스타일별 크롤링 실행
url_crawl_download(casual, 'casual')
url_crawl_download(easy_casual, 'easy-casual')
url_crawl_download(street, 'street')
url_crawl_download(formal, 'formal')
url_crawl_download(sports, 'sports')
url_crawl_download(retro, 'retro')
url_crawl_download(girlish, 'girlish')
url_crawl_download(chic, 'chic')
url_crawl_download(golf, 'golf')
url_crawl_download(romantic, 'romantic')
url_crawl_download(business, 'business')
url_crawl_download(dandy, 'dandy')
url_crawl_download(sports_casual, 'sports-casual')
url_crawl_download(semi_formal, 'semi-formal')
url_crawl_download(campus, 'campus')
