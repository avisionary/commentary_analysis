import nltk
from nltk.tokenize import sent_tokenize
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

import re
import string

import warnings
warnings.filterwarnings('ignore')

class CleanText():

    def __init__(self):
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        # Making a regex pattern to match in the characters we would like to replace from the words
        character_replace = ",()0123456789.?!@#$%&;*:_,/" 
        self.pattern = "[" + character_replace + "]"

    def remove_punct(text):
        """ A method to remove punctuations from text """
        text  = "".join([char for char in text if char not in string.punctuation])
        return re.sub('[0-9]+', '', text) #removes numbers from text
    
    def tokenization(text):
        """ A method to tokenize text data """
        return re.split('\W+', text) #splitting each sentence/ tweet into its individual words

    def remove_stopwords(self, text):
        """ A method to remove all the stopwords """
        return [word for word in text if word not in self.stopwords]

    def stemming(text):
        """ A method to perform stemming on text data"""
        return [nltk.PorterStemmer().stem(word) for word in text]
    
    def lemmatizer(text):
        return [nltk.WordNetLemmatizer().lemmatize(word) for word in text]

    # Making a common cleaning function for every part below for code reproducability
    def clean_text(self, list_words):
        new_list_words = []

        # Looping through every word to remove the characters and appending back to a new list
        # replace is being used for the characters that could not be catched through regex
        for s in list_words:
            new_word = s.lower()
            new_word = re.sub(self.pattern,"",new_word)
            new_word = new_word.replace('[', '')
            new_word = new_word.replace(']', '')
            new_word = new_word.replace('-', '')
            new_word = new_word.replace('—', '')
            new_word = new_word.replace('“', '')
            new_word = new_word.replace("’", '')
            new_word = new_word.replace("”", '')
            new_word = new_word.replace("‘", '')
            new_word = new_word.replace('"', '')
            new_word = new_word.replace("'", '')
            new_word = new_word.replace(" ", '')
            new_list_words.append(new_word)

        # Using filter to remove empty strings
        return list(filter(None, new_list_words))

    def clean_corpus(self, text):
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)

        # Remove punctuation
        text_punct_removed = self.remove_punct(text)

        # Tokenize the sentences into words and remove stopwords
        words = self.tokenization(text_punct_removed.lower())
        
        # remove stopwords
        filtered_words = self.remove_stopwords(words)
        
        # Apply stemming to the filtered words
        stemmed_words = self.stemming(filtered_words)

        # Apply lemmatization to the stemmed words
        words_lemmatized = self.lemmatizer(stemmed_words)

        # apply the common cleaning function
        cleaned_words = self.clean_text(words_lemmatized)

        return sentences, cleaned_words