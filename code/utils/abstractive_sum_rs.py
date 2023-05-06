import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

import warnings
warnings.filterwarnings('ignore')


class T5Sum():

    def __init__(self, list_comms):
        self.commentaries = list_comms
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.device = torch.device('cpu')

    def summarize_text_t5(self, text):
        preprocess_text = text.strip().replace("\n","")
        t5_prepared_Text = "summarize: "+preprocess_text
        tokenized_text = self.tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(self.device)

        # summmarize 
        summary_ids = self.model.generate(tokenized_text,
                                            num_beams=4,
                                            no_repeat_ngram_size=2,
                                            min_length=30,
                                            max_length=100,
                                            early_stopping=True)

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def get_all_comm_t5(self, comms):
        all_comm_t5 = []
        for commentary in comms:
            t5_window_comm = []
            for comment in commentary:
                summary = self.summarize_text_t5(comment)
                t5_window_comm.append(summary)
            all_comm_t5.append(" ".join(t5_window_comm))
        return all_comm_t5

    # goes into driver code
    # t5_comm = get_all_comm_t5(spacy_comm)
