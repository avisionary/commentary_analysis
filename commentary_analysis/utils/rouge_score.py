import pandas as pd
from rouge import Rouge


class RougeScore():
    """
    Class to calculate ROUGE scores for summarization evaluation.
    """

    def __init__(self):
        """
        Initialize the RougeScore object.
        """
        self.rouge = Rouge()

    def get_rouge_score(self, ft_summ, pred_summ, nlp_lib):
        """
        Calculate ROUGE scores for the given full-time summaries and predicted summaries.

        Parameters:
        - ft_summ (list): List of full-time summaries.
        - pred_summ (list): List of predicted summaries.
        - nlp_lib (str): Name of the NLP library used (e.g., 'spacy', 'nltk', 'T5').

        Returns:
        - pandas.DataFrame: DataFrame containing the ROUGE scores for each summary.
        """

        # List to store rouge scores
        all_rouge = []
        # Calculate rouge score
        for i in range(len(pred_summ)):
            all_rouge.append(self.rouge.get_scores(ft_summ[i], pred_summ[i]))
        
        # Create a dataframe that will be used to store the unigram, bigram and lcs rouge scores
        combined_rouge = pd.DataFrame(columns=['uni_recall', 'uni_precision', 'uni_f1', 
                                                'bi_recall', 'bi_precision', 'bi_f1',
                                                'lcs_recall', 'lcs_precision', 'lcs_f1',
                                                'module'])

        for score in all_rouge:
            # Unigram
            rouge1 = score[0]['rouge-1']
            # Bigram
            rouge2 = score[0]['rouge-2']
            # LCS
            rouge_l = score[0]['rouge-l']
        
            # Append values to the above created dataframe
            combined_rouge = combined_rouge.append({"uni_recall": rouge1['r'], "bi_recall": rouge2['r'], "lcs_recall": rouge_l['r'],
                                        "uni_precision": rouge1['p'], "bi_precision": rouge2['p'], "lcs_precision": rouge_l['p'],
                                        "uni_f1": rouge1['f'], "bi_f1": rouge2['f'], "lcs_f1": rouge_l['f'],
                                        "module": nlp_lib}, ignore_index=True)

        return combined_rouge
