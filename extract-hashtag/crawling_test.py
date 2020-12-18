# 원래 소스코드 - 동아일보 기사 크롤링 참고
# 크롤링 결과 : out.txt
# import sys
# from bs4 import BeautifulSoup
# import urllib.request
# from urllib.parse import quote
 
 
# TARGET_URL_BEFORE_PAGE_NUM = "http://news.donga.com/search?p="
# TARGET_URL_BEFORE_KEYWORD = '&query='
# TARGET_URL_REST = '&check_news=1&more=1&sorting=1&search_date=1&v1=&v2=&range=1'
 
 
# def get_link_from_news_title(page_num, URL,output_file):
#     for i in range(page_num):
#         current_page_num = 1 + i*15
#         # 페이지당 15개의 게시물.        
#         position = URL.index('=')
#         # URL 처음 = 오는 위치 반환 (URL에 몇페이지 인지 추가하기 위해)        
#         URL_with_page_num = URL[: position+1] + str(current_page_num) \
#                             + URL[position+1 :]
#         # 페이지가 있는 URL 재구성        
#         source_code_from_URL=urllib.request.urlopen(URL_with_page_num)
#         # 재구성한 URL을 request로 호출        
#         soup=BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='UTF-8')
#         # BeautifulSoup로 변환, 기사 분석 후 추출하기 위해
        
#         for title in soup.find_all('p','tit'):
#             title_link = title.select('a')
#             article_URL = title_link[0]['href']
#             get_text(article_URL, output_file)
#         # 본문 기사가 담긴 URL을 찾기위해
 
# def get_text(URL, output_file):
#     source_code_from_url = urllib.request.urlopen(URL)
#     # urlllib로 기사 페이지를 요청받습니다.
#     soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='UTF-8')
#     # BeautifulSoup로 페이지를 분석하기위해 soup변수로 할당 받습니다.
#     content_of_article = soup.select('div.article_txt')
#     # 기사의 본문내용을 추출
#     for item in content_of_article:
#         string_item = str(item.find_all(text=True))
#         output_file.write(string_item)
#     # 기사 텍스트가 있다면 파일에 쓴다
    
 
# def main():
#     keyword = "대통령선거" #검색하고 하는 단어
#     page_num = 5          #가져올 페이지 숫자
#     output_file_name = "out.txt" #출력할 파일명
#     target_URL = TARGET_URL_BEFORE_PAGE_NUM + TARGET_URL_BEFORE_KEYWORD \
#                  + quote(keyword) + TARGET_URL_REST
#     output_file = open(output_file_name, 'w', -1,"utf-8")
#     get_link_from_news_title(page_num, target_URL, output_file)
#     output_file.close()
 
 
# if __name__== '__main__':
#     main()


# 소스코드 재구성했는데 403 Forbidden 뜬다
# 다른 방법은 없을까?
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
 
TARGET_URL_BEFORE_PAGE_NUM = "https://namu.wiki/w/"

def get_link_from_title(URL, output_file):
    # URL을 request로 호출 
    source_code_from_URL=urllib.request.urlopen(URL)       
        
    # BeautifulSoup로 변환, 분석 후 추출하기 위해
    soup=BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='UTF-8')
        
    # 본문이 담긴 URL을 찾기위해
    for title in soup.find_all('p','tit'):
        title_link = title.select('a')
        article_URL = title_link[0]['href']
        get_text(article_URL, output_file)
        
def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    # urlllib로 기사 페이지를 요청받습니다.
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='UTF-8')
    # BeautifulSoup로 페이지를 분석하기위해 soup변수로 할당 받습니다.
    content_of_article = soup.select('div.article_txt')
    # 본문내용을 추출
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)
    # 기사 텍스트가 있다면 파일에 쓴다

def main():
    keyword = "테스트" #검색하고 하는 단어
    output_file_name = "test.txt" #출력할 파일명
    target_URL = TARGET_URL_BEFORE_PAGE_NUM + quote(keyword)
    output_file = open(output_file_name, 'w', -1,"utf-8")
    get_link_from_title(target_URL, output_file)
    output_file.close()

if __name__== '__main__':
    main()