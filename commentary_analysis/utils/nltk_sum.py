import nltk
nltk.download('omw-1.4')

from heapq import nlargest

import warnings
warnings.filterwarnings('ignore')

class NltkSum():

    def __init__(self, sentences, cleaned_words):
        self.sentences = sentences
        self.clean_words = cleaned_words

    def summarize_text_nltk(self, num_sentences=3):
        # Calculate word frequency and sentence scores
        word_freq = nltk.FreqDist(self.clean_words)
        sentence_scores = {}
        for i, sentence in enumerate(self.sentences):
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_freq:
                    if len(sentence.split()) < 30:
                        if i not in sentence_scores:
                            sentence_scores[i] = word_freq[word]
                        else:
                            sentence_scores[i] += word_freq[word]
        
        # Select the top sentences based on their scores
        summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        summary = [self.sentences[i] for i in sorted(summary_sentences)]
        return " ".join(summary)