from numpy import dot
from scipy import linalg
import scipy.sparse as sp
import scipy.sparse.linalg as la
from datetime import datetime

from semantic.transform.transform import Transform

class LSA(Transform):
	""" Latent Semantic Analysis(LSA).
		Apply transform to a document-term matrix to bring out latent relationships.
	    These are found by analysing relationships between the documents and the terms they
	    contain.
    """
	def __init__(self, sparse_matrix):
		Transform.__init__(self,sparse_matrix)
		self.matrix = sp.coo_matrix(sparse_matrix)

	def transform(self, dimensions=1):
		""" Calculate SVD of objects matrix: U . SIGMA . VT = MATRIX
		    Reduce the dimension of sigma by specified factor producing sigma'.
		    Then dot product the matrices:  U . SIGMA' . VT = MATRIX'
		"""
		rows,cols = self.matrix.get_shape()

		if dimensions <= rows: #Its a valid reduction

			#Sigma comes out as a list rather than a matrix
			u,sigma,vt = la.svds(self.matrix, dimensions)

			'''
			#Dimension reduction, build SIGMA'
			for index in xrange(rows - dimensions, rows):
				sigma[index] = 0
			'''
			print datetime.now(), " Decomposition finished, reconstruction starts..."
			transformed_matrix = dot(u, linalg.diagsvd(sigma, len(u[0]), len(vt)))
			print datetime.now(), "    First multiplication finished."
			transformed_matrix = dot(transformed_matrix, vt)

			return transformed_matrix

		else:
			print "dimension reduction cannot be greater than %s" % rows