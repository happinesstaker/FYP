from datetime import date, timedelta
from math import log1p, exp
from nltk.corpus import wordnet as wn
import numpy as np
import nltk
import DBOperation
import FYPsetting

__author__ = "Sirui XIE"

titles_dict = {}

def sim (word1, pos1, word2, pos2):
    '''
    calculate the word similarity between two words
    ignored the proposed weighing method for path edge
    should add the LSA measurement later
    :param word1:
    :param pos1:
    :param word2:
    :param pos2:
    :return: a the similarity score
    '''
    if wn.synsets(word1, pos1) & wn.synsets(word2, pos2):
        # take the case where a word has multiple synsets into account
        # as said in the umbc paper, choose the largest value
        len1 = len(wn.synsets(word1, pos1))
        len2 = len(wn.synsets(word2, pos2))
        sim_mat = np.matrix(np.arange(len1*len2).reshape((len2,len1)))
        for x in range[:len1]:
            for y in range[:len2]:
                s1 = wn.synsets(word1, pos1)[x]
                s2 = wn.synsets(word2, pos2)[y]
                sim_mat[y][x]=s1.shortest_path_distance(s2)
        distance = sim_mat.max()
        return exp(-0.25*distance)
    else:
        return 0

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
    if simi<0.05:
        penalty += simi+inverse_log_fq(token, sent)*pos_weight(pos)
    if token.antonyms:
        for x in range (len(token.antonyms)):
            if token.antonyms[x].name() == counterpart:
                penalty += simi+0.5
    return penalty

def umbc_sum(sim_dict):
    '''
    sum up the similarity score of every single token
    :param sim_dict:
    :return:
    '''
    sum = 0
    for result in sim_dict:
        sum+=result['sim']
        sum-=result['p']


def umbc_sim (title1, title2):
    '''
    compares the similarity of title1 and title2
    :param title1:
    :param title2:
    :return: a bool value, 0 for similar, 1 for not similar
    '''
    tokens1 = nltk.word_tokenize(title1)
    tagged1 = nltk.pos_tag(tokens1)
    #tokens1 = list(set(sent1)) #remove duplicate
    tokens2 = nltk.word_tokenize(title2)
    tagged2 = nltk.pos_tag(tokens2)
    #tokens2 = list(set(sent2)) #remove duplicate

    # use a matrix to store the result for later use
    Matrix = [[0 for x in range(len(tokens1))] for x in range(tokens2)]
    result1 = {}
    result2 = {}
    for x in range(len(tokens1)):
        token1=tokens1[x]
        pos1 = tagged1(x)[1]
        simi = 0;
        counterpart1 = ''
        for y in range(len(tokens2)):
            token2 = tokens2[y]
            pos2 = tagged2(y)[1]
            Matrix[y][x] = sim(token1, pos1, token2, pos2)
            if sim(token1, token2)>simi:
                simi = sim(token1, pos1, token2, pos2)
                counterpart1 = token2
        penalty1 = umbc_penalty(token1, pos1, tokens1, simi, counterpart1)
        result1[token1] = {'sim':simi, 'p':penalty1}

    for y in range (0, len(tokens2)):
        token2=tokens2[y]
        pos2 = tagged2(y)[1]
        simi = 0;
        counterpart2 = ''
        for x in range(0, len(tokens1)):
            if Matrix[y][x]>simi:
                simi = Matrix[y][x]
                counterpart2 = tokens1[x]
        penalty2 = umbc_penalty(token2, pos2, tokens2, simi, counterpart2)
        result2[token2] = {'sim':simi, 'p':penalty2}

    score = umbc_sum(result1)/(2*len(tokens1))+umbc_sum(result2)/(2*len(tokens2))

    if score > FYPsetting.SIMI_THRESHOLD:
        return True
    else:
        return False

def ini():
    '''
    initialize dates to be compared and query from database
    :return:
    '''
    for i in range (0, FYPsetting.COMPARING_DATES):
        day = date.today() - timedelta(i)
        day_digi = "%04d%02d%02d" % (day.year, day.month, day.day)
        titles = DBOperation.query_db(day_digi)
        titles_dict [i] = titles

def title_cmp():
    '''
    compare today's articles with previous 5 days
    :return: a list of articles that are not similar with previous not others in today
    '''
    ini()
    title_candidates = []
    for curr_title in titles_dict[0]:
        sim = False
        # compare with newly selected candidates first
        if title_candidates:
            for candidate in title_candidates:
                if umbc_sim(curr_title, candidate):
                    sim = True
                    break

        # then compare with articles fed to users earlier
        if not sim:
            for i in range(1, FYPsetting.COMPARING_DATES):
                if titles_dict[i]:
                    if not sim:
                        for prev_title in titles_dict[i]:
                            if umbc_sim(curr_title, prev_title):
                                sim = True
                                break
                    else:
                        break

        if not sim:
            title_candidates.extend(curr_title)

    return title_candidates

if __name__ == '__main__':
    title_cmp()