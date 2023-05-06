from utils import spacy_sum_rs, nltk_sum_rs

import warnings
warnings.filterwarnings('ignore')

class ExtractiveSum():

    def __init__(self, list_comms):
        self.commentaries = list_comms

    def get_spacy_sum(self):
        spacy_comm = spacy_sum_rs.SpacySum().get_all_comm_spacy(self.commentaries)
        spacy_comm_joined = []
        for comms in spacy_comm:
            spacy_comm_joined.append(" ".join(comms))
        
    def get_nltk_sum(self):
        return nltk_sum_rs.NltkSum().get_all_comm_nltk(self.commentaries)