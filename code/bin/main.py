import argparse
from utils.sliding_window import SlidingWindow
from utils.extractive_sum import ExtractiveSum
from utils.abstractive_sum import T5Sum
from utils.rouge_score import RougeScore

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Code for Football/Soccer Match Summarization")
    parser.add_argument("-f", "--indir", required=True, help="Data directory")
    args = parser.parse_args()

    # Initialize sliding window object
    slide_window = SlidingWindow(args.indir)

    # Create window for football match summaries
    comm_list = slide_window.create_window()

    # Get full match summaries
    all_ft_comm = slide_window.get_full_match_summ()

    # Extractive summarization
    extract_sum = ExtractiveSum(comm_list)

    # Using SpaCy
    spacy_comm = extract_sum.get_spacy_sum()
    spacy_comm_joined = []
    for comms in spacy_comm:
        spacy_comm_joined.append(" ".join(comms))

    # Using NLTK
    nltk_comm = extract_sum.get_nltk_sum()

    # Abstractive summarization using T5 model
    t5_comm = T5Sum(spacy_comm).get_all_comm_t5()

    # Calculate Rouge scores
    r_score = RougeScore()
    r_score_spacy = r_score.get_rouge_score(
        all_ft_comm, spacy_comm_joined, 'spacy')
    r_score_nltk = r_score.get_rouge_score(all_ft_comm, nltk_comm, 'nltk')
    r_score_t5 = r_score.get_rouge_score(all_ft_comm, t5_comm, 'T5')