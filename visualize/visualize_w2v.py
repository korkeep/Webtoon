# 참고 https://stackoverflow.com/questions/43776572/visualise-word2vec-generated-from-gensim
# https://programmers.co.kr/learn/courses/21/lessons/1698
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.word2vec import Word2Vec

plt.rc('font', family='Malgun Gothic') # For Windows

model_name = 'w2v.model'
model = Word2Vec.load(model_name)

vocab = list(model.wv.vocab)
X = model.wv[vocab]
print(len(vocab))

tsne = TSNE(n_components=2)

# 100개의 단어에 대해서만 시각화
X_tsne = tsne.fit_transform(X[::100, :])
fig = plt.figure()
fig.set_size_inches(40, 20)
ax = fig.add_subplot(1, 1, 1)

df = pd.DataFrame(X_tsne, index=vocab[::100], columns=['x', 'y'])

ax.scatter(df['x'], df['y'])
for word, pos in df.iterrows():
    ax.annotate(word, pos, fontsize=10)
plt.show()
