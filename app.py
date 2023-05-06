# importing libraries
import streamlit as st
import pandas as pd
import joblib
import altair as alt
import numpy as np
import gzip
#import brotli
from unidecode import unidecode
from requests import get
from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import time
import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.translate import bleu
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

#import openai

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings

import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config


warnings.filterwarnings('ignore')
# import bz2
# import pickle
# import _pickle as cPickle

def _max_width_(prcnt_width:int = 75):
    max_width_str = f"max-width: {prcnt_width}%;"
    st.markdown(f""" 
                <style> 
                .reportview-container .main .block-container{{{max_width_str}}}
                </style>    
                """, 
                unsafe_allow_html=True,
    )

_max_width_()

# def load_zipped_pickle(filename):
#     with gzip.open(filename, 'rb') as f:
#         loaded_object = pickle.load(f)
#         return loaded_object


# # Load any compressed pickle file
# def decompress_pickle(file):
#     data = bz2.BZ2File(file, 'rb')
#     data = cPickle.load(data)
#     return data



def summarize_text_t5(text):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')


    preprocess_text = text.strip().replace("\n","")
    t5_prepared_Text = "summarize: "+preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    # summmarize 
    summary_ids = model.generate(tokenized_text,
                                        num_beams=4,
                                        no_repeat_ngram_size=2,
                                        min_length=30,
                                        max_length=100,
                                        early_stopping=True)

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


def get_all_comm_t5(comms):
    all_comm_t5 = []
    for commentary in comms:
        
        st.write(commentary)
        summary = summarize_text_t5(commentary)
        all_comm_t5.append(summary)
    return " ".join(all_comm_t5)

