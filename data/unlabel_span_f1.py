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
            curEnts.append(line.split('\t')[2][0])
    return ents

def toSpans(tags):
    spans = set()
    for beg in range(len(tags)):
        if tags[beg][0] == 'B':
            end = beg
            for end in range(beg+1, len(tags)):
                if tags[end][0] != 'I':
                    break
            spans.add(str(beg) + '-' + str(end))
    #print(spans)
    return spans

def getInstanceScores(predPath, goldPath):
    goldEnts = readBIO(goldPath)
    predEnts = readBIO(predPath)
    entScores = []
    tp = 0
    fp = 0
    fn = 0
    for goldEnt, predEnt in zip(goldEnts, predEnts):
        goldSpans = toSpans(goldEnt)
        #print("goldSpans", goldSpans)
        predSpans = toSpans(predEnt)
        #print("predSpans", predSpans)
        overlap = len(goldSpans.intersection(predSpans))
        #print("n_overlap", overlap)
        #print("overlap", goldSpans.intersection(predSpans))
        tp += overlap
        fp += len(predSpans) - overlap
        fn += len(goldSpans) - overlap
        
    prec = 0.0 if tp+fp == 0 else tp/(tp+fp)
    rec = 0.0 if tp+fn == 0 else tp/(tp+fn)
    f1 = 0.0 if prec+rec == 0.0 else 2 * (prec * rec) / (prec + rec)
    return f1