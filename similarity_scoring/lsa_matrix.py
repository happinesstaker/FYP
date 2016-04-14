import sys
import os
import cPickle as pickle
import scipy.sparse as sp

from semantic.vector_space.vs_co import VS_Co
from math import exp, log
from semantic.transform.lsa import LSA
from semantic.parser import Parser
#import DBOperation
import FYPsetting
from datetime import datetime

try:
	import numpy as np
except:
	print "Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?"
	sys.exit()

class LSAMatrix:

    """ a Class that stores the newly updated cooccurrence matrix in memory
    """
    DATA_PATH = "/Volumes/FAT/FYP_data" #os.path.dirname(os.path.realpath(__file__))
    LSA_CORPUS_FILE = '%s/../../LSA_corpus' %  os.path.dirname(os.path.realpath(__file__))
    LSA_MATRIX_FILE = '%s/LSA_matrix' %  DATA_PATH
    TERM_DOC_FILE_BIN = '%s/term_doc.bin' %  DATA_PATH
    TERM_DOC_FILE = '%s/term_doc.txt' %  DATA_PATH
    WORD_LIST_FILE = '%s/word_list.txt' %  DATA_PATH
    lsa_matrix = sp.csc_matrix
    keyword_index_mapping = []

    def __init__(self, matrix, mapping):
        self.lsa_matrix = matrix
        self.keyword_index_mapping = mapping

    def update(self):
        try:
            print datetime.now(), " Try loading stored matrices..."
            raise OSError
            #start_time = datetime.now()
            f = open(LSAMatrix.LSA_MATRIX_FILE, 'rb')
            self.lsa_matrix = pickle.load(f)
            self.keyword_index_mapping = pickle.load(f)
            f.close()
            print datetime.now()-start_time
        except:
            print datetime.now(), " Matrix does not exist, creating now..."
            o_time = datetime.now()
            lsa_corpus_io_stream = open(LSAMatrix.LSA_CORPUS_FILE, 'r')
            docs = lsa_corpus_io_stream.read().split("+++---+++")
            for doc in docs:
                doc = doc.replace("\n", " ")
            print datetime.now(), (" There are %d docs"% len(docs))
            #print docs[74]
            #exit(0)
            start_time = datetime.now()
            #print "Building occurrence_matrix..."
            start_time = datetime.now()
            print datetime.now(), " Creating Vector Space..."
            vs = VS_Co(docs[:1001], transforms = [])
            #del docs
            print datetime.now(), " Vector Space created"
            print datetime.now() - start_time
            '''
            print "Occurrence_matrix built."
            print datetime.now()-start_time
            #print occurrence_matrix.collection_of_document_term_vectors
            #print occurrence_matrix.collection_of_document_term_lists

            # save occurrence_matrix into TERM_DOC_FILE
            start_time = datetime.now()
            #with open(LSAMatrix.TERM_DOC_FILE_BIN, 'wb') as f1:
                #pickle.dump(occurrence_matrix.collection_of_document_term_vectors, f1)
                #pickle.dump(occurrence_matrix.vector_index_to_keyword_mapping, f)
            with open(LSAMatrix.WORD_LIST_FILE, 'wb') as f2:
                for doc_word_list in vs.word_index_list_of_docs:

                    f2.write("".join(str(doc_word_list)))
                    f2.write("\n---+++---\n")
            print "Occurrence Matrix saved."
            print datetime.now()-start_time
            exit(0)
            '''

            start_time = datetime.now()
            print datetime.now(), " Building co-occurrence_matrix..."

            self.keyword_index_mapping = vs.vector_index_to_keyword_mapping
            print datetime.now(), "   Saved keyword index map. "
            word_num = len(self.keyword_index_mapping)
            print datetime.now(), "   Counted word numbers. "
            cooccurence_matrix = [[0 for x in range(word_num)] for x in range(word_num)]
            print datetime.now(), "   Co-occurrence matrix initialized. "

            # comment out and change to the new version
            '''
            #for doc in docs:
            for doc in docs:
                terms = self.keyword_index_mapping.keys()
                for term1 in terms:
                    for term2 in terms:
                        index1 = self.keyword_index_mapping[term1]
                        index2 = self.keyword_index_mapping[term2]
                        if not term1 == term2:
                            if(occurrence_matrix.collection_of_document_term_dicts[docs.index(doc)].has_key(term1)
                                   *occurrence_matrix.collection_of_document_term_dicts[docs.index(doc)].has_key(term2)):
                                for pos1 in occurrence_matrix.collection_of_document_term_dicts[docs.index(doc)][term1]:
                                    for pos2 in occurrence_matrix.collection_of_document_term_dicts[docs.index(doc)][term2]:
                                        difference = pos2 - pos1
                                        if difference<FYPsetting.WINDOW_SIZE+1 or difference>-(FYPsetting.WINDOW_SIZE+1):
                                            if cooccurence_matrix[index1][index2]==0:
                                                cooccurence_matrix[index1][index2] = log(2)
                                            else:
                                                cooccurence_matrix[index1][index2] = log(exp(cooccurence_matrix[index1][index2])+1)
                                        elif difference>FYPsetting.WINDOW_SIZE:
                                            break
            '''

            for doc_index in range(1001):#range(len(docs)):
                if doc_index%10000 == 0:
                    print datetime.now(), " doc", doc_index
                word_index_list = vs.word_index_list_of_docs[doc_index]
                #print word_index_list
                length = len(word_index_list)
                if length>3:
                    self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[0],word_index_list[1])
                    self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[0],word_index_list[2])
                    self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[0],word_index_list[3])
                    self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[1],word_index_list[2])
                    self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[2],word_index_list[3])
                    for i in range(1, length-3):
                        self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[i],word_index_list[i+3])
                        self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[i+1],word_index_list[i+3])
                        self.__update_cooccurrence_mat__(cooccurence_matrix, word_index_list[i+2],word_index_list[i+3])


            print datetime.now(), " Co-occurrence_matrix built.", len(cooccurence_matrix), len(cooccurence_matrix)
            print datetime.now()-start_time
            #print cooccurence_matrix[0]

            print datetime.now(), " Converting co-occurrence_matrix to float point sparse matrix..."
            start_time = datetime.now()
            cooccurence_matrix = sp.coo_matrix(cooccurence_matrix)
            cooccurence_matrix = cooccurence_matrix.asfptype()
            print datetime.now(), " Sparse matrix built."

            start_time = datetime.now()
            print datetime.now(), " Normalizing co-occurrence_matrix... "
            '''
            for x in range(word_num):
                for y in range(word_num):
                    cooccurence_matrix[x][y] = log(1+cooccurence_matrix[x][y])
            print "Normalization finished. "
            '''
            cooccurence_matrix.log1p()
            print datetime.now()-start_time

            # then we do SVD to reduce the dimension

            print datetime.now(), " Doing SVD..."
            start_time = datetime.now()
            cooccurence_matrix = LSA(cooccurence_matrix).transform(FYPsetting.LSA_DIMENSION)
            # COO_Matrix is easier to construct, CSC_Matrix is easier to access columns.
            # this conversion is for future use.
            # We should compare the time of constructing csc_matrix directly and constructing coo and then do this conversion
            self.lsa_matrix = sp.coo_matrix(cooccurence_matrix).tocsc()
            print datetime.now(), " SVD finished."
            print datetime.now()-start_time

            print datetime.now(), " Total time cost: ", datetime.now()-o_time

            '''
            # the next step is to save this lsa_matrix and keyword index mapping into database
            start_time = datetime.now()
            print "Saving matrix..."
            with open(LSAMatrix.LSA_MATRIX_FILE, 'wb') as f:
                #pickle.dump(self.lsa_matrix, f)
                #pickle.dump(self.keyword_index_mapping, f)
                f.write(str(cooccurence_matrix))
            print "Matrix saved."
            print datetime.now()-start_time
            '''


    def __update_cooccurrence_mat__(self, cooccurence_matrix ,index1, index2):
        if not index1==index2:
            cooccurence_matrix[index1][index2]+=1
            cooccurence_matrix[index2][index1]+=1

    def similarity(self, term1, term2):
        # stem and remove stop words in two terms first to make them compatible with those stored
        parser = Parser()
        term1 = parser.tokenise(term1)# after tokenization, it is a list
        if term1==[]:
            return 0
        else:
            term1 = parser.tokenise(term1[0])
        term2 = parser.tokenise(term2)
        if term2==[]:
            return 0
        else:
            term2 = parser.tokenise(term2[0])
        try:
            index1 = self.keyword_index_mapping[term1[0]]
        except:
            print term1, ": indexing error 1"
            return 0
        try:
            index2 = self.keyword_index_mapping[term2[0]]
        except:
            print term2, "indexing error 2"
            return 0
        return float(np.dot(self.lsa_matrix[index1],self.lsa_matrix[index2]) /
                     (np.linalg.norm(self.lsa_matrix[index1]) * np.linalg.norm(self.lsa_matrix[index2])))

    def term_similarity(self, term1, term2):
        '''
        Take in two terms and calculate their similarity through vector combination
        :param term1:
        :param term2:
        :return:
        '''
        parser = Parser()
        # words in terms are connected with underscore after the NLTK MWE tokenization
        # replace it with " " to make it compatible with parser here
        str(term1).replace("_", " ")
        str(term2).replace("_", " ")

        term_list1 = parser.tokenise_and_remove_stop_words([term1]) # the defined argument is document_list
        term_list2 = parser.tokenise_and_remove_stop_words([term2]) # the defined argument is document_list
        term_vector1 = []
        term_vector2 = []
        index1 = -1
        index2 = -1

        start_time = datetime.now()
        for word1 in term_list1:
            try:
                index1 = self.keyword_index_mapping[word1]
            except:
                #print word1, ": indexing error 1"
                pass

            #print datetime.now(), " Indexing word1 completes."
            if not index1 == -1:
                if term_vector1 ==[]:
                    term_vector1 = self.lsa_matrix.getcol(index1).toarray().flatten()#to ndarray > become (X, 1) > flatten
                else:
                    term_vector1 = term_vector1+self.lsa_matrix.getcol(index1).toarray().flatten()#[index1]
        #print datetime.now(), " Vector 1 built, cost ", datetime.now()-start_time

        start_time = datetime.now()
        for word2 in term_list2:
            try:
                index2 = self.keyword_index_mapping[word2]
            except:
                #print word2, ": indexing error 2"
                pass

            #print datetime.now(), " Indexing word2 completes."
            if not index2 == -1:
                if term_vector2 ==[]:
                    term_vector2 = self.lsa_matrix.getcol(index2).toarray().flatten()#[index2]
                else:
                    term_vector2 = term_vector1+self.lsa_matrix.getcol(index2).toarray().flatten()#[index2]
        #print datetime.now(), " Vector 2 built, cost ", datetime.now()-start_time

        if 1 not in (term_vector1==[], term_vector2==[]):
        #http://stackoverflow.com/questions/1075652/using-the-and-and-not-operator-in-python
            return float(np.dot(term_vector1,term_vector2) /
                     (np.linalg.norm(term_vector1) * np.linalg.norm(term_vector2)))
        else:
            return 0

if __name__ == "__main__":
    print np.__config__.show()
    print "======================================================"
    lsa = LSAMatrix(0, 0)
    lsa.update()
    #print "The similarity between silicon and valley is: ", lsa.similarity("silicon","valley")
    start_time = datetime.now()
    print "Calculating the similarity...\n", lsa.term_similarity("silicon","valley")
    print "Similarity calculation cost: ", datetime.now()-start_time
    #print lsa.lsa_matrix