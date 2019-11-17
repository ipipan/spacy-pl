import os
import plac
from pathlib import Path
from spacy.cli import train
from custom_train import custom_train
# we use a custom train, which modifies the Language class constructor,
# (both of these come from spaCy 2.2.2)
# the only difference between them is that we use our own
# simplified version of the tag_map mapping the 35 NKJP POS tags onto UD


def train_tagger(development_run = False):
  # Parameters
  BASE_MODEL = "BaseModel"
  if development_run:
    N_ITER = 1
  else:
    N_ITER = 40
  EARLY_STOPPING = 8
  TRAIN_LOC = os.path.join("ConvertedResources","Tagger", "nkjp+60s_train.json")
  DEV_LOC = os.path.join("ConvertedResources","Tagger", "nkjp+60s_dev.json")

  # setting the hyperparameters via env variables
  HYPERPARAMETERS = {"hidden_width" : "100"
                     }
  for h in HYPERPARAMETERS:
    os.environ[h] = HYPERPARAMETERS[h]

  # We use a custom tag_map, if the one fetched from the language class is not
  # identical, we use custom_train instead of the regular train utility.
  # custom_train is the standard cli.train from v. 2.2.2, but it substitutes
  # the tag_map while creating the model.
  from tag_map import custom_tag_map
  from spacy.lang import pl  
  pl_tag_map = pl.Polish.Defaults.tag_map

  if pl_tag_map == custom_tag_map:
    train("pl", Path("Tagger"), Path(TRAIN_LOC), Path(DEV_LOC),
               pipeline = "tagger", vectors = BASE_MODEL,
               n_iter = N_ITER, n_early_stopping = EARLY_STOPPING,
               verbose = False)
  else:
    custom_train("pl", Path("Tagger"), Path(TRAIN_LOC), Path(DEV_LOC),
               pipeline = "tagger", vectors = BASE_MODEL,
               n_iter = N_ITER, n_early_stopping = EARLY_STOPPING,
               verbose = False)

  # cleaning up the hyperparameters
  for h in HYPERPARAMETERS:
    os.unsetenv(h)

if __name__ == "__main__":
    plac.call(train_tagger)
