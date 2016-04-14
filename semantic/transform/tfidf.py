from math import *
from semantic.transform.transform import Transform
from datetime import datetime
import scipy.sparse as sp

class TFIDF(Transform):

    def __init__(self, matrix):
        Transform.__init__(self, matrix)
        self.document_total, self.word_num  = self.matrix.get_shape()
        self.nonzero_rows, self.nonzero_cols = self.matrix.nonzero()
        self.matrix = self.matrix.todense()
        # A list to store the number of occurrence for a term in all docs
        self.term_doc_occur_list = [0]*self.word_num
        for col in self.nonzero_cols:
            self.term_doc_occur_list[col]+=1


    def transform(self):
        """ Apply TermFrequency(tf)*inverseDocumentFrequency(idf) for each matrix element.
        This evaluates how important a word is to a document in a corpus
        With a document-term matrix: matrix[x][y]
        tf[x][y] = frequency of term y in document x / frequency of all terms in document x
        idf[x][y] = log( abs(total number of documents in corpus) / abs(number of documents with term y)  )
        Note: This is not the only way to calculate tf*idf
        """
        print datetime.now(), "   TF-IDF transform called. "

        rows,cols = self.matrix.shape
        transformed_matrix = self.matrix.copy()

        word_max_for_doc = [self.matrix[row].max() for row in range(rows)]

        for i in range(len(self.nonzero_rows)):
            row = self.nonzero_rows[i]
            col = self.nonzero_cols[i]
            word_max = word_max_for_doc[row]

            if not word_max == 0:
                term_frequency = 0.5 + 0.5*self.matrix[row, col] / float(word_max)
            else:
                term_frequency = 0.5
            inverse_document_frequency = log1p(abs(self.document_total / float(self.term_doc_occur_list[col])))
            transformed_matrix[row,col] = term_frequency * inverse_document_frequency
        return sp.coo_matrix(transformed_matrix)

        # version without handling sparseness
        for row in xrange(0, rows): #For each document

            word_max = self.matrix[row].max()#reduce(lambda x, y: x+y, self.matrix[row] )
            print datetime.now(), "   word_max is ", word_max
            for col in xrange(0, cols): #For each term
                transformed_matrix[row,col] = float(transformed_matrix[row,col])

                if transformed_matrix[row, col] != 0:
                    if not word_max ==0:
                        term_frequency = 0.5 + 0.5*self.matrix[row, col] / float(word_max)
                    else:
                        term_frequency = 0.5
                    inverse_document_frequency = log(abs(self.document_total / float(self._get_term_document_occurences(col))))
                    transformed_matrix[row,col] = term_frequency * inverse_document_frequency
                #print transformed_matrix
        return sp.coo_matrix(transformed_matrix)


    #def _tf_idf(self, row, col, word_max, ):

     #   return


    def _get_term_document_occurences(self, col):
        """ Find how many documents a term occurs in"""

        term_document_occurrences = 0

        rows, cols = self.matrix.shape

        for n in xrange(0,rows):
            if self.matrix[n, col] > 0: #Term appears in document
                term_document_occurrences +=1
        return term_document_occurrences