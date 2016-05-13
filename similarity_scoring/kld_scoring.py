import os
import cPickle as pickle
import scipy.sparse as sp
from datetime import datetime
from semantic.vector_space.vs_tf_skl import VS_TF_SKL
from semantic.transform.tfidf import TFIDF
import FYPsetting
from semantic.parser import Parser
import numpy as np
import DBOperation
from sklearn.decomposition import TruncatedSVD, NMF

class KLDistance:
    tfidf_matrix = sp.csc_matrix([])
    #term_doc_matrix = []
    keyword_index_mapping = []
    model = []
    vs = TFIDF(tfidf_matrix)

    TERM_DOC_FILE = '%s/term_doc.bin' %  os.path.dirname(os.path.realpath(__file__))
    CORPUS_FILE = '%s/../../LSA_corpus' %  os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        try:
            print datetime.now(), " Loading stored term-doc matrix..."
            raise OSError
            f = open(KLDistance.LSA_MATRIX_FILE, 'rb')
            #self.term_doc_matrix = pickle.load(f)
            self.keyword_index_mapping = pickle.load(f)
            f.close()
        except:
            print datetime.now(), " Matrix does not exist, creating now..."
            lsa_corpus_io_stream = open(KLDistance.CORPUS_FILE, 'r')
            docs = lsa_corpus_io_stream.read().split("+++---+++")
            for doc in docs:
                doc = doc.replace("\n", " ")

            print datetime.now(), " Creating Vector Space..."
            self.vs = VS_TF_SKL(docs[:401])
            print datetime.now(), " Vector space created."


    def kl_divergence(self, doc1, doc2):

        parser = Parser()
        # words in terms are connected with underscore after the NLTK MWE tokenization
        # replace it with " " to make it compatible with parser here
        term_list1 = parser.tokenise_and_remove_stop_words([doc1]) # the defined argument is document_list
        term_list2 = parser.tokenise_and_remove_stop_words([doc2]) # the defined argument is document_list

        if 0 in (len(term_list1), len(term_list2)):
            return (0,0)

        index1 = -1
        index2 = -1
        index_vector1 = []
        index_vector2 = []
        length = len(self.vs.vector_index_to_keyword_mapping)


        start_time = datetime.now()
        for word1 in term_list1:
            try:
                index1 = self.vs.vector_index_to_keyword_mapping[word1]
            except:
                #print word1, ": indexing error 1"
                pass

            #print datetime.now(), " Indexing word1 completes."
            if not index1 == -1:
                index_vector1.append(index1)

        # turn vector1 into tf-idf-vector
        index_count_dict1 = {}
        for index1 in index_vector1:
            if index1 in index_count_dict1:
                index_count_dict1[index1]+=1
            else:
                index_count_dict1[index1]=1
        word_max = max(index_count_dict1, key=index_count_dict1.get)
        if word_max ==0:
            return (0,0)
        col1 = []
        for key in index_count_dict1:
            col1.append(key)
            index_count_dict1[key] = (0.5+0.5*index_count_dict1[key]/word_max)\
                                     *np.log1p(abs(self.vs.tfidf.document_total / float(self.vs.tfidf.term_doc_occur_list[key])))

        length1 = len(col1)
        col1.append(length-1)
        data1 = index_count_dict1.values()
        data1.append(0)
        row1 = [0]*(length1+1)
        term_vector1 = sp.coo_matrix((data1, (row1, col1)))
        term_vector1=self.vs.model.transform(term_vector1)
        #print datetime.now(), " Vector 1 built, cost ", datetime.now()-start_time

        start_time = datetime.now()
        for word2 in term_list2:
            try:
                index2 = self.vs.vector_index_to_keyword_mapping[word2]
            except:
                #print word2, ": indexing error 2"
                pass

            #print datetime.now(), " Indexing word2 completes."
            if not index2 == -1:
                index_vector2.append(index2)

        # turn vector2 into tf-idf-vector
        index_count_dict2 = {}
        for index2 in index_vector2:
            if index2 in index_count_dict2:
                index_count_dict2[index2]+=1
            else:
                index_count_dict2[index2]=1
        word_max = max(index_count_dict2, key=index_count_dict2.get)
        if word_max ==0:
            return (0,0)
        col2 = []
        for key in index_count_dict2:
            col2.append(key)
            index_count_dict2[key] = (0.5+0.5*index_count_dict2[key]/word_max)\
                                     *np.log1p(abs(self.vs.tfidf.document_total / float(self.vs.tfidf.term_doc_occur_list[key])))

        length2 = len(col2)
        col2.append(length-1)
        data2 = index_count_dict2.values()
        data2.append(0)
        row2 = [0]*(length2+1)
        term_vector2 = sp.coo_matrix((data2, (row2, col2)))
        term_vector2=self.vs.model.transform(term_vector2)
        #print datetime.now(), " Vector 1 built, cost ", datetime.now()-start_time

        term_vector1 = term_vector1[0]
        term_vector2 = term_vector2[0]
        #vector_m =  [a+b for a,b in zip(map(lambda x: x*0.5, term_vector1),map(lambda x: x*0.5, term_vector2))]
        result1 = 0
        result2 = 0
        for i in range(len(term_vector1)):
            if not term_vector2[i]==0:
                result1+= term_vector1[i]*np.log1p(term_vector1[i]/term_vector2[i])
            else:
                result1+= term_vector1[i]*np.log1p(term_vector1[i]/0.000001)
            if not term_vector1[i]==0:
                result2+= term_vector2[i]*np.log1p(term_vector2[i]/term_vector1[i])
            else:
                result2+= term_vector2[i]*np.log1p(term_vector2[i]/0.000001)
        return (result1,result2)


