import vector_space
import scipy.sparse as sp
import FYPsetting

from semantic.transform.lsa import LSA
from semantic.transform.tfidf import TFIDF
from datetime import datetime
from sklearn.decomposition import TruncatedSVD, NMF


class VS_TF_SKL(vector_space.VectorSpace):

    collection_of_document_term_vectors = sp.csc_matrix([]) # should we convert it to sparse matrix?
    model = NMF(n_components=FYPsetting.LSA_DIMENSION, random_state=0)
    #model = TruncatedSVD(n_components=FYPsetting.LSA_DIMENSION, random_state=42)
    tfidf = TFIDF(collection_of_document_term_vectors)

    def __init__(self, documents = [], transforms = [TFIDF, LSA]):
        start_time = datetime.now()
        print datetime.now(), " Building base class..."
        vector_space.VectorSpace.__init__(self, documents, transforms)
        print datetime.now(), " Base class built."
        print datetime.now()-start_time
        self._make_term_doc_matrix(documents, transforms)


    def _make_term_doc_matrix(self, documents, transforms):

        start_time = datetime.now()
        print datetime.now(), " Building term-doc matrix..."
        matrix = [self._make_vector(doc) for doc in documents]
        print datetime.now(), " Term-doc matrix finished."
        matrix = sp.coo_matrix(matrix).asfptype()
        print datetime.now(), " Term-doc matrix converted to sparse matrix."
        print datetime.now() -  start_time
        print datetime.now(), " Calculating tf-idf..."
        self.tfidf = TFIDF(matrix.tocsr())
        matrix = self.tfidf.transform()
        print datetime.now(), " Doing transformation..."
        if matrix.get_shape()[0]>FYPsetting.LSA_DIMENSION:
            self.model.fit_transform(matrix)
        self.collection_of_document_term_vectors = sp.coo_matrix(matrix).tocsc()
        print datetime.now(), " Reduced tf-idf matrix converted to sparse matrix..."
        print self.collection_of_document_term_vectors.todense()
        print datetime.now(), " Tf-idf matrix built."

    def _make_vector(self, word_string):
        vector = [0] * len(self.vector_index_to_keyword_mapping)

        word_list = self.parser.tokenise_and_remove_stop_words(word_string.split(" "))

        for word in word_list:
            try:
                index = self.vector_index_to_keyword_mapping[word]
                vector[index] += 1 #Use simple Term Count Model
            except:
                pass
        return vector

    def _build_query_vector(self, term_list):
        """ convert query string into a term vector """
        query = self._make_vector(" ".join(term_list))
        return query