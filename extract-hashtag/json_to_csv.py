import pandas as pd
import json

#df = pd.DatafFrame()
with open('dict.json', 'r', encoding='utf-8') as f:
    array = json.load(f)
dict_df = pd.DataFrame.from_dict(array, orient='index')
dict_df.to_csv('dict.csv', mode='w')

keyword_df = pd.read_csv("./tf_idf_output.csv")