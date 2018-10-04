
import nltk
from nltk.chunk import tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def extract_ent(sentence):
    
    list_of_ent = []
    ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))
    iob_tagged = tree2conlltags(ne_tree)
    
    for ent in iob_tagged:       
        if ent[1] == 'NN' or ent[1]=='NNP':
            list_of_ent.append(ent[0].capitalize())

    return list_of_ent


# In[26]:


def main():
    sentence = "did george clooney won academy awards?"
    print(extract_ent(sentence))
    
if __name__ == "__main__":
    main()

