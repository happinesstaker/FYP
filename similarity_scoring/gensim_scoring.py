import os
from gensim import corpora, models, similarities
from semantic.parser import Parser
from datetime import datetime

CORPUS_FILE = '%s/../../LSA_corpus' %  os.path.dirname(os.path.realpath(__file__))
parser = Parser()
def parse_and_clean_doc(document_list):
	""" create the keyword associated to the position of the elements within the document vectors """
	print datetime.now(), "  Tokenizing documents..."
	return [parser.tokenise_and_remove_stop_words(document) for document in document_list]


if __name__ == "__main__":
    '''
    lsa_corpus_io_stream = open(CORPUS_FILE, 'r')
    docs = lsa_corpus_io_stream.read().split("+++---+++")
    for doc in docs:
        doc = doc.replace("\n", " ")
        doc = unicode(doc, errors='ignore')
    '''

    word_lists = [['human', 'machine', 'interface', 'lab', 'abc', 'computer', 'applications'], ['survey', 'user', 'opinion', 'computer', 'system', 'response', 'time'], ['eps', 'user', 'interface', 'management', 'system'], ['graph', 'minors', 'iv', 'widths', 'trees', 'well', 'quasi', 'ordering'], ['graph', 'minors', 'survey']]#parse_and_clean_doc(docs[:1001])
    print datetime.now(), "  Tokenization finished."
    dictionary = corpora.Dictionary(word_lists)
    corpus = [dictionary.doc2bow(word_list) for word_list in word_lists]
    print corpus