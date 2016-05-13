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
    LSA_CORPUS_FILE1 = '%s/../evaluation/msr_paraphrase_train.txt' %  os.path.dirname(os.path.realpath(__file__))
    LSA_MATRIX_FILE = '%s/LSA_matrix' %  DATA_PATH
    TERM_DOC_FILE_BIN = '%s/term_doc.bin' %  DATA_PATH
    TERM_DOC_FILE = '%s/term_doc.txt' %  DATA_PATH
    WORD_LIST_FILE = '%s/word_list.txt' %  DATA_PATH
    lsa_matrix = sp.csc_matrix
    keyword_index_mapping = []

    def __init__(self, matrix, mapping):
        self.lsa_matrix = matrix
        self.keyword_index_mapping = mapping
        self.update()

    def update(self):
        try:
            #print datetime.now(), " Try loading stored matrices..."
            raise OSError
            #start_time = datetime.now()
            f = open(LSAMatrix.LSA_MATRIX_FILE, 'rb')
            self.lsa_matrix = pickle.load(f)
            self.keyword_index_mapping = pickle.load(f)
            f.close()
            #print datetime.now()-start_time
        except:
            #print datetime.now(), " Matrix does not exist, creating now..."
            o_time = datetime.now()

            docs = []
            with open(LSAMatrix.LSA_CORPUS_FILE1, 'r') as corp:
                line = corp.readline()
                line = corp.readline()
                while line:
                    content = line.split("\t")
                    docs.append(content[3])
                    docs.append(content[4])
                    line = corp.readline()

            #print datetime.now(), (" There are %d docs"% len(docs))
            #print docs[74]
            #exit(0)
            start_time = datetime.now()
            #print "Building occurrence_matrix..."
            start_time = datetime.now()
            print datetime.now(), " Creating Vector Space..."
            vs = VS_Co(docs, transforms = [])
            #del docs
            print datetime.now(), " Vector Space created"
            print datetime.now() - start_time

            start_time = datetime.now()
            print datetime.now(), " Building co-occurrence_matrix..."

            self.keyword_index_mapping = vs.vector_index_to_keyword_mapping
            print datetime.now(), "   Saved keyword index map. "
            word_num = len(self.keyword_index_mapping)
            print datetime.now(), "   Counted word numbers. "
            cooccurence_matrix = [[0 for x in range(word_num)] for x in range(word_num)]
            print datetime.now(), "   Co-occurrence matrix initialized. "

            for doc_index in range(len(docs)):
                #if doc_index%10000 == 0:
                    #print datetime.now(), " doc", doc_index
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
            #print datetime.now(), " Sparse matrix built."

            start_time = datetime.now()
            print datetime.now(), " Normalizing co-occurrence_matrix... "
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
            #print "Saving matrix..."
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
        term1 = str(term1).replace("_", " ")
        term2 = str(term2).replace("_", " ")
        term1 = str(term1).replace("-", " ")
        term2 = str(term2).replace("-", " ")

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

