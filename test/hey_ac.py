import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tree import Tree
from utils import *
from textblob import TextBlob

class HeyAC:
    def __init__(self, grammar_path):
        self.lemmatizer = WordNetLemmatizer()
        self.grammar = nltk.CFG.fromstring(open(grammar_path, "r"))
        self.parser = nltk.RecursiveDescentParser(self.grammar)

    def classify(self):
        '''
        Classifies the intent from the pruned text
        '''
        raise NotImplementedError()

    def prune(self, text):
        '''
        Prunes the important words from the raw text
        '''
        processed_text, list_var = HeyAC._preprocess(text)
        parse_trees = self._parse(processed_text)
        harvest = self._prune(parse_trees)
        return harvest 

    def _prune(self, parse_trees):
        '''
        Prunes the important words from the parse tree
        '''

        harvest = {
                'NN_PROP':[],
                'NN_OBJ':[],
                'VB':[],
                'NEG':[],
                'JJ':[],
                }
        
        if len(parse_trees) > 1:
            print('[WARNING] More than a single parse detected')

        parse_tree = parse_trees[0]

        for sub_tree in parse_tree.subtrees():
            label = sub_tree.label()
            if label in harvest.keys():
                harvest[label] = sub_tree.leaves()

        return harvest

    def _parse(self, text):
        '''
        Syntactically parses text
        '''
        tokens = HeyAC._tokenize(text)
        parse_trees = list(self.parser.parse(tokens))
        return parse_trees

    @staticmethod
    def _preprocess(text):
        ''' 
        Preprocess the text
            1. Converting numbers and variables to a dummy word "hey_num"
            2. Converting all the letters to lowercase
            3. Correcting any spelling mistakes
        '''
        processed_text = HeyAC._word_to_digit(text)
        processed_text, list_var = HeyAC._digit_to_dummy(processed_text)
        processed_text = TextBlob(processed_text)
        processed_text = processed_text.lower()
        processed_text = processed_text.correct()
        processed_text = str(processed_text)

        return processed_text, list_var

    @staticmethod
    def _word_to_digit(text):
        '''
        Convert text to digit
            "Set the temperature to twenty degrees" -> "Set the temperature to 20 degrees"
        '''
        is_var, processed_text = check_var(text)
        return processed_text
    
    @staticmethod
    def _digit_to_dummy(text):
        '''
        Convert digit to a dummy word "hey_num" and returns the list of variables
            "Set the temperature to 20 degrees" -> "Set the temperature to hey_num degrees"
        '''
        text_split = text.split()
        text_split_dummy = [ "hey_num" if i.isdigit() else i for i in text_split]
        list_var = [i for i in text_split if i.isdigit()]
        processed_text = ' '.join(text_split_dummy)
        return processed_text, list_var
    
    @staticmethod
    def _tokenize(text):
        '''
        Splits the text into a list of words
        '''
        tokens = text.split(' ')
        return tokens


class hey_ac():
    def __init__(self, sent, grammar, var=False):
        self.orig_sent = sent
        self.sent = None
        self.grammar = grammar
        
        # Convert words to numbers
        self.var = var
        if self.var == True:
            self.sent = self.sent.split()
            self.sent = [ "hey_num" if i.isdigit() else i for i in self.sent]
            self.sent = ' '.join(self.sent)
        
        self.parsed = TextBlob(self.sent)
        self.parsed = self.parsed.lower() #Increase TeMpeRATure -> increase temperature

        self.parsed = self.parsed.correct() # increese -> increase
        
        self.sent_prep = []

    def lemmatization(self):
        # Lemmatization
        for i in range(len(self.parsed.words)):
            # lemmatization: colder -> cold 
            # pos = 'a' --> adj, 'v' --> verb, 'n' -> noun
            lemma = lemmatizer.lemmatize(self.parsed.words[i], pos ='a')
            lemma = lemmatizer.lemmatize(lemma, pos ='v')
            lemma = lemmatizer.lemmatize(lemma, pos ='n')
            # lemmatization: increases -> increase
            lemma = lemmatizer.lemmatize(lemma)
            self.sent_prep.append(lemma)
        
        # if contains 'please', remove
        if 'please' in self.sent_prep:
            self.sent_prep.remove('please')
            return self.sent_prep
        else:
            return self.sent_prep
    
    def wordnet(self, to_parse):
        sent_wordnet = []
        self.sent_wordnet_orig = len(to_parse)
        for word in to_parse:
            for k,v in verb_net.items():
                if word in v:
                    sent_wordnet.append(k)
                else:
                    pass
            for k,v in noun_net.items():
                if word in v:
                    sent_wordnet.append(k)
                else:
                    pass
            for k,v in adj_net.items():
                if word in v:
                    sent_wordnet.append(k)
                else:
                    pass
            if word in ["the","a","an","off","down","up", "on","to","hey_num","by", "from","a.m","at", "pm", "o'clock"]:
                sent_wordnet.append(word)
        if len(sent_wordnet) != self.sent_wordnet_orig:
            raise Exception("Sorry I do not understand you")
        else:
            return sent_wordnet
    
    
    def check(self):
        self.to_parse = self.lemmatization()
        self.to_parse = self.wordnet(self.to_parse)      
        rd_parser = nltk.RecursiveDescentParser(self.grammar)
        try:
            for p in rd_parser.parse(self.to_parse):
                if var == True:
                    numbers = [i for i in split([self.orig_sent]) if i.isdigit()]
                    for n in numbers:
                        p = str(p).replace('hey_num', n, 1)
                        self.to_parse = str(self.to_parse).replace('hey_num', n, 1)
                        self.to_parse = self.to_parse.strip('][').split(', ')

                return self.to_parse, p
        except:
            raise Exception("Sorry I do not understand you")
            
            
    # Pruning 
    def classify_me(self):
        to_prune, p = self.check()
        VB = []
        NN = []
        CO = []
        RP = []
        for i in Tree.fromstring(str(p)).subtrees():
            if i.label() == 'VB':
                VB.append(i.leaves()[0])
            elif i.label() == 'NN':
                NN.append(i.leaves()[0])
            elif i.label() == 'CO':
                CO.append(i.leaves()[0])
            elif i.label() == 'RP':
                RP.append(i.leaves()[0])
        print('Use me to classify: ')
        print('VB', VB)
        print('NN', NN)
        print('CO', CO)
        print('RP', RP)