def scraping(url):
    #get data from site
    # print(f"Scraping for this match : {match}")
    response = get(url,headers= {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} )

    #print status code

    print(response.status_code)

    if response.status_code == 200:
        pageSoup = BeautifulSoup(response.content, 'html.parser')
        time = []
        comment = []
        event = []
        event_player = []
        event_team = []
        comment_desc = []

        half_time_flag = False
        timer_flag = False
        comment_desc_dict = {True: "half time summary",
                        False : "full time summary"}

        counter = 0

        for x in pageSoup.findAll('div',class_ = "comment"):
            counter += 1

            if x.find_all("div", {"class": "comment-event"}):
                for q in x.findAll('div',class_ = "wrapper"):
                    for r in q.findAll('div',class_ = "event-icon"):
                        e = r.find("div")["class"][1]
                        e = e.replace("type-","")
                        e = unidecode(e)
                        

                    for r in q.findAll('div',class_ = "event-text has-additional"):
                        if r.find("div",{"class" : "event-text-main" }):
                            p1 = unidecode(r.find("div",{"class" : "event-text-main" }).text)
                        else:
                            p1 = ""
                        if r.find("div",{"class" : "event-text-additional" }):
                            p2 = unidecode(r.find("div",{"class" : "event-text-additional" }).text)
                            #e = x.find("div", {"class": "comment-event"}).find("event-text-additional").text
                        else:
                            p2 = ""
                        

                    for r in q.findAll('div',class_ = "event-crest"):
                        for d in r.findAll('a'):
                            #print(d)
                            te = unidecode(d.find("img")['alt'])
                            

                event_player.append([p1,p2])
                event.append(e)
                event_team.append(te)


            else:
                event.append("")
                event_player.append("")
                event_team.append("")
            for y in x.findAll('div',class_ = "comment-desc"):
                if y.find_all("span", {"class": "time"}):
                    timer_flag = True


                    t = y.find('span',class_ = "time").text
                    t = t.replace("'","")
                    #print(t)
                    time.append(t)
                    comment_desc.append("timer")
                else:
                    time.append("")
                    if time[-1] == "" and timer_flag:
                            half_time_flag = True
                    comment_desc.append(comment_desc_dict[half_time_flag])
                    #print("Summary")
                
                if y.find_all("span", {"class": "text"}):
                    c = y.find('span',class_ = "text").text
                    c = unidecode(c)
                    comment.append(c)
        

        print(f"Total scraped comments for this match: {counter} ")
        match_commentary_df = pd.DataFrame(list(zip(time, comment,event,event_player,event_team,comment_desc)),
                columns =['time', 'comment','event','event_player','event_team','comment_desc'])
        
        team_count = 0
        for teams in pageSoup.findAll('div',class_ = "widget-match-header__name"):
            if team_count == 0:
                match_commentary_df['home_team'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--full" }).text)
                match_commentary_df['home_team_abbr'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--short" }).text)
                team_count += 1
            elif team_count == 1:
                match_commentary_df['away_team'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--full" }).text)
                match_commentary_df['away_team_abbr'] = unidecode(teams.find("span",{"class" : "widget-match-header__name--short" }).text)

        for score in pageSoup.findAll('div',class_ = "widget-match-header__score"):
            match_commentary_df['full_time_score'] = unidecode(score.find("span").text)
        

        return (match_commentary_df,1)
    else:
        #log.append(match)
        return (0,0)
    


def plot_form(str_form1,str_form2):
    x_axis_start1 = 0
    x_axis_end1 = 100

    x_axis_start2 = 100
    x_axis_end2 = 200

    y_axis_start = 0
    y_axis_end = 100


    y = []
    list_form1 = str_form1.split("-")
    list_form2 = str_form2.split("-")

    list_form1.insert(0,"1")
    list_form2.insert(0,"1")

    list_form2 = list_form2[::-1]
    print(list_form2)

    final_list = list_form1 + list_form2
    print(final_list)


    x_axis_split = len(list_form1) + 1
    start_pos_x = (x_axis_end1 - x_axis_start1)/x_axis_split
    #print(start_pos_x)
    x_axis = x_axis_start1
    y_axis = y_axis_start
    for position in list_form1:
        position = int(position)
        x_axis = x_axis + start_pos_x
        print(f"Num {position}")
        print(f"X_axis : {x_axis}")
        y_axis_split = position + 1
        start_pos_y = (y_axis_end - y_axis_start)/y_axis_split
        
        for player in range(position):
            
            y_axis = y_axis + start_pos_y
            print(f"Y_Axis : {y_axis}")
            y.append((x_axis,y_axis))
        y_axis = y_axis_start

    x_axis_split = len(list_form2) + 1
    start_pos_x = (x_axis_end2 - x_axis_start2)/x_axis_split
    #print(start_pos_x)
    x_axis = x_axis_start2
    y_axis = y_axis_start
    for position in list_form2:
        position = int(position)
        x_axis = x_axis + start_pos_x
        print(f"Num {position}")
        print(f"X_axis : {x_axis}")
        y_axis_split = position + 1
        start_pos_y = (y_axis_end - y_axis_start)/y_axis_split
        
        for player in range(position):
            
            y_axis = y_axis + start_pos_y
            print(f"Y_Axis : {y_axis}")
            y.append((x_axis,y_axis))
        y_axis = y_axis_start


    formation = np.array(y)
    fig, ax = plt.subplots(figsize=(10, 5))

    

    img = plt.imread("figures/images/pitch.jpeg")

    plt.xlim(0, 200)
    plt.ylim(0, 100)

    mask = formation[:, 0] > 100  # Boolean mask for x-axis points greater than 100

    ax.scatter(formation[~mask, 0], formation[~mask, 1], s=430, edgecolors='#e5f5e0', linewidths=1,c = "#00b9ff") # plot points with x-axis value <= 100

    ax.scatter(formation[mask, 0], formation[mask, 1], s=430, edgecolors='#e5f5e0', linewidths=1, c='#ff4600') # plot points with x-axis value > 100 in red color

    ax.imshow(img, extent=[0, 200, 0, 100])
    plt.axis("off")
    #plt.show()

    # display the plot using st.pyplot()
    st.pyplot(fig)
    return formation
        

# pl = plot_form(str_form1,str_form2)




def window_df(df, start_timer, end_timer):
    comments = []
    for i in range(len(df)):
        time = df['time'][i]
        if time != '':
            if '+' in time:
                time = time[:2]
            if int(time) >= start_timer and int(time) < end_timer:
                if df['comment_desc'][i] == 'timer':
                    comments.append(df['comment'][i])
    return " ".join(comments)

def tokenization(text):
    """ A method to tokenize text data """
    text = re.split('\W+', text) #splitting each sentence/ tweet into its individual words
    return text

def summarize_text_nltk(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize the sentences into words and remove stopwords
    
    text_punct_removed = remove_punct(text)
    words = tokenization(text_punct_removed.lower())
    
    # words = word_tokenize(text)

    # remove stopwords
    stop_words =  set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    # Apply stemming to the filtered words
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]

    # Lemmatize words
    word_net_lemma = nltk.WordNetLemmatizer()
    word_lemma = [word_net_lemma.lemmatize(word) for word in stemmed_words]
    
    # Calculate word frequency and sentence scores
    word_freq = nltk.FreqDist(stemmed_words)
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_freq:
                if len(sentence.split()) < 30:
                    if i not in sentence_scores:
                        sentence_scores[i] = word_freq[word]
                    else:
                        sentence_scores[i] += word_freq[word]
    
    # Select the top sentences based on their scores
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = [sentences[i] for i in sorted(summary_sentences)]
    return " ".join(summary)


def remove_punct(text):
    """ A method to remove punctuations from text """
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text) #removes numbers from text
    return text


def custom_key(value):
    # Remove any spaces
    value = value.replace(' ', '')
    # Replace any '+' with a '.'
    value = value.replace('+', '.')
    # Try to convert to float
    try:
        return float(value)
    # If it cannot be converted to float, return a large value
    except ValueError:
        return 1000
    


# title 
st.header("Commentary Analysis")
st.markdown('Highlighting key events and summarising a soccer match')

url = st.text_input('Enter Goal.com url')


commentory_df = pd.DataFrame(columns=['time', 'comment', 'event', 'event_player', 'event_team',
       'comment_desc', 'home_team', 'home_team_abbr', 'away_team',
       'away_team_abbr', 'full_time_score', 'match', 'link'])
counter = 0

# # reading in dataset
# df = pd.read_csv("data/key_events2.csv")

# list_matches = list(df['match_x'])

# options = list(range(1,len(list_matches)+1))
# #match_selection = st.selectbox("Select match!", options, format_func=lambda x: list_matches[x-1])
# match_selection = st.selectbox("Select match!", list_matches)

# st.text(fig_data.head())
col1, col2 = st.columns(2)


# If button is pressed
#if st.button("Submit"):
try:
    temp = scraping(url)
    if temp[1] == 1:
        counter += 1
        temp_df = temp[0]

        commentory_df = pd.concat([commentory_df,temp_df])
    commentory_df['match'] = commentory_df['home_team'].astype(str) + " vs " + commentory_df['away_team'].astype(str)
    commentory_df['link'] = url

    eda_df = commentory_df
    # Drop the rows with NaN values in the 'column_name' column
    eda_df = eda_df.dropna(subset=['event'])
    eda_df = eda_df[eda_df['event'] != ""]
    #capitalize the first letter of each word in a string and replace underscores with spaces. 
    eda_df['event'] = eda_df['event'].str.replace('_', ' ').str.title()

    # Replace "." with "+" in the 'time' column of the dataframe
    eda_df['time'] = eda_df['time'].str.replace('.', '+')

    # Sort the values using the custom function as the key
    time_values = sorted(eda_df['time'].unique(), key=custom_key, reverse=True)

    # create an empty list to store the first string values
    player_involved_list = []
    #st.write(eda_df)
    # iterate over the rows of the DataFrame and extract the first string value from the "event_player" column
    for index, row in eda_df.iterrows():

        # get the first element of the list in the DataFrame column
        #st.write(row["event_player"])
        event_player_list = row["event_player"]#[2:-2].split(',')
        #st.write(event_player_list)
        #st.write(len(event_player_list))
        

        if row["event"]=="Substitution":

            # extract the first and second string values from the list and remove leading/trailing spaces and single quotes
            first_string = event_player_list[0].strip().strip("'")
            second_string = event_player_list[1].strip().strip("'")

            # concatenate the two strings with "with"
            concatenated_string = "{} with {}".format(first_string, second_string)
            player_involved_list.append(concatenated_string)
        else:
            first_string = event_player_list[0].strip().strip("'")
            player_involved_list.append(first_string)

    # add the list of first string values as a new column to the DataFrame
    eda_df["player_involved"] = player_involved_list





    #print(commentory_df.head())
    filtered_df = commentory_df[commentory_df['event'].notnull()]
    filtered_df = commentory_df[commentory_df['event'] != ""]
    #st.write(filtered_df.head())
    filtered_df['time_detail'] = filtered_df['time'].apply(lambda x: 'Added Time' if "+" in x else 'Normal Time')
    filtered_df['time'] = filtered_df['time'].apply(lambda x: x.replace(" ",""))

    #st.write(filtered_df.head())
    filtered_df['time'] = filtered_df['time'].apply(lambda x: (int(re.search("(\d+)\+(\d+)",x).group(1)) + int(re.search("(\d+)\+(\d+)",x).group(2))) if "+" in x else int(x) )
    filtered_df = filtered_df.sort_values(by="time",ascending=True)


    # Convert time column to str
    commentory_df['time'] = commentory_df['time'].astype(str)

    text = " ".join(commentory_df["comment"].values)
    pattern = r'\(\d-\d-\d-\d\)|\(\d-\d-\d\)'
    away_formation = re.findall(pattern, text)[0].replace("(", "").replace(")", "")
    home_formation = re.findall(pattern, text)[1].replace("(", "").replace(")", "")


    # Divide the dataframe into 6 separate dfs, each corresponding to 15 minutes of the match.
    comm_15 = window_df(commentory_df, 0, 16)
    comm_30 = window_df(commentory_df, 16, 31)
    comm_45 = window_df(commentory_df, 31, 46)
    comm_60 = window_df(commentory_df, 46, 61)
    comm_75 = window_df(commentory_df, 61, 76)
    comm_90 = window_df(commentory_df, 76, 91)

    # Append the respective live tickers to a list
    window_comments = [comm_15, comm_30, comm_45, comm_60, comm_75, comm_90]

    # Will be used later for summaries
    timer_list= ['[1-15]', '[16-30]', '[31-45]', '[46-60]', '[61-75]', '[76-90]']

    nltk_window_summaries = []
    for comment  in window_comments:
        nltk_window_summaries.append(summarize_text_nltk(comment))

    nltk_time_window = []
    nltk_final = []


    for i in range(len(nltk_window_summaries)):
        nltk_time_window.append(timer_list[i] + ' ' +  nltk_window_summaries[i])
        nltk_final.append(' ' +  nltk_window_summaries[i])

    nltk_window_summ = " ".join(nltk_time_window)

    st.header("Match Formations:")

    st.write(commentory_df['home_team'][0], " (",home_formation, ") vs", commentory_df['away_team'][0], " (", away_formation, ")")

    plot_form(home_formation,away_formation)
    #st.write(nltk_window_summaries)
    #st.header("Full Match Summary:")
    # st.write(time.time())
    # t5_comm = get_all_comm_t5(nltk_window_summaries)
    # st.write(t5_comm)
    # st.write(time.time())


    #t5_comm


    st.header("Match Summary:")

    for wind in nltk_time_window:
        st.write(wind)







    st.header("Key identified events:")
    st.write("The follwowing events make up the defination of key events :")
    lst = ['Goal','Substitution','Yellow Card','Assist','Penalty-goal','Own-goal','Red Card','Missed Penalty']

    s = ''

    for i in lst:
        s += "- " + i + "\n"
    #st.write(commentory_df.head())
    st.markdown(s)
    # selected_df = df[df['match_x'] == match_selection]

    tab1, tab2 = st.tabs([commentory_df['home_team'][0], commentory_df['away_team'][0]])

    # Define a dictionary of colors for each event
    event_colors = {
        'Assist': '#7fbf7b',
        'Goal': '#3690c0',
        'Red Card': '#fb6a4a',
        'Substitution': '#8c6bb1',
        'Yellow Card': '#ffffbf',
        'Own Goal':'#e0f3f8',
        'Penalty Goal':'#91bfdb',
        'Penalty Miss':'#c51b7d',
        'Penalty Save':'#e9a3c9',
    }

    with tab1:
        team_events = eda_df.loc[eda_df['event_team'] == commentory_df['home_team'][0]]

        team_events = team_events.groupby(['time', 'event']).agg({'player_involved': ', '.join}).reset_index()


        # Create a chart with time on the y-axis
        line1=(alt.Chart(team_events)
                .mark_bar()
                .encode(
                    x=alt.X('event', axis=alt.Axis(title='Event')),
                    y=alt.Y('time', scale=alt.Scale(domain=time_values), axis=alt.Axis(title='Match time (in minutes)')),
                    color=alt.Color('event',legend = None,scale=alt.Scale(domain=list(event_colors.keys()), range=list(event_colors.values()))),
                    tooltip=[alt.Tooltip('event', title='Event'), alt.Tooltip('player_involved', title='Event Player(s)'), alt.Tooltip('time', title='Match Time')]
                )
        ).properties(
            width=400,
            height=300,
            title='Temporal Analysis of Match Events'
        ).configure_axis(labelAngle=0,
                    domainColor='white').configure_view(
            stroke = None
                    )

        st.altair_chart(line1, theme = None,use_container_width=True)


    with tab2:
        team_events2 = eda_df.loc[eda_df['event_team'] == commentory_df['away_team'][0]]

        team_events2 = team_events2.groupby(['time', 'event']).agg({'player_involved': ', '.join}).reset_index()

        

        # Create a chart with time on the y-axis
        line1=(alt.Chart(team_events2)
                .mark_bar()
                .encode(
                    x=alt.X('event', axis=alt.Axis(title='Event')),
                    y=alt.Y('time', scale=alt.Scale(domain=time_values), axis=alt.Axis(title='Match time (in minutes)')),
                    color=alt.Color('event',legend = None,scale=alt.Scale(domain=list(event_colors.keys()), range=list(event_colors.values()))),
                    tooltip=[alt.Tooltip('event', title='Event'), alt.Tooltip('player_involved', title='Event Player(s)'), alt.Tooltip('time', title='Match Time')]
                )
        ).properties(
            width=400,
            height=300,
            title='Temporal Analysis of Match Events'
        ).configure_axis(labelAngle=0,
                    domainColor='white').configure_view(
            stroke = None
                    )

        st.altair_chart(line1, theme = None,use_container_width=True)



    minute_range = st.slider('Based on the match summary, what time frame key events are you interested in?',0,100,(0,100))

    #st.write(minute_range[0])

    filtered_df = filtered_df[((filtered_df['time']>=minute_range[0]) & (filtered_df['time']<=minute_range[1]))]
    for idx, row in filtered_df.iterrows():
        st.write(row['time'],row['comment'])

except:
    st.write("Enter a correct URL from goal.com to begin!")