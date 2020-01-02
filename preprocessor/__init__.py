try:
  import morfeusz2
  imported_Morfeusz = True
except ImportError:
  err_msg='''
  This model uses the morfeusz2 python module for tokenization, tagging and lemmatization.
  We couldn't find it installed on this machine.
  For best performance, please install the morfeusz2 Binding for python from here:
  
  http://morfeusz.sgjp.pl/download/en
  
          '''
  print(err_msg)
  imported_Morfeusz = False

import distance

from spacy.tokens import Doc, Token

from .Toygger import Toygger

class PolishPreProcessor():
  # this class uses morfeusz2 library to work properly
  # it performs tokenization, lemmatization, tagging and morphological analysis
  def __init__(self, nlp):
    if imported_Morfeusz:
      self.morf = morfeusz2.Morfeusz(generate = False, whitespace = morfeusz2.KEEP_WHITESPACES, expand_tags=True)
    self.imported_Morfeusz = imported_Morfeusz
    self.nlp = nlp
    self.toygger = Toygger()
    self.vocab = self.nlp.vocab

    Token.set_extension("feats", default = "")
    # we reserve a custom attribute for storing morphological features

    #tagmap into UD POS
    self.tag_map = {'adj': 'ADJ',
                    'adja': 'ADJ',
                    'adjc': 'ADJ',
                    'adjp': 'ADJ',
                    'adv': 'ADV',
                    'aglt': 'AUX',
                    'bedzie': 'VERB',
                    'brev': 'X',
                    'burk': 'ADV',
                    'comp': 'SCONJ',
                    'conj': 'CCONJ',
                    'depr': 'NOUN',
                    'fin': 'VERB',
                    'ger': 'NOUN',
                    'imps': 'VERB',
                    'impt': 'VERB',
                    'inf': 'VERB',
                    'interj': 'INTJ',
                    'interp': 'PUNCT',
                    'num': 'NUM',
                    'numcol': 'NUM',
                    'pact': 'VERB',
                    'pant': 'VERB',
                    'pcon': 'VERB',
                    'ppas': 'VERB',
                    'ppron12': 'PRON',
                    'ppron3': 'PRON',
                    'praet': 'VERB',
                    'pred': 'VERB',
                    'prep': 'ADP',
                    'qub': 'PART',
                    'siebie': 'PRON',
                    'subst': 'NOUN',
                    'winien': 'VERB',
                    'xxx': 'X',
                    #additional tags besides nkjp
                    'part' : 'PART',# particle
                    'ign' : 'X',
                    'dig' : 'NUM',
                    'romandig' : 'NUM',
                    'frag' : 'X',
                    'pacta' : 'VERB',
                    'numcomp' : 'NUM'}


  def disambiguate_tokenization(self, analyses):
    # The logic of this function is a bit messy and could be improved
    # Perhaps we should utilize graph paths as returned by Morfeusz2 instead of graph nodes
    # Helper functions:
    def renumerate_analysis(analysis, target_start):
      # we assume that analyses have span 1 only
      new_analysis = (target_start, target_start+1, analysis[2])
      return new_analysis

    # Creating a token_number -> [analyses] dictionary
    exceptions = {"Coś":('Co', 'ś'), "Ktoś":('Kto', 'ś'), "Kogoś":("Kogo", "ś"), "Kiedyś":('Kiedy', 'ś'), "Gdzieś":('Gdzie', 'ś'),
                "coś":('co', 'ś'), "ktoś":('kto', 'ś'), "kogoś":("kogo", "ś"), "kiedyś":('kiedy', 'ś'), "gdzieś":('gdzie', 'ś')}
    # There are some frequently used words which can be segmented in principle, but this happens very rarely
    # We always choose the more finegrained tokenization, with exception of the words listed above
    # This improves tokenization accuracy by 0.1 to 0.5%
    
    position_to_analyses={}
    analyses_to_remove=[]
    max_index = 0
    for a in analyses:
      start_index = a[0]
      end_index = a[1]
      span = end_index - start_index
      max_index = max((max_index, start_index))
      form = a[2][0]
      if span>1:
      # Disambiguation of tokenization
      # let us asssume for now that all differences in segmentation are contained in each other
      # and thus we choose to always oversegment
        if form not in exceptions:
          continue
        else:
          dec1, dec2 = exceptions[form]
          for a2 in analyses:
            if (a2[0] == start_index and a2[2][0] == dec1) or (a2[1] == end_index and a2[2][0] == dec2):
              analyses_to_remove.append(a2) 
      try:
        position_to_analyses[start_index].append(a)
      except KeyError:
        position_to_analyses[start_index]=[a]
    for p in position_to_analyses:
      for a_r in analyses_to_remove:
        if a_r in position_to_analyses[p]:
          position_to_analyses[p].remove(a_r)
    
    # Renumeration - is it needed at all?
    n_position_to_analyses={}
    curr_ind=0
    for ind in range(max_index+1):
      if position_to_analyses[ind] == []:
        continue
      else:
        table = []
        for a in position_to_analyses[ind]:
          renumerated = renumerate_analysis(a, curr_ind)
          table.append(renumerated)
        n_position_to_analyses[curr_ind] = table
        curr_ind += 1
        
    return n_position_to_analyses

  def skip_white_space_list(self, position_to_analyses):
    # This could, in principle, be done on a dict-based basis,
    # i.e. it could return a form -> analysis dictionary
    # as opposed to a list, i.e. an index -> analysis dictionary
    # because morfeusz is context insensitive
    # Skipping white-space tokens
    non_white_analysis = []
    words = []
    space_afters = []
    for ind in position_to_analyses:
      entry = position_to_analyses[ind][0]
      form = entry[2][0]
      # Because the tokenization is disambiguated, we assume that all interpretations
      # share the same form
      tagging = entry[2][2].split(':')[0]
      if form == ' ' or tagging == 'sp':
        space_afters[-1]=True
      else:
        space_afters.append(False)
        words.append(form)
        non_white_analysis.append([a for a in position_to_analyses[ind]])
    return (non_white_analysis, words, space_afters)

  def disambiguate_morphology(self, matching_analyses):
    # Returns only those features, which are constant in all analyses
    morphs_annotations = [((m[3]).split(":"))[1:] for m in matching_analyses]
    aligned = zip(*morphs_annotations)
    matching_features = filter(lambda an: all([a == an[0] for a in an]), aligned)
    agreement_array = [f[0] for f in matching_features]
    disambiguated_string = ":".join(agreement_array)
    return disambiguated_string

  def pos_tags(self, tags):
    return [self.tag_map[t.split(":")[0]] for t in tags]
  
  def lemmatize_by_tags(self, tags, non_white_analysis):
    lemmas = []

    for an, tag in zip(non_white_analysis, tags):
      ordered_analyses = sorted(an, key = lambda x: distance.levenshtein(tag.split(":"), x[2][2].split(":")))
      best = ordered_analyses[0]
      lemma = best[2][1].split(":")[0]
      lemmas.append(lemma)
      
    return lemmas
  
  def process(self, text):
    text = text.strip()		
    # this is a temporary fix, if the text begins with whitespace, we have problems with space-afters		
    # we should ideally rethink the way we treat whitespace, because spacy does seem to remember some of it (i.e. whether it was a \t or space
    analyses = self.morf.analyse(text)
    position_to_analyses = self.disambiguate_tokenization(analyses)
    
    #non_white_analysis, words, space_afters = self.skip_white_space(position_to_analyses)
    non_white_analysis, words, space_afters = self.skip_white_space_list(position_to_analyses)

    # Saving the tokenization
    doc = Doc(self.vocab, words, space_afters)
    
    # HERE COMES TOYGGER
    tags = self.toygger.process(non_white_analysis, doc)
    ud_tags = self.pos_tags(tags)
    lemmas = self.lemmatize_by_tags(tags, non_white_analysis)
    
    for ind, tok in enumerate(doc):
      # these assignments may need to be done by the respective setters of spacy.tokens.token
      # the ordering of assignments is important because of this

#
      split_tag = tags[ind].split(":")
      doc[ind].tag_ = split_tag[0]

      try:
        features = split_tag[1:]
        doc[ind]._.feats = ":".join(features)
      except IndexError:
        pass

      doc[ind].pos_ = ud_tags[ind]
      doc[ind].lemma_ = lemmas[ind]
#
      
      # we also may need to implement the integer coding of features
    
    # assert doc.text == text #can be false
    # nondestructive tokenization seems impossible, because spacy does not distinguish
    # between different types of whitespace while creating the doc

    return doc
  
  def __call__(self, text):
    return self.process(text)
