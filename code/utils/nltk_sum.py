import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.translate import bleu
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

import re
import string

from heapq import nlargest

import warnings
warnings.filterwarnings('ignore')

class NltkSum():

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def remove_punct(self, text):
        """ A method to remove punctuations from text """
        text  = "".join([char for char in text if char not in string.punctuation])
        text = re.sub('[0-9]+', '', text) #removes numbers from text
        return text
    
    def tokenization(self, text):
        """ A method to tokenize text data """
        text = re.split('\W+', text) #splitting each sentence/ tweet into its individual words
        return text

    def summarize_text_nltk(self, text, num_sentences=3):
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Tokenize the sentences into words and remove stopwords
        text_punct_removed = self.remove_punct(text)
        words = self.tokenization(text_punct_removed.lower())
        
        # remove stopwords
        filtered_words = [word for word in words if word not in self.stop_words]
        
        # Apply stemming to the filtered words
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in filtered_words]
        
        # Calculate word frequency and sentence scores
        word_freq = nltk.FreqDist(stemmed_words)
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_freq:
                    if len(sentence.split()) < 30:
                        if i not in sentence_scores:
                            sentence_scores[i] = word_freq[word]
                        else:
                            sentence_scores[i] += word_freq[word]
        
        # Select the top sentences based on their scores
        summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        summary = [sentences[i] for i in sorted(summary_sentences)]
        return " ".join(summary)
    
    def get_all_comm_nltk(self, comms):
        all_comm_nltk = []
        for commentary in comms:
            nltk_window_comm = []
            for comment in commentary:
                nltk_window_comm.append(self.summarize_text_nltk(comment))
            all_comm_nltk.append(" ".join(nltk_window_comm))
        return all_comm_nltk