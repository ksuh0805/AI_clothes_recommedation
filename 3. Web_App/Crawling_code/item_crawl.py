# BeautifulSoup4 사용 musinsa.com 아이템 이미지 크롤링
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve

# item_list 텍스트 파일에 있는 아이템 url에서 이미지 저장
read_file_path = './item_list.txt'
read_f_style = open(read_file_path, 'r', encoding='utf-8')
lines = read_f_style.readlines()
urls = []
item_keys = []
# txt 파일에서 한줄씩 읽어와 url 리스트에 저장
for line in lines[1:]:
    words = list(line.split())
    urls.append(words[2])
    item_keys.append(words[0])
read_f_style.close()


# 리스트에 저장된 url에서 이미지에 해당하는 태그 이미지 저장
for i, url in enumerate(urls):
    item_url_request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    url_open = urlopen(item_url_request).read()
    item_page = BeautifulSoup(url_open, 'html.parser')
    item_img_url = 'https:' + item_page.select_one('.product-img > img')['src']
    down_dir = './item_img/'

    urlretrieve(item_img_url, down_dir + item_keys[i] + '.jpg')

