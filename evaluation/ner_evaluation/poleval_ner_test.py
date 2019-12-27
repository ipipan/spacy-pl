import sys, json, getopt
from dateutil import parser

def overlap(offsetsa, offsetsb):
    try:
        start1, end1 = offsetsa.split('_')
        start2, end2 = offsetsb.split('_')
    except ValueError:
        print(offsetsa)
        print(offsetsb)
    return not (int(end1) < int(start2) or int(end2) < int(start1))

def exact(offsetsa, offsetsb):
    try:
        start1, end1 = offsetsa.split('_')
        start2, end2 = offsetsb.split('_')
    except ValueError:
        print(offsetsa)
        print(offsetsb)
    return (int(start1) == int(start2)) and (int(end1) == int(end2))

# this to ensure we get rid of derived types when loading entities (redundant otherwise)
def removeDerivs(annots):
    return { (a,c) for a,c in annots if c.find('derivType') < 0 }

def compareTextsOverlap(eGold, eModel):
    eGold = removeDerivs(eGold)
    eModel = removeDerivs(eModel)
    tp, fp, fn = 0, 0, 0
    for (offsets_gold, cat_gold) in eGold:
        for (offsets_model, cat_model) in eModel:
            if overlap(offsets_gold, offsets_model) and cat_gold == cat_model:
                tp += 1
                break
    fp = len(eModel) - tp
    fn = len(eGold) - tp
    return [tp, fp, fn]

def compareTextsExact(eGold, eModel):
    eGold = removeDerivs(eGold)
    eModel = removeDerivs(eModel)
    tp, fp, fn = 0, 0, 0
    for (offsets_gold, cat_gold) in eGold:
        for (offsets_model, cat_model) in eModel:
            if exact(offsets_gold, offsets_model) and cat_gold == cat_model:
                tp += 1
                break
    fp = len(eModel) - tp
    fn = len(eGold) - tp
    return [tp, fp, fn]

def makeAnnsFormat(inputDoc, cols, htype):
    z_anns = []
    for ben in inputDoc.split('\n'):
        pcs = ben.split('\t')
        try:
            if len(pcs)==cols:
                cat, ofrom, oto = pcs[-2].split(' ')
                z_anns.append( [ofrom+"_"+oto,  cat] )
        except ValueError:
            # handling fragmented entity, two strategies:
            if htype=='merge':
                # take start and end, use as a single big entity
                cat, ofrom, ignored, oto = pcs[-2].split(' ')
                z_anns.append( [ofrom+"_"+oto,  cat] )
            if htype=='split':
                # split into two entities
                catAndOffsets1, offsets2 = pcs[-2].split(';')
                cat, ofrom, oto = catAndOffsets1.split(' ')
                z_anns.append( [ofrom+"_"+oto,  cat] )
                ofrom, oto = offsets2.split(' ')
                z_anns.append( [ofrom+"_"+oto,  cat] )            
    return z_anns

# compute micro F1 scores for exact and overlap matches
# htype parameter reflects two possible strategies for handling fragmented entities ("split" or "merge")
def computeScores(goldfile, userfile, htype="split"):

    global_tp_ov = 0 ; global_fp_ov = 0 ; global_fn_ov = 0
    global_tp_ex = 0 ; global_fp_ex = 0 ; global_fn_ex = 0

    idsToAnnsUser = {}
    with open(userfile) as json_data:
        userjson = json.load(json_data)
        for nr in range(len(userjson)):
            # id = 'PCCwR-1.1-TXT/short/Inne teksty pisane/722.txt'
            if 'answers' in userjson[nr]:
                idsToAnnsUser[userjson[nr]['id']] = userjson[nr]['answers']
            else:
                idsToAnnsUser[userjson[nr]['id']] = ''

    found = 0;
    nonfound = 0

    idsToAnnsGold = {}
    with open(goldfile) as json_data:
        goldjson = json.load(json_data)

    for nr in range(len(goldjson['questions'])):
        idGold = '/'.join(goldjson['questions'][nr]['input']['fname'].split('/')[4:])
        # print(idGold)
        if idGold in idsToAnnsUser:
            found += 1
            # find the most recent answer:
            if len(goldjson['questions'][nr]['answers']) > 1:
                maximum = parser.parse('1900-01-02T14:22:41.439308+00:00');
                index = 0
                for i, value in enumerate(goldjson['questions'][nr]['answers']):
                    value = parser.parse(goldjson['questions'][nr]['answers'][i]['created'])
                    if value > maximum:
                        maximum = value
                        index = i
                idsToAnnsGold[idGold] = goldjson['questions'][nr]['answers'][index]['data']['brat']
            else:
                idsToAnnsGold[idGold] = goldjson['questions'][nr]['answers'][0]['data']['brat']

                # overlap scores:
                ovtp = compareTextsOverlap(makeAnnsFormat(idsToAnnsGold[idGold], 3, htype),
                                           makeAnnsFormat(idsToAnnsUser[idGold], 2, htype))
                global_tp_ov += ovtp[0]
                global_fp_ov += ovtp[1]
                global_fn_ov += ovtp[2]

                # exact match scores:
                extp = compareTextsExact(makeAnnsFormat(idsToAnnsGold[idGold], 3, htype),
                                         makeAnnsFormat(idsToAnnsUser[idGold], 2, htype))
                global_tp_ex += extp[0]
                global_fp_ex += extp[1]
                global_fn_ex += extp[2]

        # id not found
        else:
            nonfound += 1

    print(userfile)
    print("Nr of documents identified by ID in both data sets: "+str(found)+", not identified (left out): "+str(nonfound))

    prec = float(global_tp_ov) / float(global_fp_ov + global_tp_ov)
    recall = float(global_tp_ov) / float(global_fn_ov + global_tp_ov)
    f1 = float(2 * prec * recall) / float(prec + recall)
    print("OVERLAP precision: %0.3f recall: %0.3f F1: %0.3f " %( prec, recall, f1))

    prec = float(global_tp_ex) / float(global_fp_ex + global_tp_ex)
    recall = float(global_tp_ex) / float(global_fn_ex + global_tp_ex)
    f1 = float(2 * prec * recall) / float(prec + recall)
    print("EXACT precision: %0.3f recall: %0.3f F1: %0.3f " %( prec, recall, f1))





def main(argv):

    goldfile = 'POLEVAL-NER_GOLD.json'
    userfile = ''
    try:
        opts, args = getopt.getopt(argv, "g:u:h", ["goldfile=", "userfile="])
    except getopt.GetoptError:
        print('poleval_ner_test.py -g <inputfile> -u <userfile>')
        sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
        print('poleval_ner_test.py -g <goldfile> -u <userfile>')
        sys.exit()
      elif opt in ("-u", "--userfile"):
        userfile = arg
      elif opt in ("-g", "--goldfile"):
        goldfile = arg

    print('gold file is: ' + goldfile)
    print('user file is: '+ userfile)

    computeScores(goldfile, userfile, htype="split")

if __name__ == "__main__":
    main(sys.argv[1:])
