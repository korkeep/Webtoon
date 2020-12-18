import pandas as pd

keyword_df = pd.read_csv("./tf_idf_output.csv")
name_df = pd.read_csv("./dict.csv")

result_df = pd.merge(keyword_df, name_df, how='left', on='index')

#['index', 'name', 'keyword', 'result', 'rank']
cols = result_df.columns.tolist()
tmp = cols[4]
del cols[4]
cols.insert(1, tmp)
result_df = result_df[cols]

result_df.to_csv('search_output.csv', mode='w')