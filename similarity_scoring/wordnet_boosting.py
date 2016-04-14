from nltk.corpus import wordnet as wn, genesis as gw
import numpy as np
from math import exp
import nltk.collocations

class WordNet_boosting:
    '''
        A class that provides WordNet similarity funstions and Multi-word Expressions lemma
    '''
    def __init__(self):
        self.N_GRAM_NUM = 10000
        self.FILTERING_NUM = 10

    def term_similarity(self, token1, pos1, token2, pos2):
        if token1 == token2 and pos1 == pos2:
            return 1.0
        else:
            tag1 = self.get_wordnet_pos(pos1)
            tag2 = self.get_wordnet_pos(pos2)
            if [] not in (wn.synsets(token1, tag1), wn.synsets(token2, tag2)):
                # take the case where a word has multiple synsets into account
                # as said in the umbc paper, choose the largest value
                len1 = len(wn.synsets(token1, tag1))
                len2 = len(wn.synsets(token2, tag2))
                sim_mat = np.zeros((len2,len1))
                # the reason to use index here is to save time for np.matrix accessing
                # or we would have to search the index of each synset, which will cost more time
                for x in range(len1):
                    s1 = wn.synsets(token1, tag1)[x]
                    for y in range(len2):
                        s2 = wn.synsets(token2, tag2)[y]
                        if s1.shortest_path_distance(s2) == None:
                            sim_mat[y, x] = 1000000
                        else:
                            sim_mat[y, x]=s1.shortest_path_distance(s2)
                distance = sim_mat.min()
                if distance == 1000000:
                    return 0
                else:
                    return exp(-0.25*distance)
            else:
                return 0


    def get_wordnet_pos(self, tag):
        if tag[0] == 'J':
            return wn.ADJ
        elif tag[0]=='V':
            return wn.VERB
        elif tag[0]=='N':
            return wn.NOUN
        elif tag[0]=='R':
            return wn.ADV
        else:
            return ''

    def multi_words_xpn(self):
        mwes = []
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        finder = nltk.collocations.BigramCollocationFinder.from_words(gw.words('english-web.txt'))
        finder.apply_freq_filter(self.FILTERING_NUM)
        mwes.append(finder.nbest(bigram_measures.pmi, self.N_GRAM_NUM))
        trigram_measures = nltk.collocations.TrigramAssocMeasures()
        finder = nltk.collocations.TrigramCollocationFinder.from_words(gw.words('english-web.txt'))
        finder.apply_freq_filter(self.FILTERING_NUM)
        mwes.append(finder.nbest(bigram_measures.pmi, self.N_GRAM_NUM))
        return mwes