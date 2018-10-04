
# coding: utf-8

# In[24]:


from nltk.chunk import conlltags2tree, tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))


# In[25]:


def extract_ent(sentense):
    
    list_of_ent = []
    ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))
    iob_tagged = tree2conlltags(ne_tree)
    
    for ent in iob_tagged:       
        if ent[1] == 'NN' or ent[1]=='NNP':
            list_of_ent.append(ent[0].capitalize())

    return list_of_ent


# In[26]:


def main():
    sentence = "gershon and John are working at checkpint."
    print (extract_ent(sentence))
    
if __name__== "__main__":
    main()

