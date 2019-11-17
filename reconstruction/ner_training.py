import os
import plac
from spacy.cli import train
from pathlib import Path

def train_ner(development_run = False):
  # Parameters
  BASE_MODEL = "BaseModel"
  if development_run:
    N_ITER = 1
  else:
    N_ITER = 60
  EARLY_STOPPING = 20
  TRAIN_LOC = os.path.join("ConvertedResources","NER", "nkjp_ner_train.json")
  DEV_LOC = os.path.join("ConvertedResources","NER", "nkjp_ner_dev.json")

  # setting the hyperparameters via env variables
  HYPERPARAMETERS = {"hidden_width" : "150",
                     "optimizer_eps" : "0.000001",
                     "dropout_from" : "0.4",
                     "dropout_to": "0.4"
                     }
  for h in HYPERPARAMETERS:
    os.environ[h] = HYPERPARAMETERS[h]
    
  train("pl", Path("NER"), Path(TRAIN_LOC), Path(DEV_LOC),
        pipeline = "ner", vectors = BASE_MODEL,
        n_iter = N_ITER, n_early_stopping = EARLY_STOPPING,
        verbose = False)

  # cleaning up the hyperparameters
  for h in HYPERPARAMETERS:
    os.unsetenv(h)

if __name__ == "__main__":
    plac.call(train_ner)
