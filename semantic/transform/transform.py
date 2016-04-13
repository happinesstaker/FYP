
from semantic.matrix_formatter import MatrixFormatter
from scipy import array

class Transform:
    def __init__(self, spmat):
        self.matrix = spmat

    def __repr__(self):
        MatrixFormatter(self.matrix).pretty_print