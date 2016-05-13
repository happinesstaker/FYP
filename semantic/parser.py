import os
from semantic.porter_stemmer import PorterStemmer
import os
import re

class Parser:
    STOP_WORDS_FILE = '%s/english.stop' %  os.path.dirname(os.path.realpath(__file__))

    stemmer = None
    stopwords = []

    def __init__(self, stopwords_io_stream = None):
		self.stemmer = PorterStemmer()

		if(not stopwords_io_stream):
			stopwords_io_stream = open(Parser.STOP_WORDS_FILE, 'r')

		self.stopwords = stopwords_io_stream.read().split()

    def tokenise_and_remove_stop_words(self, document_list):
		if not document_list:
			return []

		vocabulary_string = " ".join(document_list)

		tokenised_vocabulary_list = self.tokenise(vocabulary_string)
		clean_word_list = self._remove_stop_words(tokenised_vocabulary_list)
		return clean_word_list

    def _remove_stop_words(self, list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


    def tokenise(self, string):
		""" break string up into tokens and stem words """
		string = self._clean(string)
		words = string.split(" ")
		return [self.stemmer.stem(word, 0, len(word)-1) for word in words]

    def _clean(self, string):
		""" remove any nasty grammar tokens from string """
		#string = string.encode('latin-1', 'ignore')
		string = string.lstrip()
		string = string.rstrip()
		string = string.replace("\'", " ") #xxx's
		string = string.replace("\"", "")
		string = string.replace(".","")
		string = string.replace("!","")
		string = string.replace(",","")
		string = string.replace("?","")
		string = string.replace(":","")
		string = string.replace("<","")
		string = string.replace(">","")
		string = string.replace(";","")
		string = string.replace("[","")
		string = string.replace("]","")
		string = string.replace("{","")
		string = string.replace("}","")
		string = string.replace("(","")
		string = string.replace(")","")
		string = string.replace("-", "_")
		string = string.replace("\\", "")
		string = string.replace("\s+"," ")
		string = string.replace("\t", " ")
		string = string.replace("\n", " ")
		string = string.replace("\r", " ")
		string = string.lower()
		string = re.sub(' +',' ',string) # remove unwanted whitespace
		return string