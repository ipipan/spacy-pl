import os
import plac
from pathlib import Path
from spacy.cli import train

def train_parser(development_run = False):
  # Parameters
  BASE_MODEL = "BaseModel"
  if development_run:
    N_ITER = 1
  else:
    N_ITER = 150
  EARLY_STOPPING = 20
  TRAIN_LOC = os.path.join("ConvertedResources","Parser", "pl_pdb-ud-train.json")
  DEV_LOC = os.path.join("ConvertedResources","Parser", "pl_pdb-ud-dev.json")
  GOLD_PREPROC = False # ideally this would be set to True, but as of v 2.2
  # True would force 1 sentence per document policy, which makes the model
  # incapable of sentencization
  
  # setting the hyperparameters via env variables
  HYPERPARAMETERS = {"dropout_from" : "0.5",
                     "dropout_to" : "0.5",
                     "hidden_width" : "200",
                     "token_vector_width" : "200"}
  for h in HYPERPARAMETERS:
    os.environ[h] = HYPERPARAMETERS[h]
    
  train("pl", Path("Parser"), Path(TRAIN_LOC), Path(DEV_LOC),
        pipeline = "parser", vectors = BASE_MODEL,
        n_iter = N_ITER, n_early_stopping = EARLY_STOPPING,
        gold_preproc = GOLD_PREPROC, verbose = False)

  # cleaning up the hyperparameters
  for h in HYPERPARAMETERS:
    os.unsetenv(h)

if __name__ == "__main__":
    plac.call(train_parser)
