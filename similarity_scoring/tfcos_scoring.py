import os
import cPickle as pickle
import scipy.sparse as sp
from datetime import datetime
from semantic.vector_space.vs_tf import VS_TF
from semantic.transform.tfidf import TFIDF
from semantic.transform.lsa import LSA
import FYPsetting
from semantic.parser import Parser
import numpy as np
from sklearn.decomposition import TruncatedSVD, NMF

class TfSim:
    tfidf_matrix = sp.csc_matrix([])
    #term_doc_matrix = []
    keyword_index_mapping = []

    TERM_DOC_FILE = '%s/term_doc.bin' %  os.path.dirname(os.path.realpath(__file__))
    CORPUS_FILE = '%s/../../LSA_corpus' %  os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        try:
            print datetime.now(), " Loading stored term-doc matrix..."
            raise OSError
            f = open(TfSim.LSA_MATRIX_FILE, 'rb')
            #self.term_doc_matrix = pickle.load(f)
            self.keyword_index_mapping = pickle.load(f)
            f.close()
        except:
            print datetime.now(), " Matrix does not exist, creating now..."
            lsa_corpus_io_stream = open(TfSim.CORPUS_FILE, 'r')
            docs = lsa_corpus_io_stream.read().split("+++---+++")
            for doc in docs:
                doc = doc.replace("\n", " ")

            print datetime.now(), " Creating Vector Space..."
            vs = VS_TF(docs[:301])
            print datetime.now(), " Vector space created."

            #print occurrence_matrix.collection_of_document_term_vectors
            #print occurrence_matrix.collection_of_document_term_lists

            '''
            # save occurrence_matrix into TERM_DOC_FILE
            start_time = datetime.now()
            with open(KLDistance.TERM_DOC_FILE, 'wb') as f:
                pickle.dump(occurrence_matrix.collection_of_document_term_vectors, f)
                pickle.dump(occurrence_matrix.vector_index_to_keyword_mapping, f)
            print "Occurrence Matrix saved."
            print datetime.now()-start_time
            '''

            #self.term_doc_matrix = occurrence_matrix.collection_of_document_term_vectors
            self.keyword_index_mapping = vs.vector_index_to_keyword_mapping
            self.tfidf_matrix = vs.collection_of_document_term_vectors

        #self.tfidf_matrix = TFIDF(self.term_doc_matrix).transform()
        #self.tfidf_matrix = LSA(self.tfidf_matrix).transform(FYPsetting.LSA_DIMENSION)

    def cos_similarity(self, doc1, doc2):

        parser = Parser()
        # words in terms are connected with underscore after the NLTK MWE tokenization
        # replace it with " " to make it compatible with parser here

        term_list1 = parser.tokenise_and_remove_stop_words([doc1]) # the defined argument is document_list
        term_list2 = parser.tokenise_and_remove_stop_words([doc2]) # the defined argument is document_list
        term_vector1 = []
        term_vector2 = []
        index1 = -1
        index2 = -1

        start_time = datetime.now()
        for word1 in term_list1:
            try:
                index1 = self.keyword_index_mapping[word1]
            except:
                print word1, ": indexing error 1"

            print datetime.now(), " Indexing word1 completes."
            if not index1 == -1:
                if term_vector1 ==[]:
                    term_vector1 = self.tfidf_matrix.getcol(index1).toarray().flatten()#to ndarray > become (X, 1) > flatten
                else:
                    term_vector1 = term_vector1+self.tfidf_matrix.getcol(index1).toarray().flatten()#[index1]
        print datetime.now(), " Vector 1 built, cost ", datetime.now()-start_time
        print term_vector1

        start_time = datetime.now()
        for word2 in term_list2:
            try:
                index2 = self.keyword_index_mapping[word2]
            except:
                print word2, ": indexing error 2"

            print datetime.now(), " Indexing word2 completes."
            if not index2 == -1:
                if term_vector2 ==[]:
                    term_vector2 = self.tfidf_matrix.getcol(index2).toarray().flatten()#[index2]
                else:
                    term_vector2 = term_vector1+self.tfidf_matrix.getcol(index2).toarray().flatten()#[index2]
        print datetime.now(), " Vector 2 built, cost ", datetime.now()-start_time
        print term_vector2

        if 1 not in (term_vector1==[], term_vector2==[]):
        #http://stackoverflow.com/questions/1075652/using-the-and-and-not-operator-in-python
            print "dot: ",np.dot(term_vector1,term_vector2)
            print "mod 1: ", np.linalg.norm(term_vector1)
            print "mod 2: ", np.linalg.norm(term_vector2)
            return float(np.dot(term_vector1,term_vector2) /
                     (np.linalg.norm(term_vector1) * np.linalg.norm(term_vector2)))
        else:
            return 0



if __name__ == "__main__":
    start_time = datetime.now()
    tfs = TfSim()
    print "Total time cost: ", datetime.now()-start_time
    print tfs.cos_similarity("silicon valley", "Lacob bugs")