__author__ = 'raphaelfettaya'

from basic_NER import extract_keywords, find_entities
from wikisearch import search_entity


class ExtractionError(Exception):
    pass


def upper_case(s):
    """
    upper case first letter of all words
    """
    return " ".join([w[0].upper() + w[1:] for w in s.split(" ")])


def answer(sentence):
    keywords = extract_keywords(sentence)
    entities = find_entities(sentence)
    if len(entities) == 0:
        entities = find_entities(upper_case(sentence))
        if len(entities) == 0:
            raise ExtractionError()
    entity = entities[0]
    for s in entity.split():
        if s.lower() in keywords:
            keywords.remove(s.lower())
    result = search_entity(entity, keywords)
    return str(result)

if __name__ == '__main__':
    # with open('test_sentences.txt') as f:
    #    sentences = f.read().split('\n')
    # for (sentence, label) in sentences:
    #     print(sentence)
    #     try:
    #         print(answer(sentence))
    #     except ExtractionError:
    #         print('Cannot answer')

    from test_set import test_set
    tp = fp = tn = fn = 0
    for (sentance, label) in test_set:
        print(sentance)
        try:
            ans = answer(sentance)
            print(ans, "Correct" if ans == str(label) else "Wrong")
            if ans == str(label):
                if ans:
                    tp += 1
                else:
                    fp += 1
            elif label:
                fn += 1
            else:
                tn += 1

        except ExtractionError:
            print('Cannot answer')

    print(tp, " ", fp, "\n", fn, " ", tn)