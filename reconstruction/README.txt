These scripts serve the purpose of reproducing the model for polish, for spaCy.

The expected structure of the folder is as follows:

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