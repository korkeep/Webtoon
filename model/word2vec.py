import json
from soynlp.utils import DoublespaceLineCorpus
from soynlp.tokenizer import MaxScoreTokenizer
from gensim.models.word2vec import Word2Vec


def vectorize(corpus_filename='sentences.txt', score_filename='scores.json'):
    with open(score_filename, 'r', encoding='utf-8') as score_dict:
        scores = json.load(score_dict)
    corpus = DoublespaceLineCorpus(corpus_filename, iter_sent=True)
    tokenizer = MaxScoreTokenizer(scores=scores)
    sentences = [tokenizer(s) for s in corpus]
    model = Word2Vec(sentences)
    model.init_sims(replace=True)
    model.save('w2v.model')
    model.wv.save('w2v.wv')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Vectorize words and save them.")
    parser.add_argument('corpus', type=str, default='../preparation/filtered_best_comments_hangul_corpus.txt',
                        help='filename of corpus')
    parser.add_argument('scores', type=str, default='../preparation/scores.json', help='filename of scores')
    args = parser.parse_args()
    vectorize(args.corpus, args.scores)
