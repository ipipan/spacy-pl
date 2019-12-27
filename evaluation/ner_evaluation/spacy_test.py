import spacy
import json



model_name = input("Please input the name of the model to be loaded: ")

nlp = spacy.load(model_name)
nlp.disable_pipes("tagger")
nlp.disable_pipes("parser")


test_file = open("poleval_test_ner_2018.json", "r", encoding = "utf-8")
test_obj = json.load(test_file)
test_file.close()


for example in test_obj:
  par = example["text"]
  doc = nlp(par)
  for ent in doc.ents:
    entz.append("{} {} {}\t{}".format(ent.label_, ent.start_char, ent.end_char, ent.text))

  out = "\n".join(entz)
  example["answers"] = out

out_file = open("{}_ner.json".format(model_name), "w", encoding = "utf-8")
json.dump(test_obj, out_file)

