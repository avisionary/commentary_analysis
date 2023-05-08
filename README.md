# Soccer Match Summarization
This is a project that focuses on summarizing soccer matches using data scraped from goal.com. The goal of this project is to extract key information from match reports and generate a summary that captures the essence of the game.

## Usage

1. Clone the repository to your local machine.

2. Go to the terminal and navigate to the directory where the repository is located.

3. Create a new environment using the `environment.yml` file. This can be done by running the following command:<br>
            `conda env create -f environment.yml`

4. Activate the new environment.

5. Navigate to the commentary_analysis directory and install the commentary_analysis library by running the following command:
            `pip install -e .`

6. Run the main.py according to your preferences:
    - For scraping the code for the entire Champions League 2021-22 and getting Abstractive and Extractive Summaries for all commentaries and Plotting their Rouge scores run:
            `python3 bin/main.py --links "../data/" --output_path "../data/commentary_new.csv" --t5 1 --scrape 1 --eval_plot 1`

    Remember that scraping and running Abstractive Summaries take a lot of time since it used T5 model to summarize each match.

7. To use the User Interface navigate to the main repository directory and run:
            `streamlit run app.py`
    
    You can enter any "goal.com" links and get the formation and summary of that match.

## Command Line Arguments
The following command line arguments are supported:
- `--links`: The path to the collection of links (Required and should be in double quotes and a csv file).
- `--output_path`: The path to the where the scraped data will be stored (Required and should be in double quotes and end with .csv).
- `--scrape`: A flag to indicate whether the data should be scraped (1) or not (0). Disclaimer: It takes time to run this model and hence not advised. (Required)
- `--t5`: A flag to indicate whether Abstractive Summaries should be returned (1) or not (0). Disclaimer: It takes time to run this model and hence not advised. (Required)
- `--plot`: A flag to indicate whether Rouge scores of the models should be plotted (1) or not (0). (Required)

## Data Description
The dataset used in this project is scraped from goal.com using web scraping tools such as Beautiful Soup and Requests. The data includes minute by minute live ticker for any match link from goal.com. The data is stored in a csv file.

## Directory Structure
```bash
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
```



