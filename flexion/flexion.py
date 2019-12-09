import morfeusz2
import conllu
from itertools import product
morf = morfeusz2.Morfeusz(expand_tags = True)
  
pdb_test = r"C:\Users\RT\Desktop\Praktyki\corpora\PDB\pl_pdb-ud-test.conllu"

def flex(word, attr):
  def match(tagbase, taggoal, attr):
    spl1 = tagbase.split(":")
    for s in spl1:
      repl = tagbase.replace(s,attr)
      if repl == taggoal:
        return True
    return False
  analysis = morf.analyse(word)

  ##
  ## Here spacy should be used to disambiguate
  ##
  
  lemma = analysis[0][2][1]
  tag = analysis[0][2][2]
  generation = morf.generate(lemma)
  right = [g for g in generation if match(tag, g[2], attr)]
  if right == []:
    return word
  else:
    newform = right[0][0]
    return newform

# we should rather select only those forms from generate which match the required pattern


# supertags should not be discounted, but its not easy to recognize them, right now we do everything positionally
# and assume that matching positions are matching attributes

# żeby morfeusz był wrażliwy na kontekst trzeba wykorzystać tagger kontekstowy,
# ale obecny tagger kontekstowy nie zwraca pełnych tagów
# + ustawianie kilku wartości jednocześnie
# upewnij się że nie replaceujesz więcej niż raz (że regex ni pasuje do więcej niż jednego miejsca), np. korzystając z 

def load_test_words():
  file = open(pdb_test, 'r', encoding = "utf-8")
  txt = file.read()
  file.close()

  test_dict = {}
  # this dict is composed of lemma:(set of (form, xpostag) pairs)

  trees = conllu.parse(txt)
  for tree in trees:
    for token in tree:
      form = token["form"]
      lemma = token["lemma"]
      xpostag = token["xpostag"]
      try:
        test_dict[lemma].add((form, xpostag))
      except KeyError:
        test_dict[lemma] = set([(form, xpostag)])
  cleared_dict = {k:test_dict[k] for k in test_dict if len(test_dict[k])>1}
  return test_dict

def is1apart(tag1, tag2):
  # verifies whether two tags differ by one attribute only
  if tag1 == None or tag2 == None:
    return False
  diff_count = 0
  features1 = tag1.split(":")
  features2 = tag2.split(":")
  for f1, f2 in zip(features1, features2):
    if f1 != f2:
      diff_count += 1
  return diff_count == 1

def differing_attribute(tag1, tag2):
  features1 = tag1.split(":")
  features2 = tag2.split(":")
  for f1, f2 in zip(features1, features2):
    if f1 != f2:
      return f2
    
def test_data2pairs(test_dict):
  good_data = []
  for entry in test_dict:
    words = test_dict[entry]
    for w1, w2 in product(words, words):
      if is1apart(w1[1],w2[1]):
        attr = differing_attribute(w1[1], w2[1])
        good_data.append((w1[0], w2[0], attr))
  return good_data

test_dic = load_test_words()
data_pairs = test_data2pairs(test_dic)

score = 0
baseline_score = 0
results = []
for base, goal, attr in data_pairs:
  results.append((base, attr, goal, flex(base,attr), flex(base,attr) == goal))
  if flex(base,attr).lower() == goal.lower():
    score += 1
  if base.lower() == goal.lower():
    baseline_score += 1

print("The score is {}%, the baseline score is {}%".format(100 * score/len(data_pairs), 100 * baseline_score/len(data_pairs)))
