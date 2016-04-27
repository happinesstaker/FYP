import numpy
import sys, os
from random import random
from similarity_scoring import umbc_scoring as umbc

CORPUS_FILE = "%s/msr_paraphrase_test.txt" %  os.path.dirname(os.path.realpath(__file__))
RESULT_FILE = "%s/our_rubbish_result.txt" %  os.path.dirname(os.path.realpath(__file__))
TEST_SIZE = 500


def semantic_similarity_value(str1, str2):
    '''Modify and insert our semantic function here'''
    #return semantic_value(str1, str2)
    return umbc.umbc_sim(str1, str2)

def pearson_correlation(X, Y):
   ''' Compute Pearson Correlation Coefficient. '''
   # Normalise X and Y
   X -= X.mean()
   Y -= Y.mean()
   # Standardise X and Y
   X /= X.std()
   Y /= Y.std()
   # Compute mean product
   return numpy.mean(X*Y)


test_index = 0
result_list = list()
golden_list = list()

if len(sys.argv)==2:
    TEST_SIZE = int(sys.argv[1])

with open(CORPUS_FILE, "r") as corpus, open(RESULT_FILE, "w") as output:
    output.write("Gold\tOur\tStr1\tStr2\n")
    line = corpus.readline()
    line = corpus.readline()
    i=0
    while line:
        try:
            line = line.decode('utf-8')
            print i
            contents = line.split("\t")

            result = semantic_similarity_value(contents[3], contents[4])

            # save golden result
            golden_list.append(float(contents[0]))

            # compute our result

            result_list.append(result)

            # save local file
            output.write("%s\t%5f\t%s\t%s\n" % (contents[0], result, contents[3], contents[4]))

            # next line
            line = corpus.readline()

            test_index += 1

            if test_index % 10 == 0:
                print ".",
            if test_index % 100 == 0:
                print " ",test_index

            if test_index >= TEST_SIZE:
                break
        except:
            #result_list.append(0)
            line = corpus.readline()

            test_index += 1

        i+=1
    '''
    line = output.readline()
    line = output.readline()
    result_list = []
    golden_list = []
    while line:
        contents = line.split("\t")
        golden_list.append(contents[0])
        result_list.append(contents[1])
    '''
result_list = numpy.array(result_list)
golden_list = numpy.array(golden_list)
print "\n=========================="
print "Run with %s pairs of sentences." % test_index
print "Pearson Correlation is %10f" % pearson_correlation(result_list, golden_list)
print
print "Test result is saved in our_rubbish_result.txt"