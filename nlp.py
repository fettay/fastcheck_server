__author__ = 'raphaelfettaya'

import spacy

NLP = spacy.load('en_core_web_sm')


def entity_recognize(sentence):
    doc = NLP(sentence)
    for entity in doc.ents:
        print(entity.text, entity.label_)


if __name__ == "__main__":
    print(entity_recognize("Is Donald really a won an Amy Award?"))


