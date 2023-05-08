import argparse
import pandas as pd
from utils.munging import SoccerEventExtractor
from utils.sliding_window import SlidingWindow
from utils.extractive_sum import ExtractiveSum
from utils.abstractive_sum import T5Sum
from utils.rouge_score import RougeScore
from utils.collect_data import MulitScraping
from utils.plot_rouge import PlotRouge

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Code for Football/Soccer Match Summarization")
    parser.add_argument("--scrape", required=True, help="Specifiy if you want to scrape data or use existing data")
    parser.add_argument("--links", required=True, help="Path to links file")
    parser.add_argument("--output_path", required=True, help="Path to output file")
    parser.add_argument("--t5", required=True, help="Specifiy if you want to use T5 model or not")
    parser.add_argument("--eval_plot", required=True, help="Specifiy if you want to plot the Rouge scores or not")
    args = parser.parse_args()
    
    try:
        args.scrape = int(args.scrape)
        args.t5 = int(args.t5)
        args.eval_plot = int(args.eval_plot)
        
    except:
        print("Please specify integer values for scraping, t5 and eval_plot")
    
    if args.scrape not in [0,1]:
        parser.error("Please specify 0 or 1 for scraping data")
    
    if args.scrape == 1:
        # Scrape data from goal.com
        scraper = MulitScraping(args.links, args.output_path)
        match_df = pd.read_csv(args.output_path)
        
    else:
        # Use existing data
        match_df = pd.read_csv(args.output_path)
    
    main_df = SoccerEventExtractor(match_df)
    clean_df = main_df._generate_match_ids()

    # Initialize sliding window object
    slide_window = SlidingWindow(clean_df)

    # Create window for football match summaries
    comm_list = slide_window.create_window()

    # Get full match summaries
    all_ft_comm = slide_window.get_full_match_summ()
    
    # create RougeScore object
    r_score = RougeScore()

    # Extractive summarization
    extract_sum = ExtractiveSum(comm_list)

    # Using SpaCy
    spacy_comm = extract_sum.get_spacy_sum()
    spacy_comm_joined = []
    for comms in spacy_comm:
        spacy_comm_joined.append(" ".join(comms))

    # Using NLTK
    nltk_comm = extract_sum.get_nltk_sum()
    
    print('Extractive done')

    if (args.t5 not in [0,1]):
        parser.error("Please specify 0 or 1 for using T5 model")
        
    if args.t5 == 1:
        # Abstractive summarization using T5 model
        t5_comm = T5Sum(spacy_comm).get_all_comm_t5()
        r_score_t5 = r_score.get_rouge_score(all_ft_comm, t5_comm, 'T5')
        print('Abstractive done')
    else:
        print('Abstractive not done')

    # Calculate Rouge scores
    r_score_spacy = r_score.get_rouge_score(
        all_ft_comm, spacy_comm_joined, 'spacy')
    r_score_nltk = r_score.get_rouge_score(all_ft_comm, nltk_comm, 'nltk')
    
    if (args.eval_plot not in [0,1]):
        parser.error("Please specify 0 or 1 for plotting Rouge scores")
        
    if args.eval_plot == 1:
        plt_rouge = PlotRouge()
        rouge_df = plt_rouge.extract_melt_rouge(r_score_spacy, r_score_nltk)
        
        plt_rouge.plot_uni_rouge_score(rouge_df)
        plt_rouge.plot_lcs_rouge_score(rouge_df)
    
    else:
        print('Plotting not done')

