from datetime import date, timedelta
from math import log1p, exp
from nltk.corpus import wordnet as wn
from nltk.tokenize import MWETokenizer
import nltk
import DBOperation
import FYPsetting
from lsa_matrix import LSAMatrix
from tfcos_scoring import TfSim
from wordnet_boosting import WordNet_boosting

from datetime import datetime
import re
import numpy as np

existing_articles = {}
lsa_mat = LSAMatrix(0, 0)
wn_bst = WordNet_boosting()
#tf_sim = TfSim()

def sim (token1, pos1, token2, pos2):
    '''
    calculate the term similarity between two terms
    in LSA, by doing word vectorization first and combine vecotrs
    in WordNet Boosting, term similarity is already contained
    ignored the proposed weighing method for path edge
    should add the LSA measurement later
    :return: a the similarity score
    '''
    lsa_sim = lsa_mat.term_similarity(token1, token2)
    wn_sim = wn_bst.term_similarity(token1, pos1, token2, pos2)
    simi = 0
    if token1 == token2 and pos1 == pos2:
        simi = 1.0
    elif lsa_sim>0.8 and wn_sim<0.2:
        simi = 0.5*lsa_sim + 0.5*(0.5+wn_sim)
    elif lsa_sim <0.1 and wn_bst<0.8:#filter
        simi = 0
    else:
        simi = 0.5*lsa_sim+0.5*wn_sim
    #print token1, " and ", token2, " has similarity of ", simi
    # set the ceiling as mentioned in the paper
    print token1, pos1, token2, pos2, "lsa: ",lsa_sim, "wn: ",wn_sim, "sim: ", simi
    if simi>1:
        simi = 1
    return simi

def inverse_log_fq(token, sent):
    '''
    calculate the penalty for the token's inverse log frequency
    :param token:
    :param sent:
    :return:
    '''
    fdist = nltk.FreqDist(sent)
    if log1p(fdist[token]):
        return 1/log1p(fdist[token])
    else:
        return 0

def pos_weight(pos):
    '''
    assign POS weight to the token according to the rule written in umbc paper
    1 for noun, verb, pronoun, and number; 0.5 for others
    :param pos:
    :return:
    '''
    # choose the prefix as there are detailed categories defined under NN, VB etc.
    if pos[:2]=='NN' or pos[:2]=='VB' or pos[:3]=='PRP' or pos=='CD' or pos[:2]=='WP':
        return 1
    else:
        return 0.5

def umbc_penalty(token, pos, sent, simi, counterpart):
    '''
    calcualte the penalty for every single token
    consisting of two situations for penalty
        A. very unsimilar
        B. antonym
    :param token:
    :param pos:
    :param sent:
    :param simi:
    :param counterpart:
    :return:
    '''
    penalty = 0
    if simi<0.2:
        penalty += simi+inverse_log_fq(token, sent)*pos_weight(pos)

    tag = wn_bst.get_wordnet_pos(pos)
    s = wn.synsets(token, tag)
    if not s==[]:

        #try:
            for y in range(len(s)):
                ant = s[y].lemmas()[0].antonyms()
                if not ant == []:
                    for x in range (len(ant)):
                        if ant[x].name() == counterpart:
                            penalty += (simi+0.5)
                            #print datetime.now(), " ", token, ": antonyms found."
        #except:
            #pass
    return penalty

def umbc_sum(sim_dict):
    '''
    sum up the similarity score of every single token
    :param sim_dict:
    :return:
    '''
    sum = 0
    for result in sim_dict:
        sum+=sim_dict[result]['sim']
        sum-=sim_dict[result]['p']
    return sum

