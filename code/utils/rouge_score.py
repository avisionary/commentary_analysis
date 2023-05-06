import pandas as pd
from rouge import Rouge


class RougeScore():

    def __init__(self):
        self.rouge = Rouge()

    def get_rouge_score(self, ft_summ, pred_summ, nlp_lib):
        all_rouge = []
        for i in range(len(pred_summ)):
            all_rouge.append(self.rouge.get_scores(ft_summ[i], pred_summ[i]))
        
        combined_rouge = pd.DataFrame(columns=['uni_recall', 'uni_precision', 'uni_f1', 
                                                'bi_recall', 'bi_precision', 'bi_f1',
                                                'lcs_recall', 'lcs_precision', 'lcs_f1',
                                                'module'])

        for score in all_rouge:
            rouge1 = score[0]['rouge-1']
            rouge2 = score[0]['rouge-2']
            rouge_l = score[0]['rouge-l']

            combined_rouge = combined_rouge.append({"uni_recall": rouge1['r'], "bi_recall": rouge2['r'], "lcs_recall": rouge_l['r'],
                                        "uni_precision": rouge1['p'], "bi_precision": rouge2['p'], "lcs_precision": rouge_l['p'],
                                        "uni_f1": rouge1['f'], "bi_f1": rouge2['f'], "lcs_f1": rouge_l['f'],
                                        "module": nlp_lib}, ignore_index=True)

        return combined_rouge
