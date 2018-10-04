
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.stem.porter import *
import nltk
import gensim
from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
w2v = gensim.models.KeyedVectors.load_word2vec_format(r'C:\Users\gersh\Google Drive\iPython_notebooks\Try\FakeFact\GoogleNews-vectors-negative300.bin',binary=True)
#w2v = gensim.models.KeyedVectors.load_word2vec_format(r'C:\Users\gersh\Google Drive\iPython_notebooks\Try\Datahack_2018\fastcheck_server\glove.6B.50d.txt')
def extract_ent(str):
    list_of_ent = []
    ne_tree = ne_chunk(pos_tag(word_tokenize(str)))
    iob_tagged = tree2conlltags(ne_tree)
    
    for ent in iob_tagged:       
        if ent[1] == 'NN' or ent[1]=='NNP':
            list_of_ent.append(ent[0].capitalize())
    return list_of_ent

def stemmer(word):
    pstemmer = PorterStemmer()
    return pstemmer.stem(word)

def similar_w2v(word):
    similar_words= w2v.most_similar(word, topn=5)
    return similar_words
    

def main():
    sentence = "George Cloony and John and Yossi, nomination Rafael are working at checkpoint."
    print (extract_ent(sentence))
    for keyword in extract_ent(sentence):
        print (stemmer(keyword))
    print (similar_w2v('oscar'))
    print (similar_w2v('nobel'))
    print (similar_w2v('hackathon'))
    print (similar_w2v('data'))



if __name__== "__main__":
    main()
