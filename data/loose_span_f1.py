import sys

def readBIO(path):
    ents = []
    curEnts = []
    for line in open(path, encoding = "utf-8"):
        line = line.strip()
        if line == '':
            ents.append(curEnts)
            curEnts = []
        elif line[0] == '#' and len(line.split('\t')) == 1:
            continue
        else:
            curEnts.append(line.split('\t')[2])
    return ents

def toSpans(tags):
    spans = set()
    for beg in range(len(tags)):
        if tags[beg][0] == 'B':
            end = beg
            for end in range(beg+1, len(tags)):
                if tags[end][0] != 'I':
                    break
            spans.add(str(beg) + '-' + str(end) + ':' + tags[beg][2:])
    # print("spans", spans)
    return spans

def getBegEnd(span):
    return [int(x) for x in span.split(':')[0].split('-')]

def getLooseOverlap(spans1, spans2):
    found = 0
    for spanIdx, span in enumerate(spans1):
        spanBeg, spanEnd = getBegEnd(span)
        #print("spanBeg", spanBeg)
        #print("spanEnd", spanEnd)
        #print("span", span)
        label = span.split(':')[1]
        #print("lbel1", label)
        match = False
        for span2idx, span2 in enumerate(spans2):
            span2Beg, span2End = getBegEnd(span2)
            label2 = span2.split(':')[1]
            #print("label2", label2)
            if label == label2:
                if span2Beg >= spanBeg and span2Beg <= spanEnd:
                    match = True
                if span2End <= spanEnd and span2End >= spanBeg:
                    match = True
        if match:
            found += 1
    #print(found)
    return found

def getInstanceScores(predPath, goldPath):
    goldEnts = readBIO(goldPath)
    predEnts = readBIO(predPath)
    #print(goldEnts)
    # print("gold", goldEnts)
    # print("pred", predEnts)
    entScores = []
    recall_tp = 0
    recall_fp = 0
    recall_fn = 0

    precision_tp = 0
    precision_fp = 0
    precision_fn = 0
    
    for goldEnt, predEnt in zip(goldEnts, predEnts):
        goldSpans = toSpans(goldEnt)
        predSpans = toSpans(predEnt)
        overlapLoose = getLooseOverlap(goldSpans, predSpans)
        recall_tp += overlapLoose
        recall_fn += len(goldSpans) - overlapLoose
        overlapLoose = getLooseOverlap(predSpans, goldSpans)
        precision_tp += overlapLoose
        precision_fp += len(predSpans) - overlapLoose
        
        # #print("predSpans", predSpans)
        # overlap = len(goldSpans.intersection(predSpans))
        # #print("n_overlap", overlap)
        # #print("overlap", goldSpans.intersection(predSpans))
        # tp += overlap
        # fp += len(predSpans) - overlap
        # fn += len(goldSpans) - overlap

    print('loose (partial overlap with same label)')
    prec = 0.0 if precision_tp + precision_fp == 0 else precision_tp/(precision_tp+precision_fp)
    rec = 0.0 if recall_tp+recall_fn == 0 else recall_tp/(recall_tp+recall_fn)
    print('l_recall:   ', rec)
    print('l_precision:', prec)
    f1 = 0.0 if prec+rec == 0.0 else 2 * (prec * rec) / (prec + rec)

    # prec = 0.0 if tp+fp == 0 else tp/(tp+fp)
    # rec = 0.0 if tp+fn == 0 else tp/(tp+fn)


    # f1 = 0.0 if prec+rec == 0.0 else 2 * (prec * rec) / (prec + rec)
    return f1



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide path to gold file and output of your system (in tab-separated format)')
        print('For example: \npython3 eval.py opener_en-dev.conll bert_out-dev.conll')
        print()
        print('The files should be in a conll-like (i.e. tab-separated) format. Each word should be on a separate line, and line breaks are indicated with an empty line. The script will assume to find the BIO annotations on the 3th column. So: index<TAB>word<TAB>label.')

    else:
        score = getInstanceScores(sys.argv[1], sys.argv[2])
        print(score)