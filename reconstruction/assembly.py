import os
import plac
import shutil
import json
from spacy import cli

def assemble_model(version_string = "0.1"):
  # Copying the basis of the model
  shutil.copytree("BaseModel", "Model")

  # Moving the pipeline components
  tagger_model_path = os.path.join("Tagger", "model-best", "tagger")
  tagger_endpath = os.path.join("Model", "tagger")
  os.rename(tagger_model_path, tagger_endpath)
  tagger_meta_file = open(os.path.join("Tagger", "model-best", "meta.json"), "r", encoding = "utf-8")
  tagger_meta = json.load(tagger_meta_file)
  tagger_meta_file.close()
  tagger_acc = tagger_meta["accuracy"]
  tag_labels = tagger_meta["labels"]["tagger"]
  shutil.rmtree("Tagger")
  
  parser_model_path = os.path.join("Parser", "model-best", "parser")
  parser_endpath = os.path.join("Model", "parser")
  os.rename(parser_model_path, parser_endpath)
  parser_meta_file = open(os.path.join("Parser", "model-best", "meta.json"), "r", encoding = "utf-8")
  parser_meta = json.load(parser_meta_file)
  parser_meta_file.close()
  parser_acc = parser_meta["accuracy"]
  shutil.rmtree("Parser")

  ner_model_path = os.path.join("NER", "model-best", "ner")
  ner_endpath = os.path.join("Model", "ner")
  os.rename(ner_model_path, ner_endpath)
  ner_meta_file = open(os.path.join("NER", "model-best", "meta.json"), "r", encoding = "utf-8")
  ner_meta = json.load(ner_meta_file)
  ner_meta_file.close()
  ner_acc = ner_meta["accuracy"]
  ner_labels = ner_meta["labels"]["ner"]
  shutil.rmtree("NER")

  #rewriting meta
  metafile = open(os.path.join("Model", "meta.json"), "r", encoding = "utf-8")
  meta = json.load(metafile)
  metafile.close()
  meta["pipeline"] = ['tagger', 'parser', 'ner']
  meta["version"] = version_string
  meta["author"] = "Ryszard Tuora and Łukasz Kobyliński,\
at Institute of Computer Science, Polish Academy of Sciences"
  meta["email"] = "ryszardtuora@gmail.com"
  meta["url"] = r"https://github.com/ipipan/spacy-pl"
  meta["license"] = "GNU GPL 3.0"
  meta["accuracy"] = {}
  meta["accuracy"]["tags_acc"] = tagger_acc["tags_acc"]
  meta["accuracy"]["uas"] = parser_acc["uas"]
  meta["accuracy"]["las"] = parser_acc["las"]
  meta["accuracy"]["ents_p"] = ner_acc["ents_p"]
  meta["accuracy"]["ents_r"] = ner_acc["ents_r"]
  meta["accuracy"]["ents_f"] = ner_acc["ents_f"]
  meta["accuracy"]["ents_per_type"] = ner_acc["ents_per_type"]
  meta["labels"]["tagger"] = tag_labels
  meta["labels"]["ner"] = ner_labels
  metafile = open(os.path.join("Model", "meta.json"), "w", encoding = "utf-8")  
  json.dump(meta, metafile)
  metafile.close()

  
  #integrating the lemmatizer
  if "Lemmatizer" not in os.listdir():
    # If resources have not been unpacked, unpack them
    import tarfile
    tar = tarfile.open("Lemmatizer.tar.gz", "r:gz")
    tar.extractall()
    tar.close()
  
  modelname = "pl_model-{}".format(meta["version"])
  new_path = os.path.join("Model", modelname)
  os.rename("Model", modelname)
  os.mkdir("Model")
  os.rename(modelname, new_path)
  shutil.copytree("Lemmatizer", os.path.join("Model", "Lemmatizer"))
  shutil.copy("model__init__.py", os.path.join("Model", "__init__.py"))
  meta_path = os.path.join("Model", "pl_model-{}".format(meta["version"]), "meta.json")
  shutil.copy(meta_path, os.path.join("Model", "meta.json"))
  print("\nAssembly done\n")
   
if __name__ == "__main__":
    plac.call(assemble_model)
