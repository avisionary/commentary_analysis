from utils.spacy_sum import SpacySum
from utils.nltk_sum import NltkSum
from utils.clean_data import CleanText

import warnings
warnings.filterwarnings('ignore')

class ExtractiveSum():

    def __init__(self, list_comms):
        self.commentaries = list_comms

    def get_spacy_sum(self):
        return SpacySum().get_all_comm_spacy(self.commentaries)

    def get_nltk_sum(self):
        all_comm_nltk = []
        for commentary in self.commentaries:
            nltk_window_comm = []
            for comment in commentary:
                clean_comm = CleanText().clean_corpus(comment)
                nltk_window_comm.append(NltkSum(clean_comm[0], clean_comm[1]).summarize_text_nltk())
            all_comm_nltk.append(" ".join(nltk_window_comm))
        return all_comm_nltk