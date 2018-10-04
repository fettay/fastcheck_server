import en_core_web_sm
from RAKE import Rake

# Load English tokenizer, tagger, parser, NER and word vectors
NLP = en_core_web_sm.load()
RAKE = Rake('stopwords.txt')


def find_entities(sentence):
    doc = NLP(sentence)

    # Find named entities, phrases and concepts

    return [entity.text for entity in doc.ents]


def extract_keywords(sentence):
    return [w for s, _ in RAKE.run(sentence) for w in s.split()]


if __name__ == '__main__':
    with open('test_sentences.txt') as f:
        sentences = f.read().split('\n')
    for sentence in sentences:
        print(sentence)
        print(find_entities(sentence))
        print(extract_keywords(sentence))