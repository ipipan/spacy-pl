import os
import plac
from spacy.cli import convert

def convert_tagger(outdir):
  # Converting the NKJP, and 1960s corpora (for the tagger)

  Tagger_out = os.path.join(outdir, "Tagger")
  os.mkdir(Tagger_out)
  
  for filename in ["nkjp+60s_train.conllu",
                   "nkjp+60s_dev.conllu"]:
    filepath = os.path.join("Resources", "NKJP+1960s", filename)
    convert(filepath, Tagger_out)

def convert_parser(outdir):
  # Converting PDB (for training the parser)
  # Parameters
  N_SENTS = 10
  #
  PDB_out = os.path.join(outdir, "Parser") 
  os.mkdir(PDB_out)

  for filename in ["pl_pdb-ud-train.conllu",
                   "pl_pdb-ud-dev.conllu",
                   "pl_pdb-ud-test.conllu"]:
    filepath = os.path.join("Resources", "PDB", filename)
    convert(filepath, PDB_out, n_sents = N_SENTS)

def convert_ner(outdir):
  # Converting the NKJP (for NER)

  NER_out = os.path.join(outdir, "NER")
  os.mkdir(NER_out)
  
  for filename in ["nkjp_ner_train.iob",
                   "nkjp_ner_dev.iob"]:
    filepath = os.path.join("Resources", "NKJP_NER", filename)
    convert(filepath, NER_out)

def convert_resources():
  if "Resources" not in os.listdir():
    # If resources have not been unpacked, unpack them
    import tarfile
    tar = tarfile.open("resources.tar.gz", "r:gz")
    tar.extractall()
    tar.close()
  
  out = "ConvertedResources"
  os.mkdir(out)
  convert_tagger(out)
  print("\nResources for the tagger converted.\n")
  convert_parser(out)
  print("\nResources for the parser converted.\n")
  convert_ner(out)
  print("\nResources for the NER component converted.\n")


if __name__ == "__main__":
    plac.call(convert_resources)
