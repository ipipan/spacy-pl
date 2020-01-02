import pickle

from os import path
from keras.models import load_model
from numpy.random import seed
from numpy import zeros, argmax
from distance import levenshtein

from .indices import Indices
from .tagset import TAG_GROUPS, VALID_TAGS
from .settings import Settings


#TODO:
#suffix based vectorization


class Toygger():
  
  def __init__(self):
    dir_name = path.dirname(__file__)
    self.model = load_model(path.join(dir_name, "toygger_model.h5"))    
    self.settings = Settings()
    self.indices = Indices.load_indices(path.join(dir_name, "toygger_indices.pickle"), self.settings, "")
    self.seed = seed(self.settings.SEED)
    self.task_id = self.indices.TASK_ID # name of the task
    self.TAG_GROUPS = TAG_GROUPS
    self.VALID_TAGS = VALID_TAGS


  def morf_to_nkjp(self, morf_tag):
    #translates a morfeusz tag to a nkjp tag:
    pos_dic = {#additional tags besides nkjp		
              'part' : 'qub',	
              'ign' : 'xxx',		
              'dig' : 'num',		
              'romandig' : 'num',		
              'frag' : 'xxx',		
              'pacta' : 'pact',		
              'numcomp' : 'num'
               }

    segs = morf_tag.split(":")
    try:# if the pos_tag is in the pos_dic we translate it
      pos_seg = pos_dic[segs[0]]
    except KeyError: # else we just keep it as is
      pos_seg = segs[0]
    add_tags = [pos_seg]
    for s in segs[1:]:
      if s not in ('col', 'ncol', 'pt', 'NOP'):# these features are not in nkjp tagset
        add_tags.append(s)      
    return ":".join(add_tags)

  
  def morf2vector(self, morf_in, input_tag=True):
      tags = set()
      for morftag in morf_in.split('|'):
          tags.update(morftag.split(':')) # tags contains all possible features as listed
      vec = zeros((self.indices.IN_NUMTAGS))
      offset = 0
      relevant_grps = self.settings.INPUT_TAGS if input_tag else self.settings.OUTPUT_TAGS
      index = self.indices.IN_TAG2INDEX if input_tag else self.indices.OUT_TAG2INDEX
      for grp_no in relevant_grps:
          grp = self.TAG_GROUPS[grp_no]
          ts = tags.intersection(grp) # For each group we mark features which are admissible to the wordform
          if ts:
              for t in ts:
                  vec[index[t]] = 1 # our vector contains 1s where possible, on the places specified by indices
          else:
              # mark the NOXYZ tag
              vec[index[grp[-1]]] = 1 # if a given attribute does not apply at all to our word, we mark it accordingly
      return vec

  def process(self, morf_ans, doc):
    # morf_ans is a list of analyses, where an analysis is a list of interpretations for a given token
    data = []
    for morf_an, tok in zip(morf_ans, doc):
      tok_tags = [interp[2][2] for interp in morf_an]
      tag = "_"
      label = 'IGN' if tok_tags == set(['ign']) else ''
      data.append((tok.orth_, "|".join(tok_tags), tag, label))

    MAX_WORDS = len(data)
    X_s = [zeros((1, MAX_WORDS, self.indices.IN_NUMTAGS)), None, None, None, None, None, None]
    X_s[5] = zeros((len(data), MAX_WORDS, self.settings.WORD2VEC_DIM))

    for i, (data_point, tok) in enumerate(zip(data, doc)):
      morf_possible_tags = data_point[1]
      v_in = self.morf2vector(morf_possible_tags)
      X_s[0][0][i] = v_in
      X_s[5][0][i] = tok.vector

    X = [X for X in X_s if X is not None]
    
    predictions = self.model.predict(X)
    tags = [[] for x in range(len(doc))]
    for feat_i, feature in enumerate(predictions): # a feature, e.g. grammatical case
      feature = feature[0]
      for tok_i, tok_pred in enumerate(feature):# a token's prediction for a given feature
        tag = TAG_GROUPS[feat_i][argmax(tok_pred)]
        if not tag.startswith("NO"):
          tags[tok_i].append(TAG_GROUPS[feat_i][argmax(tok_pred)])

    corrected_tags = []
    for tok_i, (tok_pred, data_point) in enumerate(zip(tags, data)):
      morf_possible_tags = data_point[1]
      predicted_tag = ":".join(tok_pred)
      candidate_tags = set(filter(None, set(morf_possible_tags.split("|"))))
      # ign means selection from all possible valid tags
      if 'ign' in candidate_tags:
        candidate_tags = self.VALID_TAGS
      if candidate_tags and predicted_tag not in candidate_tags:
        distances = [(levenshtein(tok_pred, t.split(":")),t) for t in candidate_tags]
        corrected_tag = self.morf_to_nkjp(sorted(distances)[0][1])

      else:
        corrected_tag = predicted_tag

      corrected_tags.append(corrected_tag)

    return corrected_tags