def umbc_sim (title1, title2):
    '''
    compares the similarity of title1 and title2
    :param title1:
    :param title2:
    :return: a bool value, 0 for similar, 1 for not similar
    '''
    #print datetime.now(), " Preprocessing titles..."
    title1 = title_prepocessing(title1)
    title2 = title_prepocessing(title2)
    #print datetime.now(), " Tokenization and parsing starts..."
    tokenizer = MWETokenizer(wn_bst.multi_words_xpn())
    tokens1 = tokenizer.tokenize(title1.split())
    #print datetime.now(), " First title tokenized."
    tagged1 = nltk.pos_tag(tokens1)
    #print datetime.now(), " First title parsed."
    tokens2 = tokenizer.tokenize(title2.split())
    #print datetime.now(), " Second title tokenized."
    tagged2 = nltk.pos_tag(tokens2)
    #print datetime.now(), " Second title parsed."
    # remove tokens that are not supported by WordNet
    tagged1 = [x for x in tagged1 if not wn_bst.get_wordnet_pos(x[1])=='']
    tagged2 = [x for x in tagged2 if not wn_bst.get_wordnet_pos(x[1])=='']
    #print datetime.now(), " Tokens cleaned."

    # use a matrix to store the result for later use
    #print datetime.now(), " Building matrix..."
    len1 = len(tagged1)
    len2 = len(tagged2)
    Matrix = np.zeros((len2,len1))
    result1 = {}
    result2 = {}
    for x in range(len1):
        token1=tagged1[x][0]
        pos1 = tagged1[x][1]
        simi = 0
        counterpart1 = ''
        for y in range(len2):
            token2 = tagged2[y][0]
            pos2 = tagged2[y][1]
            Matrix[y, x] = sim(token1, pos1, token2, pos2)
            if Matrix[y,x]>simi:
                simi = Matrix[y, x]
                counterpart1 = token2
        penalty1 = umbc_penalty(token1, pos1, tokens1, simi, counterpart1)
        result1[token1] = {'sim':simi, 'p':penalty1, 'counter':counterpart1}
    #print datetime.now(), " Title1 result calculated..."
    for y in range (0, len2):
        token2=tagged2[y][0]
        pos2 = tagged2[y][1]
        simi = 0
        counterpart2 = ''
        for x in range(0, len1):
            if Matrix[y,x]>simi:
                simi = Matrix[y,x]
                counterpart2 = tagged1[x][0]
                print token2, counterpart2, simi
        penalty2 = umbc_penalty(token2, pos2, tokens2, simi, counterpart2)
        result2[token2] = {'sim':simi, 'p':penalty2, 'counter':counterpart2}
    #print datetime.now(), " Title2 result calculated..."
    print result1
    sum1 = umbc_sum(result1)
    sum1 = float(sum1)
    print result2
    sum2 = umbc_sum(result2)
    sum2 = float(sum2)
    #print sum1, sum2
    score = sum1/(2*len1)+sum2/(2*len2)
    #cut upper and lower bound
    if score < 0:
        score = 0


    return score

def ini():
    '''
    initialize dates to be compared and query from database
    initialize LSA_Matrix
    :return:
    '''
    global lsa_mat
    global wn_bst
    global existing_articles
    for i in range (FYPsetting.COMPARING_DATES):
        day = date.today() - timedelta(i)
        day_digi = "%04d%02d%02d" % (day.year, day.month, day.day)
        titles = DBOperation.query_articles(day_digi)
        #print datetime.now(), " Title2s extracted."
        existing_articles.append(titles)

    lsa_mat.update()

def title_prepocessing(string):
    string = string.lstrip()
    string = string.rstrip()
    string = string.replace("\'", "")
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
    string = string.replace("\\", "")
    string = string.replace("\s+"," ")
    string = string.replace("\t", " ")
    string = string.replace("\n", " ")
    string = re.sub(' +',' ',string)
    return string

def sim_score(doc1, doc2):
    return 0.5*umbc_sim(doc1[0], doc1[0])+ 0.5*tf_sim.cos_similarity(doc1[1], doc2[1])

def article_cmp(curr_article = ("currencet title", "current body")):
    '''

    compare today's articles with previous 5 days
    :return: a list of articles that are not similar with previous not others in today
    '''
    #ini()
    global existing_articles
    existing_articles = {"This is title 1":"This is body 1", "Here is title 1":"Here is body 1"}
    article_candidates = {}
    '''
    #for curr_article in curr_articles:
    '''
    sim = False
    # compare with newly selected candidates first
    if not article_candidates=={}:
        for candidate in article_candidates:
            # This weight can be adjusted
            score = sim_score(curr_article, candidate)
            #print curr_article, candidate, "score is: ", score
            if score > FYPsetting.SIMI_THRESHOLD:
                sim = True
                break

    # then compare with articles fed to users earlier
    if not sim:
        '''
        for i in range(1, FYPsetting.COMPARING_DATES):
            print i
            if existing_articles[i]:
                if not sim:
                    for existing_article in existing_articles[i]:# existing_articles is a list of article list by date
                        score = sim_score(curr_article, existing_article)
                        if score > FYPsetting.SIMI_THRESHOLD:
                            sim = True
                            break
                else:
                    break
        '''


        for existing_article in existing_articles:# existing_articles is a list of article list by date
            score = sim_score(curr_article, existing_article)
            #print curr_article, existing_article, "score is: ", score
            if score > FYPsetting.SIMI_THRESHOLD:
                sim = True
                break


    if not sim:
        # is there any cases where two articles have the same title?
        article_candidates[curr_article[0]]=curr_article[1]

    return article_candidates

if __name__ == '__main__':
    #title_cmp()
    #ini()
    #print umbc_sim("Apple is bad.","Apple is good.")

    print article_cmp()