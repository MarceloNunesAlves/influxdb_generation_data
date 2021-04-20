import random

def calcRandom(_amplitude, _perc_random):
    return _amplitude - random.uniform(_amplitude-((_perc_random*_amplitude)/100),_amplitude+((_perc_random*_amplitude)/100))