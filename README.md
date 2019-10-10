# spaCy: Polish language pipeline and models

## Where to get it
The latest version of the model is available here: [http://zil.ipipan.waw.pl/SpacyPL]()

## Installation
Install package as any other python module: 

```bash
python -m pip install pl_spacy_model-x.x.x.tar.gz
```

## Quick start

```python
import spacy
nlp = spacy.load('pl_spacy_model')

# List the tokens including their lemmas and POS tags
doc = nlp("Granice mojego języka oznaczają granice mojego świata") # ~Wittgenstein
for token in doc:
    print(token.text, token.lemma_, token.pos_)
```

## A more complete example
Please see this [Jupyter notebook](spaCy-PL-demo.ipynb)

## What is included?

### Lemmatizer
The lemmatizer is implemented as a look-up table, using a lemma dictionary imported from the [Morfeusz morphological analyzer](http://morfeusz.sgjp.pl/).

### Tagger
The tagger has been trained on a corpus consisting of the 1 million word subcurpous of the [National Corpus of Polish](http://clip.ipipan.waw.pl/NationalCorpusOfPolish} and the 500k [Frequency Corpus of the 1960s Polish language](http://clip.ipipan.waw.pl/PL196x).

### Depenendency Parser
For training a dependency parser, we've used the [PDB UD treebank](https://universaldependencies.org/treebanks/pl_pdb/index.html)

### Named Entity Recognizer
NER model has been trained on the 1 million word subcurpous of the [National Corpus of Polish](http://clip.ipipan.waw.pl/NationalCorpusOfPolish}. 

## Change history
 * 0.0.3 -- added support for spaCy 2.2

## Authors
Ryszard Tuora

supervision: Łukasz Kobyliński
