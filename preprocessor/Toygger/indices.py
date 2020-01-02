# -*- coding: utf-8 -*-
import codecs
import numpy
import os
import pickle

from collections import defaultdict

from .tagset import *
#from constants import *


class Indices(object):
    
    def __init__(self, task_id):
        self.TASK_ID = task_id
        self.IN_TAGS = []
        self.IN_TAG2INDEX = None
        self.IN_NUMTAGS = None
        self.OUT_TAGS = []
        self.OUT_TAG2INDEX = None
        self.OUT_NUMTAGS = None
        self.CHAR2INDEX = None
        self.NUMCHARS = None
        self.NUM_SUFFIXES = None
        self.SUFFIX2INDEX = None
        self.WORD2VEC = None
        self.SUFFIX_INDEX = None
        self.CONCRAFT_MODEL = None
    
    def createTagIndices(self, settings):
        for grp_no, tags in enumerate(TAG_GROUPS): # tag groups is the set of all tag attributes understood as tuples of their possible values
            if grp_no in settings.INPUT_TAGS: # 
                self.IN_TAGS += tags # extension by the !values! of the attribute
            if grp_no in settings.OUTPUT_TAGS:
                self.OUT_TAGS += tags # extension by the !values! of the attribute
	# for each tag attribute (e.g. 'acc') we assign a number
        self.IN_TAG2INDEX = { t : i for i, t in enumerate(self.IN_TAGS) }
        self.IN_NUMTAGS = len(self.IN_TAGS)
        self.OUT_TAG2INDEX = { t : i for i, t in enumerate(self.OUT_TAGS) }
        self.OUT_NUMTAGS = len(self.OUT_TAGS)
    
        
    @staticmethod
    def load_indices(path, settings, task_id):
        indices = Indices(task_id)
        with open(path, 'rb') as f:
            dct = pickle.load(f)
        for attr, val in dct.items():
            setattr(indices, attr, val)
        return indices
     
    def save(self, path):
        dct = { attr : val for attr, val in self.__dict__.items() if attr not in ('WORD2VEC', 'SUFFIX_INDEX') }
        with open(path, 'wb') as f:
            pickle.dump(dct, f)


