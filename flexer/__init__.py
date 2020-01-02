import morfeusz2
import distance


class Flexer(object):
  name = "flexer"
  def __init__(self, nlp):
    self.nlp = nlp
    try:
      self.nlp.tokenizer.morf.generate("")
    except RuntimeError:
      # morfeusz does not have the generate dictionary loaded
      self.nlp.tokenizer.morf = morfeusz2.Morfeusz(expand_tags = True, whitespace = morfeusz2.KEEP_WHITESPACES, generate = True)
    self.morf = self.nlp.tokenizer.morf

  def __call__(self, doc):
    # this component does nothing in __call__
    # its functionality is performed via the flex method
    return doc

  def flex(self, token, pattern):
    # token is a spacy token
    # pattern is a ":" separated list of desired attributes for the new word to take on
    # the new word will be selected from the options provided by the generator
    # as the levenshtein nearest pattern counting from the pressent token's features

    split_pattern = pattern.split(":")
    lemma = token.lemma_
    
    pos_tag = token.tag_
    feats = token._.feats
    tag = pos_tag
    if feats != "":
      tag += ":" + feats
      
    split_tag = tag.split(":")

    def gen_to_tag(gen):
      return gen[2].split(":")
    
    generation = self.morf.generate(lemma)
    right = [g for g in generation if all([f in gen_to_tag(g) for f in split_pattern])]
    #right = [g for g in generation if attr in gen_to_tag(g) and gen_to_tag(g)[0] == pos_tag]
    #right = [g for g in generation if match(tag, g[2], attr)]
    if right == []:
      return word

    else:
      
      srt = sorted(right, key = lambda g: distance.levenshtein(split_tag, gen_to_tag(g)))
      newform = srt[0][0]
      return newform
