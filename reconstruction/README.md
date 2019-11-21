These scripts serve the purpose of reproducing the model for polish, for spaCy.

The expected structure of the folder is as follows:

/folder
  /Lemmatizer.tar.gz
  /resources.tar.gz
  /all the other .py files

Scripts can be either run separately, at different times (learning will take quite some time), or just called from the main script: reconstruction.py
So, either just run reconstruction.py, or perform the following steps in the order given here.

1. conversion.py - conversion of resources into .json
2. initialization.py - initializing the model, and processing the word vectors
3. tagger_training.py - training the tagger, and replacing the tag_map by our own
4. parser_training.py - training the parser_training
5. ner_training.py - training the NER component
6. assembly.py - assembling the final model, combining components, copying the lemmatizer and custom init.py
7. evaluate.py - evaluating the model using the conll-18 evaluation script, the results are saved as an .xlsx, and .csv files.

The hyperparameters and settings are defined in their respective scripts.

The data for the parser are provided as available at universaldependencies.org. Data for NER and Tagger come from NKJP and Polish Frequency Corpus of the 1960s. They have been converted into .iob, and conllu formats, as they were initially formatted in .xml, and required some tedious preprocessing. Because these files are unlikely to get updated, at the moment we do not plan on providing the original, big .xml files and the kludge'y scripts used to convert them. In case of problems please contact one of the authors at ryszardtuora@gmail.com.

The resources we've used are:

1. KGR fasttext embeddings on the GNU LGPL 3.0 license
Kocoń, Jan and Gawor, Michał, Evaluating {KGR10} Polish word embeddings in the recognition of temporal expressions using BiLSTM-CRF, Schedae Informaticae, (27) 2018
http://www.ejournals.eu/Schedae-Informaticae/2018/Volume-27/art/13931/ , doi:10.4467/20838476SI.18.008.10413
http://hdl.handle.net/11321/606

2. NKJP corpus on the GNU GPL 3.0 license
http://nkjp.pl/

3. The corpus of the frequency dictionary of contemporary Polish (from 1960s) on the GNU GPL 2.0 license
http://clip.ipipan.waw.pl/PL196x

4. Lemma dictionary from Morfeusz 2 on the 2-clause BSD license
Marcin Woliński Morfeusz reloaded. In Nicoletta Calzolari, Khalid Choukri, Thierry Declerck, Hrafn Loftsson, Bente Maegaard, Joseph Mariani, Asuncion Moreno, Jan Odijk, and Stelios Piperidis, editors, Proceedings of the Ninth International Conference on Language Resources and Evaluation, LREC 2014, pages 1106–1111, Reykjavík, Iceland, 2014. ELRA.
http://morfeusz.sgjp.pl/

5. PDB UD treebank on the GNU GPL 3.0 license 
http://git.nlp.ipipan.waw.pl/alina/PDBUD
