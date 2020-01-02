# -*- coding: utf-8 -*-

from itertools import product

# NJKP

POS_V = ('adj', 'adja', 'adjc', 'adjp', 'adv', 'aglt', 'bedzie', 'brev', 'burk', 'comp', 'conj', 'depr', 'fin', 'ger', 'ign', 'imps', 'impt', 'inf', 'interj', 'interp', 'num',  'numcol', 'pact', 'pacta', 'pant', 'pcon', 'ppas', 'ppron12', 'ppron3', 'praet', 'pred', 'prep', 'qub', 'siebie', 'subst', 'winien', 'xxx')
NUM_V = ('sg', 'pl', 'NONUM')
CASE_V = ('nom', 'gen', 'dat', 'acc', 'inst', 'loc', 'voc', 'NOCASE')
GEND_V = ('m1', 'm2', 'm3', 'f', 'n', 'NOGEND')
REC_V = ('rec', 'congr', 'NOREC')
PERS_V = ('pri', 'sec', 'ter', 'NOPERS')
ACC_V = ('akc', 'nakc', 'NOACC')
PRP_V = ('praep', 'npraep', 'NOPRP')
DEG_V = ('pos', 'com', 'sup', 'NODEG')
ASP_V = ('perf', 'imperf', 'NOASP')
AGL_V = ('agl', 'nagl', 'NOAGL')
VOC_V = ('wok', 'nwok', 'NOVOC')
AFF_V = ('aff', 'neg', 'NOAFF')
PUN_V = ('pun', 'npun', 'NOPUN')

TAG_GROUPS = (
    POS_V,
    NUM_V,
    CASE_V,
    GEND_V,
    REC_V,
    PERS_V,
    ACC_V,
    PRP_V,
    DEG_V,
    ASP_V,
    AGL_V,
    VOC_V,
    AFF_V,
    PUN_V,
)

VALID_POSITIONS = {
    'adj' : (NUM_V, CASE_V, GEND_V, DEG_V),
    'adja' : (),
    'adjc' : (),
    'adjp' : (),
    'adv' : ((None,) + DEG_V,),
    'aglt' : (NUM_V, PERS_V, ASP_V, VOC_V),
    'bedzie' : (NUM_V, PERS_V, ASP_V),
    'brev' : (PUN_V,),
    'burk' : (),
    'comp' : (),
    'conj' : (),
    'depr' : (NUM_V, CASE_V, GEND_V),
    'fin' : (NUM_V, PERS_V, ASP_V),
    'ger' : (NUM_V, CASE_V, GEND_V, ASP_V, AFF_V),
    'ign' : (),
    'imps' : (ASP_V,),
    'impt' : (NUM_V, PERS_V, ASP_V),
    'inf' : (ASP_V,),
    'interj' : (),
    'interp' : (),
    'num' : (NUM_V, CASE_V, GEND_V, REC_V),
    'numcol' : (NUM_V, CASE_V, GEND_V, REC_V),
    'pact' : (NUM_V, CASE_V, GEND_V, ASP_V, AFF_V),
    'pacta' : (),
    'pant' : (ASP_V,),
    'pcon' : (ASP_V,),
    'ppas' : (NUM_V, CASE_V, GEND_V, ASP_V, AFF_V),
    'ppron12' : (NUM_V, CASE_V, GEND_V, PERS_V, (None,) + ACC_V),
    'ppron3' : (NUM_V, CASE_V, GEND_V, PERS_V, (None,) + ACC_V, (None,) + PRP_V),
    'praet' : (NUM_V, GEND_V, ASP_V, (None,) + AGL_V),
    'pred' : (),
    'prep' : (CASE_V, (None,) + VOC_V),
    'qub' : ((None,) + VOC_V,),
    'siebie' : (CASE_V,),
    'subst' : (NUM_V, CASE_V, GEND_V),
    'winien' : (NUM_V, GEND_V, ASP_V),
    'xxx' : (),
}

VALID_TAGS = set()
for pos, positions in VALID_POSITIONS.items():
    for seq in product(*[p[:-1] for p in positions]):
        tag = ':'.join(filter(None, (pos,) + seq))
        VALID_TAGS.add(tag)
