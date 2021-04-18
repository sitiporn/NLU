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

    def parse(self, text):
        processed_text, list_var = HeyAC._preprocess(text)
        parse_trees = self._parse(processed_text)
        return parse_trees

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
