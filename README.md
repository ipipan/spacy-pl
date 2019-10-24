# spaCy: Polish language pipeline and models

## Where to get it
The latest version of the model is available here: [http://zil.ipipan.waw.pl/SpacyPL](http://zil.ipipan.waw.pl/SpacyPL)

## Installation
First, you need to install spaCy. Please refer to the [official documentation](https://spacy.io/usage) to do so.

For example, using Anaconda:

```bash
conda install -c conda-forge spacy
```

Then, after downloading the package, install it as any other python module: 

```bash
python -m pip install PATH/TO/pl_spacy_model-x.x.x.tar.gz
```

## Quick start

```python
import spacy
nlp = spacy.load('pl_spacy_model')

# List the tokens including their lemmas and POS tags
doc = nlp("Granice mojego języka oznaczają granice mojego świata") # ~Wittgenstein
for token in doc:
    print(token.text, token.lemma_, token.tag_)
```

## A more complete example
Please see this [Jupyter notebook](https://nbviewer.jupyter.org/github/ipipan/spacy-pl/blob/master/spaCy-PL-demo.ipynb)

or this [poster](poster.pdf) and [presentation](presentation.pdf).

## What is included?

### Lemmatizer
The lemmatizer is implemented as a look-up table, using a lemma dictionary imported from the [Morfeusz morphological analyzer](http://morfeusz.sgjp.pl/).

### Tagger
The tagger has been trained on a corpus consisting of the 1 million word subcurpous of the [National Corpus of Polish](http://clip.ipipan.waw.pl/NationalCorpusOfPolish} and the 500k [Frequency Corpus of the 1960s Polish language](http://clip.ipipan.waw.pl/PL196x). For tasks involving Polish language only, we reccomend using the internal tagset (`token.tag_` as opposed to `token.pos_`), because the latter is a lossy mapping of the former.

### Depenendency Parser
For training a dependency parser, we've used the [LFG UD treebank](https://universaldependencies.org/treebanks/pl_lfg/index.html)

### Named Entity Recognizer
NER model has been trained on the 1 million word subcurpous of the [National Corpus of Polish](http://clip.ipipan.waw.pl/NationalCorpusOfPolish). 

### Word embeddings
Word embeddings trained on KGR10 corpus (over 4 billion of words) using Fasttext by Jan Kocoń and Michał Gawor (https://clarin-pl.eu/dspace/handle/11321/606). Our model uses only the vector representation for 800.000 most frequent words.

Please see this [Jupyter notebook](https://nbviewer.jupyter.org/github/ipipan/spacy-pl/blob/master/spaCy-PL-embeddings.ipynb) for a demo.

## Change history
 * 0.0.3 -- added support for spaCy 2.2

## Authors
Ryszard Tuora

supervision: Łukasz Kobyliński

## Citing
Ryszard Tuora and Łukasz Kobyliński, "Integrating Polish Language Tools and Resources in spaCy". In: Proceedings of PP-RAI'2019 Conference, 16-18.10.2019, Wrocław, Poland.

![Poster](img/poster.png)
