import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

import warnings
warnings.filterwarnings('ignore')

class SpacySum():

    def __init__(self):
        self.pipe = spacy.load("en_core_web_sm")

    def get_spacy_summary(self, text, pipe):
        doc = self.pipe(text)

        keyword = []
        stopwords = list(STOP_WORDS)
        pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
        for token in doc:
            if (token.text in stopwords or token.text in punctuation):
                continue
            if token.pos_ in pos_tag:
                keyword.append(token.text)

        freq_word = Counter(keyword)
        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)

        sent_strenght = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strenght.keys():
                        sent_strenght[sent] += freq_word[word.text]
                    else:
                        sent_strenght[sent] = freq_word[word.text]

        summarized_sentences = nlargest(3, sent_strenght, key=sent_strenght.get)
        final_sentences = [w.text for w in summarized_sentences]
        return " ".join(final_sentences)
    
    def get_all_comm_spacy(self, comms):
        all_comm_spacy = []
        for commentary in comms:
            spacy_window_comm = []
            for comment in commentary:
                spacy_window_comm.append(self.get_spacy_summary(comment))
                all_comm_spacy.append(spacy_window_comm)
        return all_comm_spacy