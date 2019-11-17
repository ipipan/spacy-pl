import os
import plac
from spacy.cli import init_model
from pathlib import Path


def initialize():
  vec_name = "kgr10_handpruned.plain.skipgram.dim100.neg10.vec"
  # The vectors we use were handpruned to 800.000 most common words
  # the remaining words were simply removed from the embedding table
  # we've found that this does not reduce performance, but speeds up
  # the processing, and reduces the size of the model significantly
  # when compared to pruning the vectors using the --prune-vectors utility.

  vectors_path = os.path.join("Resources", "Embeddings", vec_name)
  init_model("pl", Path("BaseModel"), vectors_loc = Path(vectors_path))


if __name__ == "__main__":
    plac.call(initialize)
