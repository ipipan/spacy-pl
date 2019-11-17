import os
import plac
import sys
import getopt
from spacy import cli



def main(dev_run: ("Runs all the training with 1 iteration only", 'option', 'd'), version = "0.1"):
  # dev_run is a flag, which sets all the training iterations to 1,
  # for the purposes of testing the assembly process
  if dev_run:
    development_run = True
  else:
    development_run = False
  
  VERSION = version
  # converting the resources into JSON files
  from conversion import convert_resources
  convert_resources()
  print("\nResources converted\n")
  
  # initializing the model
  from initialization import initialize
  initialize()
  print("\nModel initialized\n")

  # training the components, this may naturally take long time
  # for training them separately at different times, just run the respective scripts
  from tagger_training import train_tagger
  train_tagger(development_run)
  print("\nTagger trained\n")

  from parser_training import train_parser
  train_parser(development_run)
  print("\nParser trained\n")

  from ner_training import train_ner
  train_ner(development_run)
  print("\nNER component trained\n")

  # assembling the model
  from assembly import assemble_model
  assemble_model(VERSION)
  print("\nModel assembled\n")

if __name__ == "__main__":
    plac.call(main)
