from soynlp.utils import DoublespaceLineCorpus
from soynlp.word import WordExtractor
import sys
import json
import heapq
import numpy as np


def preprocess(filename):
    sentences = DoublespaceLineCorpus(filename, iter_sent=True)

    word_extractor = WordExtractor(min_frequency=30,
                                   min_cohesion_forward=0.05,
                                   min_right_branching_entropy=0.01
                                   )

    word_extractor.train(sentences)  # list of str or like
    extract = word_extractor.extract()
    words = []
    word_dict = {}
    frequencies = []
    for k in extract:
        if len(k) < 2:
            continue
        v = extract[k]
        score = v.cohesion_forward * v.right_branching_entropy
        word_dict[k] = score
        heapq.heappush(words, (-score, k))
        frequencies.append(v.leftside_frequency)

    with open(f'{filename}.words', 'w', encoding='utf-8') as out:
        while len(words) > 0:
            priority, w = heapq.heappop(words)
            out.write(w + "\n")

    with open(f'{filename}_scores.json', 'w', encoding='utf-8') as dict_out:
        json.dump(word_dict, dict_out, ensure_ascii=False)

    frequency_array = np.array(frequencies)
    frequency_mean = frequency_array.mean()
    print(f"Mean: {frequency_mean}, Std: {np.sqrt(np.mean((frequency_array - frequency_mean) ** 2))},\
     Median: {np.median(frequency_array)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        preprocess(sys.argv[1])
    else:
        print("Usage: words.py [filename with extension]")
    print("Done.")
