import sys

from semantic.vector_space import VectorSpace
from math import exp, log
from semantic.transform.lsa import LSA
import DBOperation
import FYPsetting

try:
	from numpy import dot
	from numpy.linalg import norm
except:
	print "Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?"
	sys.exit()

class LSAMatrix:

    """ a Class that stores the newly updated cooccurrence matrix in memory
    """

    lsa_matrix = []
    keyword_index_mapping = []

    def __init__(self, matrix):
        self.lsa_matrix = matrix

    def update(self):
        docs = DBOperation.query_corpus()
        occurrence_matrix = VectorSpace(docs, transforms = [])
        self.keyword_index_mapping = occurrence_matrix.vector_index_to_keyword_mapping
        word_num = len(self.keyword_index_mapping)
        cooccurence_matrix = [[0 for x in range(word_num)] for x in range(word_num)]

        for doc in docs:
            terms = self.keyword_index_mapping.keys()
            for term1 in terms:
                for term2 in terms:
                    index1 = self.keyword_index_mapping(term1)
                    index2 = self.keyword_index_mapping(term2)
                    if not index1 == index2:
                        for pos1 in occurrence_matrix.collection_of_document_term_lists[docs.index(doc)][index1]:
                            for pos2 in occurrence_matrix.collection_of_document_term_lists[docs.index(doc)][index2]:
                                difference = pos2 - pos1
                                if difference<FYPsetting.WINDOW_SIZE+1 or difference>-(FYPsetting.WINDOW_SIZE+1):
                                    cooccurence_matrix[term1][term2] = log(exp(cooccurence_matrix[term1][term2])+1)
                                elif difference>FYPsetting.WINDOW_SIZE:
                                    break

        self.lsa_matrix = LSA(cooccurence_matrix).transform(FYPsetting.LSA_DIMENSION)
        # the next step is to save this lsa_matrix into database

    def similarity(self, term1, term2):
        try:
            index1 = self.keyword_index_mapping(term1)
            index2 = self.keyword_index_mapping(term2)
        except:
            return 0
        return float(dot(self.lsa_matrix[index1],self.lsa_matrix[index2]) / (norm(self.lsa_matrix[index1]) * norm(self.lsa_matrix[index2])))



