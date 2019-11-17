# coding: utf8
from __future__ import unicode_literals
from spacy.util import load_model_from_init_py, get_model_meta
from pathlib import Path
from .Lemmatizer.lemmatizer import PolishLemmatizer

__version__ = get_model_meta(Path(__file__).parent)['version']


def load(**overrides):
    model = load_model_from_init_py(__file__, **overrides)
    lemmatizer = PolishLemmatizer()
    model.tagger.vocab.morphology.lemmatizer = lemmatizer
    # loading our custom, lookup-based lemmatizer
    return model
