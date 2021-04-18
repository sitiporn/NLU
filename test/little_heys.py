def split(lst):
    return ([i for item in lst for i in item.split()])
      
def convert_n2int(x):
     try:
        return int(x)
     except ValueError:
        return x
    
def convert_w2n (textnum, numwords={}):
    
    replace = True
    
    units = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight","nine", "ten",          "eleven","twelve","thirteen","fourteen", "fifteen","sixteen", "seventeen", "eighteen", "nineteen"]
    
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]
    
    if not numwords:
        units = units

        tens = tens

        scales = scales

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):  numwords[word] = (1, idx)
        for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y'), ('th', '')]
    
    textnum_split = split([textnum])
    idx = []
    for i in range(len(textnum_split)):
        check_text = textnum_split[i]
        if "-" in check_text:
            idx.append(i)
            
    for i in idx:
        to_find = textnum_split[i].split('-')
        if to_find[0] in tens:
            textnum_split[i] = " ".join(to_find)
        else:
            textnum_split[i] = "-".join(to_find)
    textnum = ' '.join(textnum_split)

    current = result = 0
    curstring = ""
    onnumber = False
    for word in textnum.split():
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in numwords:
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
            else:
                scale, increment = numwords[word]

                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True

    if onnumber:
        curstring += repr(result + current)

    return curstring

def check_var(sent):
    sent = convert_w2n(sent)
    sent = split([sent])
    a = [convert_n2int(sent[j]) for j in range(len(sent))]
    check_int = []
    for elem in a:
        if type(elem)== int:
            check_int.append(True)
        else:
            check_int.append(False)
    if True in check_int:
        return True, ' '.join(sent)
    else:
        return False, ' '.join(sent) 
