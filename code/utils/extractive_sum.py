from utils.spacy_sum_rs import SpacySum
from utils.nltk_sum_rs import NltkSum

import warnings
warnings.filterwarnings('ignore')

class ExtractiveSum():

    def __init__(self, list_comms):
        self.commentaries = list_comms

    def get_spacy_sum(self):
        return SpacySum().get_all_comm_spacy(self.commentaries)
        # spacy_comm_joined = []
        # for comms in spacy_comm:
        #     spacy_comm_joined.append(" ".join(comms))
        # return spacy_comm
        
    def get_nltk_sum(self):
        return NltkSum().get_all_comm_nltk(self.commentaries)