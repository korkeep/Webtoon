# 네이버 웹툰 댓글 분석
<img width="672" alt="Screen Shot 2020-06-18 at 5 44 42 PM" src="https://user-images.githubusercontent.com/17666783/85104142-fd91d500-b242-11ea-9030-aa91fed22abb.png">

<img width="547" alt="Screen Shot 2020-06-18 at 5 48 00 PM" src="https://user-images.githubusercontent.com/17666783/85104146-fff42f00-b242-11ea-9752-7b7435bae309.png">

## 목차
1. [Acquisition](#acquisition)
1. [Preparation](#preparation)
1. [Model](#model)
1. [Visualize](#visualize)
1. [spark-pipeline](#spark-pipeline)
1. [Web Visualization](#web)
1. [Hash Tagging](#hashtag)
1. [Demonstration](#demonstration)

## 설명
네이버 웹툰의 댓글을 분석해 웹툰을 추천하고 웹툰별 해쉬태그 및 키워드(wordcloud)를 제공한다.


### Installation

**Local Analysis**
```
$ git clone https://github.com/philjjoon/2020-01-group1.git
$ pip install -r 'requirements.txt'
```

**Web**
```
$ git clone https://github.com/philjjoon/2020-01-group1.git
$ cd /2020-01-group1/visualize/web
$ npm install package-lock.json
cd ../db/finaldb.sql data import in MySQL
mysql > mysql -u root -p databasename > finaldb.sql
$ node app.js 50077
```



### 주의사항
각 단계는 각 디렉토리에서 실행해야 작동이 보장됩니다.\
예: preparation.py는 preparation에서 실행해야 합니다.

필요한 의존성 목록은 requirements.txt에 명시되어 있습니다.  
## Acquisition
make_title.py => scheduler.py 순서로 실행을 권장합니다.\ 
또는 다음 링크에서 다운로드하세요: [Google Drive (경희대 전용)](https://drive.google.com/file/d/1tbzGGU8wmZ7LKnAeOI1kRLQaVWMptFIh/view?usp=sharing)
### make_title_dic.py
입력: incomplete.html, complete.html\
출력: dict.json, titleId.json\
입력 HTML을 파싱해서 titleId 목록과 titleId-제목 사전을 만든다.\
이때 유료 웹툰은 제외되며 각 html 파일의 주소는 다음과 같다.\
incomplete.html: https://comic.naver.com/webtoon/weekday.nhn \
complete.html: https://comic.naver.com/webtoon/finish.nhn 
### comments.py
입력: titleId.txt\
출력: 댓글 json 파일들 {titleId}.json 형태\
titleId 목록을 통해 댓글을 크롤링 한다.
Selenium을 사용하므로 느리다.
### crawler.py
입력: titleId.txt\
출력: 댓글 json 파일들 {titleId}.json 형태\
titleId 목록을 통해 댓글을 크롤링 한다.
네이버 내부 API를 사용하여 속도가 빠르다.
### scheduler.py
입력: titleId.txt\
출력: 댓글 json 파일들 json_of_{best|all}/{titleId}.json 형태\
titleId 목록을 통해 댓글을 크롤링 한다.\
crawler.py를 병행 처리하기 위해 사용한다. 시간이 단축된다. 
## Preparation
preparation.py=>csv2parquet.py 순으로 실행해야 합니다.
### preparation.py
입력: 댓글 json 파일들(의 디렉토리)\
출력: 결합 후 전처리된 텍스트 파일, 그 파일의 titleId 순서가 적힌 텍스트 파일(파일이름.title_id.txt)\
명령줄 인수: 
* -b 베스트 댓글만 입력으로 사용 (json_of_best, 기본은  json_of_all)
* -H 한글만 사용 (기본은 영숫자도 포함)
* -d DoubleSpaceLineCorpus 형태 저장(기본은 parquet용 csv)

json 파일을 전처리해 문장 단위 텍스트 또는 DoubleSpaceLineCorpus로 저장한다.
### csv2parquet.py
입력: preparation.py로 만든 댓글 csv 파일
출력: 동일한 내용의 parquet파일

댓글 csv를 원본json과 동일한 스키마의 parquet로 변환한다.\
title_id:uint32, episode_num:uint32(),comment_num': uint32, sentence: string, registered_time:timestamp('s', 'UTC+09:00')
## Model
words.py=>word2vec.py 순서로 실행해야 합니다.
### words.py
입력: DoubleSpaceLineCorpus\
출력: {filename}.words, {filename}_scores.json\
명령줄 인수: 
* filename 입력으로 사용할 파일 이름

문장 단위 택스트에서 단어점수를 기준으로 키위드를 추출하고, .words로 저장한다.\
또한 단어들의 단어점수를 json으로 저장한다. 
### word2vec.py
입력: DoubleSpaceLineCorpus, score.json(words.py의 출력)\
출력: w2v.model, w2v.model.wv.vectors.npy, w2v.model.trainables.syn1neg.npy, w2v.wv\
명령줄 인수: 
* corpus DoubleSpaceLineCorpus 파일 이름
* scores scores.json 파일이름

DoubleSpaceLineCorpus를 score.json을 이용해 MaxScoreTokenizer로 처리한다.\
그 후 처리한 문서로 word2vec.py를 학습하고 gensim model로 저장한다.\
베스트 댓글의 벡터만 추출해도 분석에 큰 지장이 없다.
### wv2parquet.py
입력: w2v.wv
출력: w2v.parquet

추출한 Word Vector를 사용해 (단어, Word Vector) 쌍으로 구성된 parquet 파일을 만든다.
## Visualize
### w2v_demo.py
입력: w2v.model* (word2vec.py의 출력들)\
명령줄 인수: 
 * positive 유사 벡터 추정 시 positive에 해당 하는 단어들
 * -n 유사 벡터 추정 시  negative에 해당 하는 단어들
 
 w2v_demo positive \[, ...\] \[-n\[, ...\]\] 형태 사용\
 벡터 추정 해서 가장 가까운 순서대로 5개 추천
 
### visualize_w2v.py
입력: w2v.model* (word2vec.py의 출력들)

pandas, matplotlib, scikit-learn을 사용해 2D 평면에 벡터를 사상한다.
## spark-pipeline
Spark를 활용해 추가적인 분석을 합니다.\
Spark와 HDFS가 필요하고, 기본 HDFS 디렉토리는 hdfs://master:9000/user/hadoop/입니다.\
실행 순서는 ParquetSave=>TokenCount=>TF_IDF=>weighting=>D2V=>d2v.py(로컬)을 권장합니다.\
만약 문장단위 Doc2Vec을 하고 싶다면 ParquetSave=>doctovec_test로 실행하시면 됩니다.
### prerequisites
* csv2parquet.py의 댓글 parquet
* words.py의 scores.json
* wv2parquet.py의 w2v.parquet(선택 사항, 문장단위 분석 때는 불필요)

이상의 파일을 HDFS에 올려두어야 합니다.
### ParquetSave.ipynb
입력: 댓글 parquet, scores.json
출력: all_hangul_tokens/\*.parquet 형태로 파티션되어 저장

Soynlp의 MaxScoreTokenizer를 사용해 Tokenize하고 그 결과를 parquet로 저장한다.
### TokenCount.ipynb
입력: all_hangul_tokens/\*.parquet
출력: token_count/\*.parquet 형태로 파티션되어 저장

저장된 토큰들을 title_id 별로 세어 그 결과를 parquet로 저장한다.
### TF_IDF.ipynb
입력: token_count/\*.parquet
출력: tf_idf/\*.parquet , tf_idf.csv/\*.csv 형태로 파티션 되어 저장

TokenCounting의 결과를 바탕으로 TF-IDF 분석을 해 키워드를 구하고, 그 결과를 parquet와 csv로 저장한다.\
csv는 단순 텍스트이므로 cat명령어를 통해 결합 가능하고, 이는 DB에 사용된다.
### weighting.ipynb
입력: w2v.parquet, token_count/\*.parquet
출력: weighted_vector/\*.parquet 형태로 파티션되어 저장

Doc2Vec방식을 그 문서 댓글에 포함된 Word2Vec들의 가중평균으로 정의한다. 이때 가중치는 단어의 등장 수이다.\
weighting에서는 각 문서의 토큰마다 그 문서에서 등장한 횟수*word vector로 가중된 벡터를 만들어 저장한다.\
weighting과 D2V는 메모리 오류로 인해 나눈 것으로, 환경의 메모리가 충분하면 나눌 필요가 없다.
### D2V.ipynb
입력: weighted_vector/\*.parquet, token_count/\*.parquet
출력: doc2vec/\*.parquet, doc2vec_csv/\*.csv 형태로 파티션되어 저장

가중된 벡터들을 사용해 가중평균을 내는 작업을 마무리한다.\
이렇게 나온 평균 벡터를  Document Vector로서 사용한다.\
csv는 cat하여 d2v.csv 형태로 저장해 doc_distance.py에 활용한다.
### doc_distance.py
입력: D2V의 출력 파일인 d2v.csv
출력: dist.csv

Doc2Vec csv 파일을 읽고 문서 간 cosine 거리를 구해 (tite_id1, title_id2, 둘 사이의 cosine 거리) 형태의 csv 파일로 저장한다.\
이는 DB에 사용된다.

---

### doctovec_test.ipynb
*Implements and evaluates word2vec to develop doc2vec

 - Pre-loads parquet file since there was memory allocation problem
 - Splits word tokens to use word2vec library
 - Evaluates accuracy with Random Forest Classifier

### dist_algorithm.ipynb
*Matches titleid to title and show

 - Makes enable dictionary function in sqlcontext UDF


## <a name="web"></a> Web Visualization (visualize/)
### web
Data Visualization: Responsive WEB <br/>
Environment: <br/>
Express Framework <br/>
-Back-end: Node JS <br/>
-Front-end: HTML/CSS/JS <br/>

<br>

#### public
/jqcloud: wordcloud module <br/>
/hashtags, /keywords, /suggestions: insert analysis result (.csv) to db <br/>

#### routes
/index.js: <br/>
crawling_webtoon(): crawling webtoon info (title_id, title_name, thum_link, website_link) using Cheerio



### db
#### db.sql
MySQL DB <br/>
EER Diagram: <br/>
![eer diagram](https://user-images.githubusercontent.com/17666783/85103003-c91d1980-b240-11ea-89c0-60115ac678ee.png)


## <a name="hashtag"></a> HashTag Algorithm Description
**Step1:** 웹툰 제목을 웹툰 코드와 매치  
- 웹툰 코드, 웹툰 이름이 짝으로 정의된 dict.json을 dict.csv로 만든다. (json_to_csv.py 이용)
- Pandas의 join 기능 활용해 '웹툰 이름'을 칼럼에 추가한 search_output.csv를 만든다. (name_added.py 이용)

**Step2:** 웹툰 "제목 +키워드"를 파라미터로, 네이버 검색 결과를 크롤링  
- 키워드에는 '사람들이 얼마나 자주 사용하는지, 실제로 쓰이는 낱말인지'에 대한 가치가 필요하다.
- td_idf 결과만으로는 위 사항을 만족하지 못하는 것 같아서 네이버 검색 API를 이용해 크롤링했다. (crawling_bs4.py 이용)
- search 파라미터 = 제목 + 띄워쓰기 + 키워드 형식으로 검색한다. (파라미터에는 웹 URL 인코딩이 활용됐음)
- url = 'https://m.search.naver.com/search.naver?where=m_view&sm=mtb_jum&query={}'.format(search)

**Step3:** 검색 결과의 항목 수를 count  
- 원래는 결과가 '30' 이상인 것들은 상용어구, 조사와 같은 의미 없는 값이라 판단해 Delete 했다.
- 샘플 데이터 500개를 이용해 테스트해본 결과 중요한 '키워드 단어'도 함께 삭제되는 경우도 종종 있었다.
- 항목 수의 최대값은 10으로 둠으로써 'td_idf' 분석 결과의 의미를 유지하는 동시에,
- '사람들이 얼마나 자주 사용하는지, 실제로 쓰이는 낱말인지'에 대한 가치를 담으려고 했다.
- 해쉬태그로 쓰일 5개 키워드 선출 알고리즘 = count * td_idf 값이 높은 순서로 정렬 후 상위 10단계로 자르기 (crawling_bs4.py 이용)

**Step4:** 조사(은, 는, 이, 가) 제거 + 의미없는 단어 중복 제거  
- 웹툰 코드를 ID로 groupby를 이용해 키워드를 List로 묶어서 List column에 추가한다.
- List화된 것들을 앞에서 체크한 키워드와 중복되는 것이 없는지 확인한다. (교수, 교수가, 교수는 = '교수'로 묶여야)
- 중복되는 것은, 현재 스트링 인덱스 슬라이싱 알고리즘을 활용해 비교한다. (rank_added.py 이용)

**Step5:** 추출한 해쉬태그 csv 형태로 데이타 전달  
- Webtoon_ID, Hashtag_keword, Rank 순으로 hashtag.csv를 만들어 프론트에 전달한다.

## Demonstration
DEMO Video: https://drive.google.com/file/d/1l5Mv4z3rhxoX49fQrmCIsKGX1oT5JSGG/view?usp=sharing <br/>
![image](https://user-images.githubusercontent.com/20378368/108582395-67382500-7376-11eb-82b0-7fec9d67a01a.png)

