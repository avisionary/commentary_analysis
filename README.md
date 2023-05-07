# Soccer Match Summarization
This is a project that focuses on summarizing soccer matches using data scraped from goal.com. The goal of this project is to extract key information from match reports and generate a summary that captures the essence of the game.

## Usage

1. Clone the repository to your local machine.

2. Go to the terminal and navigate to the directory where the repository is located.

3. Create a new environment using the `environment.yml` file. This can be done by running the following command:<br>
            `conda env create -f environment.yml`

4. Activate the new environment.
    
5. Install the soccer_match_summarization library by running the following command:
            `pip install -e .`

## Command Line Arguments
The following command line arguments are supported:
1. For the Naive Bayes' Classifier:
    - `-f` or `--indir`: The path to the input directory containing the training data (required).
2. For the Inverted Index Builder:
    - `-f` or `--filepath`: The path to the collection of documents (required and should be an xml file).
    - `-t` or `--tokenizer`: The tokenizer to use. The options are `whitespace`, `nltk` or `ngrams` (required).
    - `-s` or `--stem`: A flag to indicate whether to stem the words or not. If this flag is present, the words will be stemmed. If this flag is not present, the words will not be stemmed. (optional).

## Data Description
The dataset used in this project is scraped from goal.com using web scraping tools such as Beautiful Soup and Requests. The data includes minute by minute live ticker for any match link from goal.com. The data is stored in a csv file.

## Directory Structure
.
├── LICENSE
├── README.md
├── __init__.py
├── app.py
├── code
│   ├── Formation_Analysis.ipynb
│   ├── __init__.py
│   ├── bin
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── main.py
│   ├── model_test.ipynb
│   ├── tests
│   │   ├── __init__.py
│   │   ├── data
│   │   │   └── temp.rtf
│   │   └── test_code.py
│   └── utils
│       ├── __init__.py
│       ├── abstractive_sum.py
│       ├── clean_data.py
│       ├── collect_data.py
│       ├── extractive_sum.py
│       ├── formation_analysis_aa.ipynb
│       ├── multiple_scraping.ipynb
│       ├── munging_aa.ipynb
│       ├── nltk_sum.py
│       ├── rouge_score.py
│       ├── scraping.py
│       ├── scraping_check_aa.ipynb
│       ├── sliding_window.py
│       └── spacy_sum.py
├── data
│   ├── cl_data_21_22 _stage_leg.csv
│   ├── cl_data_21_22.csv
│   ├── cl_match_links_21_22.csv
│   ├── commentory.csv
│   ├── commentory_matchid.csv
│   ├── formation_subs.csv
│   ├── key_events.csv
│   ├── key_events2.csv
│   ├── temp.rtf
│   └── temp_data.csv
├── environment.yml
├── figures
│   ├── images
│   │   ├── pitch.jpeg
│   │   └── temp.rtf
│   └── plots
│       └── temp.rtf
├── pytest.ini
└── setup.py




