# 단어 중복처리
import pandas as pd
keyword_df = pd.read_csv("./keyword.csv")

# Algorithm 
# 1. 일단 ID로 groupby를 이용해 묶어서 List화 한다
# 2. List화된 것들을 앞에 나온 것들과 겹치는 것이 없는지 확인한다.
# 3. 겹치는 것은, 현재 인덱스의 스트링의 마지막 엘리먼트에서 0, -1, -2한 값을 비교한다.

# 1. 일단 ID로 groupby를 이용해 묶어서 List화 한다
list_df = keyword_df.groupby('id')['keyword'].apply(list).reset_index(name='list')
list_df

# 2. List화된 것들을 앞에 나온 것들과 겹치는 것이 없는지 확인한다.
def check_ahead(a, b):
    # 두번째 파라미터 : result list의 크기만큼 반복
    for i in range (0, len(b)):
        # 3. 현재 인덱스의 스트링의 마지막 엘리먼트에서 0, -1한 값을 비교한다
        if a==b[i][:len(b[i])-3]: # 한글이어서 3번 빼줘야 함, 인코딩 형식
            return False
        elif a[:len(a)-3]==b[i]: # 한글이어서 3번 빼줘야 함, 인코딩 형식
            return False
        elif a[:len(a)-3]==b[i][:len(b[i])-3]: # 한글이어서 3번 빼줘야 함, 인코딩 형식
            return False
    return True

# result_df
result_df = pd.DataFrame(columns = ['id', 'keyword', 'rank'])

# 2, 3 알고리즘 동작 수행
for i, row in list_df.iterrows():
    result_list = []
    k_id = row[0] # keyword id
    k_list = row[1] # keyword list
    
    for j in range(0, len(k_list)):
        if j==0:
            result_list.append(k_list[j])
        elif len(result_list) >= 5: break
        elif check_ahead(k_list[j], result_list):
            result_list.append(k_list[j])
    
    for k in range (0, len(result_list)):
        temp = [k_id, result_list[k], k+1]
        result_df.loc[i*5 + k] = temp # i*5만큼 더해주고, 1만큼 증가함

new_df = result_df.set_index('id', drop=True, append=False, inplace=False)
new_df.to_csv('hashtag.csv', mode='w')
new_df