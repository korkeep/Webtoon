from ast import literal_eval
from scipy.spatial.distance import cosine
import pandas as pd
table=pd.read_csv('d2v.csv',names=['title_id','vec_str'])
table['vec'] = table.apply(lambda x: literal_eval(x['vec_str']),axis=1)
table.drop(['vec_str'], axis=1).set_index('title_id')
dist_dict={}
row_list=[]
for i in table.index:
    t_id = table.at[i, 'title_id']
    vec = table.at[i, 'vec']
    for j in table.index:
        a_t_id = table.at[j, 'title_id']
        a_vec = table.at[j, 'vec']
        if t_id!=a_t_id and (t_id,a_t_id) not in dist_dict:
            dist=cosine(vec, a_vec)
            dist_dict[(t_id,a_t_id)]=dist
            row_list.append([t_id, a_t_id, dist])
            row_list.append([a_t_id, t_id, dist])

dist_table=pd.DataFrame(row_list)
dist_table.to_csv('dist.csv')


