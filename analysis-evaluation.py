import os
import spacy
import conllu
import pandas

from tag_map import tag_map

#LOADING THE MODEL
nlp = spacy.load('pl_spacy_model_morfeusz')
print('Model loaded')
print(nlp.pipeline)

#OUTPUT NAME:
modelname= 'pl_spacy_model_suff0.1.0'#input('Please provide the name for the model: ')
print('Files will have the  "{}" suffix.'.format(modelname))

corpora=[#os.path.join("corpora", "LFG", "pl_lfg-ud-train.conllu"),
         #os.path.join("corpora", "LFG", "pl_lfg-ud-dev.conllu"),
         os.path.join("corpora", "LFG", "pl_lfg-ud-test.conllu"),
         #os.path.join("corpora", "PDB", "pl_pdb-ud-train.conllu"),
         #os.path.join("corpora", "PDB", "pl_pdb-ud-dev.conllu"),
         os.path.join("corpora", "PDB", "pl_pdb-ud-test.conllu"),
         os.path.join("corpora", "PUD","pl_pud-ud-test.conllu"),
         ]

def load_corpus(corpus_name):
  #loads a corpus into 'tokenlist' representation from the conllu module
  file=open(corpus_name, 'r', encoding='utf-8')
  txt=file.read()
  file.close()
  tokenlists=conllu.parse(txt)
  return tokenlists

def corpus_into_string(tokenlists):
  #turns a list of tokenlists into a string of sentences separated by \n
  return '\n'.join([tl.metadata['text'] for tl in tokenlists])

def process_string(string):
  #uses the nlp pipeline to process a string of text
  sents = string.split('\n')
  sent_num=len(sents)
  ind=0
  inds=[int(sent_num*(r/10)) for r in range(1,10)]
  dox = []
  for s in sents:
    ind+=1
    if ind in inds:
      print(str(ind/sent_num)+' out of '+str(sent_num)+' sentences.')
    dox.append(nlp(s))
  return dox

def doc_to_conllu(doc):
  #takes a spaCy document corresponding to a sentence, and returns a .conllu representation of it
  sent_conllus = []
  last_token_ind = 0
  for sent in doc.sents:
    toks=[]
    offset = 1 - last_token_ind
    for t in sent: 
      index = t.i + offset
      ID = str(index)#str(index)
      FORM = t.text
      LEMMA = t.lemma_
      UPOS = t.pos_
      longtag = (t.tag_).split(':')
      XPOS = longtag[0].lower()
      try:
        features = t._.feats.split(":")
      except AttributeError:
        features = []
      morph_tag = ":".join([XPOS] + features)

      try:
        FEATS = tag_map[morph_tag][1]#'_' # should be ':'.join(longtag[1:])
      except KeyError:
        FEATS = "_"
      HEAD = str(t.head.i + offset)
      # spaCy assigns 0 to the first token, whereas UD requires it to be 1
      DEPREL = t.dep_.lower()

      if not nlp.has_pipe('parser'):
      #for nlp not including parsers
        if HEAD==ID:
          HEAD='1'
          DEPREL='dep'
          if ID=='1':
            HEAD='0'
            DEPREL='root'
      #/

      
      # spaCy assigns 'ROOT' in allcaps to the root, whereas other deprels are
      # learned from the dataset, and in our case are lowercase
      if DEPREL == 'root':
        # with respect to the root token, spaCy assigns it its own id as head
        # this is inconsistent with the UD conventions, which require that
        # the root token has head = 0
        HEAD = str(0)
      DEPS = '_'
      MISC = '_'
      fields=[ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC]
      tok='\t'.join(fields)
      toks.append(tok)
    last_token_ind += index
    sent_conllu='\n'.join(toks)
    sent_conllus.append(sent_conllu)
  conllu = '\n\n'.join(sent_conllus)
  conllu+='\n\n'
  return conllu

def dox_to_conllu(dox):
  # takes a list of documents (which correspond to sentences here)
  # and returns a conllu file
  conllu=''
  sent_num=len(dox)
  ind=0
  inds=[int(sent_num*(r/10)) for r in range(1,10)]
  for d in dox:
    ind+=1
    if ind in inds:
      print(str(ind/sent_num)+' out of '+str(sent_num)+' sentences.')
    c=doc_to_conllu(d)
    conllu+=c
  return conllu

def parse(corpora):
  #takes a list of filenames, and processes them, saving the outputs to disk
  for f in corpora:
    c=load_corpus(f)
    s=corpus_into_string(c)
    p=process_string(s)
    cn=dox_to_conllu(p)
    file=open(f.replace('.conllu','_spaCy_{}.conllu'.format(modelname)), 'w', encoding='utf-8')
    file.write(cn)
    file.close()
    print(f + ' is done.')

def evaluate(eval_dic):
  #evaluates the outputs against gold files using conll18_ud_eval module by UD
  #eval_dic should be a dictionary with gold filenames as keys and system filenames as values
  import conll18_ud_eval
  table=[]
  for k in eval_dic:
    gfile=open(k, 'r', encoding='utf-8')
    sfile=open(eval_dic[k], 'r', encoding='utf-8')
    g=conll18_ud_eval.load_conllu(gfile)
    s=conll18_ud_eval.load_conllu(sfile)
    gfile.close()
    sfile.close()
    evaluation=conll18_ud_eval.evaluate(g,s)
    newdic={}
    name=k.split('\\')[-1]
    name=name.replace('-ud-','_')
    name=name.replace('.conllu','')
    newdic['name']=name
    for component in ['Sentences', 'Tokens', 'Words','Lemmas', 'UPOS', 'XPOS', 'UFeats','UAS','LAS']:
      newdic[component + ' precision'] = evaluation[component].precision
      newdic[component + ' recall'] = evaluation[component].recall
      newdic[component + ' f1'] = evaluation[component].f1
      newdic[component + ' aligned_accuracy'] = evaluation[component].aligned_accuracy
    newdic['tokens'] = evaluation['Tokens'].gold_total
    newdic['words'] = evaluation['Words'].gold_total
    newdic['sentences'] = evaluation['Sentences'].gold_total
    table.append(newdic)
  df=pandas.DataFrame(table)
  return df

sent = "W starożytności tereny obecnych Niemiec zamieszkiwały plemiona Celtów."
for x in nlp(sent):
  print("\t".join([x.orth_, x.lemma_, x.tag_, x.dep_, x.head.orth_]))

eval_dic={c:c.replace('.conllu','_spaCy_{}.conllu'.format(modelname)) for c in corpora}
parse(corpora)
data=evaluate(eval_dic)
col_order = ['name', 'Sentences precision', 'Sentences recall', 'Sentences f1', 'Words precision',
             'Words recall', 'Words f1', 'Tokens precision', 'Tokens recall', 'Tokens f1',
             'XPOS precision', 'XPOS recall', 'XPOS f1', 'XPOS aligned_accuracy', 'UPOS precision',
             'UPOS recall', 'UPOS f1', 'UPOS aligned_accuracy', 'UFeats precision', 'UFeats recall',
             'UFeats f1', 'UFeats aligned_accuracy', 'Lemmas precision', 'Lemmas recall',
             'Lemmas f1', 'Lemmas aligned_accuracy', 'UAS precision', 'UAS recall', 'UAS f1',
             'UAS aligned_accuracy', 'LAS precision', 'LAS recall', 'LAS f1', 'LAS aligned_accuracy']

data[col_order].to_excel('{}.xlsx'.format(modelname))
