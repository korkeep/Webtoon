from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

wv = KeyedVectors.load("w2v.wv")#, mmap='r')
wv_list =[(k, wv[k]) for k in wv.vocab]
df = pd.DataFrame(wv_list, columns=['token', 'vector'])
table = pa.Table.from_pandas(df)
print(table.schema)
pq.write_table(table, 'w2v.parquet')
