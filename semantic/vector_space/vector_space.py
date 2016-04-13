import sys
from semantic.parser import Parser
import re

try:
	import numpy
except:
	print "Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?"
	sys.exit()

class VectorSpace:
	""" A algebraic model for representing text documents as vectors of identifiers.
    A document is represented as a vector. Each dimension of the vector corresponds to a
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """
	vector_index_to_keyword_mapping = {}


	parser = None

	def __init__(self, documents = [], transforms = []):
		self.parser = Parser()
		#self._doc_preprocess(documents)
		if len(documents) > 0:
				self._build(documents, transforms)

	def _doc_preprocess(self, docs):
		print "previous", len(docs)
		docs = map(self.parser._clean, docs)
		docs = filter(lambda x: x == '' or ' ', docs)
		print "now", len(docs)


	def _build(self, documents, transforms):
		""" Create the vector space for the passed document strings without duplicate words"""
		self.vector_index_to_keyword_mapping = self._get_vector_keyword_index(documents)

		# comment out for the class splitting, moved downward to vs_tf
		#matrix = [self._make_vector(document) for document in documents]
		#matrix = reduce(lambda matrix,transform: transform(matrix).transform(), transforms, matrix)
		#self.collection_of_document_term_vectors = matrix

		# comment out for the algorithm modification
		#matrix2 = [self._make_dict(document) for document in documents]
		#matrix2 = [self._make_dict(word_list) for word_list in self.word_list_of_docs]
		#self.collection_of_document_term_dicts = matrix2


	def _get_vector_keyword_index(self, document_list):
		""" create the keyword associated to the position of the elements within the document vectors """
		vocabulary_list = self.parser.tokenise_and_remove_stop_words(document_list)
		unique_vocabulary_list = self._remove_duplicates(vocabulary_list)
		vector_index={}
		offset=0
		#Associate a position with the keywords which maps to the dimension on the vector used to represent this word
		for word in unique_vocabulary_list:
			vector_index[word] = offset
			offset += 1
		return vector_index  #(keyword:position)


	# comment out for the class splitting
	'''
	def _make_vector(self, word_string):
		""" @pre: unique(vectorIndex) """

		vector = [0] * len(self.vector_index_to_keyword_mapping)

		word_list = self.parser.tokenise_and_remove_stop_words(word_string.split(" "))

		index_list = []
		for word in word_list:
			vector[self.vector_index_to_keyword_mapping[word]] += 1 #Use simple Term Count Model
			#index_list.append(self.vector_index_to_keyword_mapping[word])
		#self.word_index_list_of_docs.append(index_list)
		return vector
	'''
	'''
	def _make_list(self, word_string):
		""" make an array of list of the index of each term in each document"""
		vector = [[]] * len(self.vector_index_to_keyword_mapping)
		print 'vector', vector

		word_list = self.parser.tokenise_and_remove_stop_words(word_string.split(" "))

		counter = 0
		for word in word_list:
			i = self.vector_index_to_keyword_mapping[word]
			if vector[3] == []:
				print word, 'has index', 3
				(vector[3]).append(counter)
				print vector[3]
				print 'vector', vector
				exit(0)
			else:
				print word, 'has index', self.vector_index_to_keyword_mapping[word]
				list = vector[i]
				print list
				list.append(counter)
				print vector[i]
				print 'vector', vector
			counter += 1
		print vector
		return vector
	'''

	# As _make_vector has been modified and the word_list for each doc is stored,
	# there is no need to rebuild these lists again.
	'''
	def _make_dict(self, word_string):
		""" make an array of list of the index of each term in each document"""
		dict = {}
		#print 'dict', dict

		word_list = self.parser.tokenise_and_remove_stop_words(word_string.split(" "))

		counter = 0
		for word in word_list:
			i = self.vector_index_to_keyword_mapping[word]
			if not dict.has_key(word):
				dict[word] = [counter]

			else:
				dict[word].append(counter)
			counter += 1
		return dict
	'''


	def _remove_duplicates(self, list):
		""" remove duplicates from a list """
		return set((item for item in list))


	def _cosine(self, vector1, vector2):
		""" related documents j and q are in the concept space by comparing the vectors :
			cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
		return float(numpy.dot(vector1,vector2) / (numpy.norm(vector1) * numpy.norm(vector2)))