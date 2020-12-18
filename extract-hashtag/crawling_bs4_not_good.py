# Crawuling bs4
import csv
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
import pandas as pd

# quote_plus를 통해, 한글이 웹에 들어가는 형식으로 인코딩 된 명령어 삽입
result_df = pd.read_csv("./search_output.csv")
result_df.tail(5)

new_df = result_df
new_df.columns = ['num', 'id', 'name', 'keyword', 'result', 'rank']
name_keyword_df = result_df.loc[:,['num', 'id', 'name', 'keyword', 'rank', 'result']]
name_keyword_df.tail()

search_count = []

# 제목을 parameter로 네이버 검색 결과 추출
# 최종 결과때는 groupby name으로 하고, count 순으로 출력돼야
#for i, row in name_keyword_df.iterrows(): 직관적이지만, 속도가 너무 느리다
for i in name_keyword_df.index:
    temp = name_keyword_df.at[i, 'name'] + ' ' + name_keyword_df.at[i, 'keyword'] # name + keyword
    
    search = quote(temp)
    url = 'https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query={}'.format(search)

    html = urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    total = soup.select('.api_txt_lines.total_tit')
    
    search_count.append(len(total))

# count >= 30인 항목은 '조사'의 가능성이 높으므로, 검색 결과로부터 제외
# count 순으로 keyword sorting, 만약 count가 같으면 output이 높은 순
name_keyword_df["count"] = search_count
name_keyword_df = name_keyword_df[name_keyword_df['count'] != 30]

# 일단 10개를 뽑아오고, 중복처리는 나중에 해본다.
name_keyword_df = name_keyword_df.groupby('id').apply(lambda x: x.nlargest(10, 'count'))
name_keyword_df

# count >= 30인 항목은 '조사'의 가능성이 높으므로, 검색 결과로부터 제외
# count 순으로 keyword sorting, 만약 count가 같으면 output이 높은 순
result_df = name_keyword_df.copy()
temp_df = result_df.set_index('id', drop=True, append=False, inplace=False)
new_df = temp_df.loc[:, ['keyword']]
new_df.to_csv('keyword.csv', mode='w')
new_df