import argparse
from gensim.models.word2vec import Word2Vec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word2Vector demonstration")
    parser.add_argument('positive', nargs='+', action='extend')
    parser.add_argument('-n', '--neg', nargs='*', action='extend')
    args = parser.parse_args()
    print(args.positive, args.neg)
    model = Word2Vec.load('w2v.model')
    try:
        print(model.wv.most_similar(
            positive=args.positive[0] if len(args.positive) <= 1 and args.neg is None else args.positive,
            negative=args.neg, topn=5))
    except KeyError as e:
        print("없는 단어입니다!", e)
