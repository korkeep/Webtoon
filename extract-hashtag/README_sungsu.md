# HashTag Algorithm Description (Made by 2016104109 Sungsu)
1. 웹툰 제목을 웹툰 코드와 매치
 - 웹툰 코드, 웹툰 이름이 짝으로 정의된 dict.json을 dict.csv로 만든다. (json_to_csv.py 이용)
 - Pandas의 join 기능 활용해 '웹툰 이름'을 칼럼에 추가한 search_output.csv를 만든다. (name_added.py 이용)

2. 웹툰 "제목 +키워드"를 파라미터로, 네이버 검색 결과를 크롤링
 - 키워드에는 '사람들이 얼마나 자주 사용하는지, 실제로 쓰이는 낱말인지'에 대한 가치가 필요하다.
 - td_idf 결과만으로는 위 사항을 만족하지 못하는 것 같아서 네이버 검색 API를 이용해 크롤링했다. (crawling_bs4.py 이용)
 - search 파라미터 = 제목 + 띄워쓰기 + 키워드 형식으로 검색한다. (파라미터에는 웹 URL 인코딩이 활용됐음)
 - url = 'https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query={}'.format(search)

3. 검색 결과의 항목 수를 count
 - 원래는 결과가 '30' 이상인 것들은 상용어구, 조사와 같은 의미 없는 값이라 판단해 Delete 했지만,
 - 샘플 데이터 500개를 이용해 테스트해본 결과 중요한 '키워드 단어'도 함께 삭제되는 경우도 종종 있었다.
 - 항목 수의 최대값은 10으로 둠으로써 'td_idf' 분석 결과의 의미를 유지하는 동시에,
 - '사람들이 얼마나 자주 사용하는지, 실제로 쓰이는 낱말인지'에 대한 가치를 담으려고 했다.
 - 해쉬태그로 쓰일 5개 키워드 선출 알고리즘 = count * td_idf 값이 높은 순서로 정렬 후 상위 10단계로 자르기 (crawling_bs4.py 이용)

4. 조사(은, 는, 이, 가) 제거 + 의미없는 단어 중복 제거
 - 웹툰 코드를 ID로 groupby를 이용해 키워드를 List로 묶어서 List column에 추가한다.
 - List화된 것들을 앞에서 체크한 키워드와 중복되는 것이 없는지 확인한다. (교수, 교수가, 교수는 = '교수'로 묶여야)
 - 중복되는 것은, 현재 스트링 인덱스 슬라이싱 알고리즘을 활용해 비교한다. (rank_added.py 이용)

4. 추출한 해쉬태그 csv 형태로 데이타 전달
 - Webtoon_ID, Hashtag_keword, Rank 순으로 hashtag.csv를 만들어 프론트에 전달한다.
