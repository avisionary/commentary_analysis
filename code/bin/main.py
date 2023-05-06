import argparse
from utils.sliding_window_rs import SlidingWindow
from utils.extractive_sum_rs import ExtractiveSum
from utils.abstractive_sum_rs import T5Sum
from utils.rouge_score import RougeScore

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code to make corpus "
                                                 "for Football Match Summarization")
    parser.add_argument("-f", "--indir", required=True, help="Data directory")
    args = parser.parse_args()

    slide_window = SlidingWindow(args.indir)
    comm_list = slide_window.create_window()
    all_ft_comm = slide_window.get_full_match_summ()

    extract_sum = ExtractiveSum(comm_list)
    spacy_comm = extract_sum.get_spacy_sum()
    spacy_comm_joined = []
    for comms in spacy_comm:
        spacy_comm_joined.append(" ".join(comms))

    nltk_comm = extract_sum.get_nltk_sum()

    abstract_sum = T5Sum(spacy_comm)
    t5_comm = abstract_sum.get_all_comm_t5()

    r_score = RougeScore()
    r_score_spacy = r_score.get_rouge_score(
        all_ft_comm, spacy_comm_joined, 'spacy')
    r_score_nltk = r_score.get_rouge_score(all_ft_comm, nltk_comm, 'nltk')
    r_score_t5 = r_score.get_rouge_score(all_ft_comm, t5_comm, 'T5')