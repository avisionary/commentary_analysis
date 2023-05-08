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

7. To use the User Interface run:
            `streamlit run bin/app.py`
    
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
├── commentary_analysis
│   ├── Formation_Analysis.ipynb
│   ├── README.md
│   ├── bin
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── main.py
│   ├── comm_env.yml
│   ├── commentary_analysis.egg-info
│   │   ├── PKG-INFO
│   │   ├── SOURCES.txt
│   │   ├── dependency_links.txt
│   │   └── top_level.txt
│   ├── jupyter_files
│   │   ├── cl_data_modelling_rs.ipynb
│   │   ├── eda.ipynb
│   │   ├── formation_analysis_aa.ipynb
│   │   ├── multiple_scraping.ipynb
│   │   ├── munging.ipynb
│   │   ├── munging_aa.ipynb
│   │   ├── scraping_check_aa.ipynb
│   │   ├── summary_abstractive_rs.ipynb
│   │   ├── summary_extractive_rs.ipynb
│   │   └── summary_rs_sliding_window.ipynb
│   ├── model_test.ipynb
│   ├── pytest.ini
│   ├── setup.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   └── test_code.cpython-39-pytest-7.2.1.pyc
│   │   ├── data
│   │   │   ├── test_match.csv
│   │   │   └── test_url.txt
│   │   └── test_code.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-39.pyc
│       │   ├── abstractive_sum.cpython-39.pyc
│       │   ├── clean_data.cpython-39.pyc
│       │   ├── collect_data.cpython-39.pyc
│       │   ├── extractive_sum.cpython-39.pyc
│       │   ├── munging.cpython-39.pyc
│       │   ├── nltk_sum.cpython-39.pyc
│       │   ├── plot_rouge.cpython-39.pyc
│       │   ├── rouge_score.cpython-39.pyc
│       │   ├── scraping.cpython-39.pyc
│       │   ├── sliding_window.cpython-39.pyc
│       │   ├── spacy_sum.cpython-39.pyc
│       │   └── stoc.cpython-39.pyc
│       ├── abstractive_sum.py
│       ├── clean_data.py
│       ├── collect_data.py
│       ├── eda.py
│       ├── extractive_sum.py
│       ├── munging.py
│       ├── nltk_sum.py
│       ├── plot_formations.py
│       ├── plot_rouge.py
│       ├── rouge_score.py
│       ├── scraping.py
│       ├── sliding_window.py
│       ├── spacy_sum.py
│       └── stoc.py
├── data
│   ├── cl_data_21_22 _stage_leg.csv
│   ├── cl_data_21_22.csv
│   ├── cl_match_links_21_22.csv
│   ├── commentary_new.csv
│   ├── commentory.csv
│   ├── commentory_matchid.csv
│   ├── formation_subs.csv
│   ├── key_events.csv
│   ├── key_events2.csv
│   ├── temp.rtf
│   └── temp_data.csv
├── figures
│   ├── images
│   │   ├── pitch.jpeg
│   │   └── temp.rtf
│   └── plots
│       ├── fig_lcs.html
│       ├── fig_uni.html
│       └── temp.rtf
└── requirements.txt
```



