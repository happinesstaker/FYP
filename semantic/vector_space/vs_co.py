import vector_space
from semantic.transform.lsa import LSA
from datetime import datetime

class VS_Co(vector_space.VectorSpace):

    word_index_list_of_docs = []

    def __init__(self, documents = [], transforms = [LSA]):
        #print datetime.now(), " Initializing base class..."
        start_time = datetime.now()
        vector_space.VectorSpace.__init__(self, documents, transforms)
        #print datetime.now(), " Base class initialized"
        #print datetime.now() - start_time
        self._make_word_index_list(documents)

    def _make_word_index_list(self, docs):
        i = 0
        for doc in docs:
            word_list = self.parser.tokenise_and_remove_stop_words(doc.split(" "))
            index_list = []
            for word in word_list:
                try:
                    index_list.append(self.vector_index_to_keyword_mapping[word])
                except:
                    pass
            self.word_index_list_of_docs.append(index_list)
            i+=1