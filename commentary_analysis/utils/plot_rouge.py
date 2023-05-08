import pandas as pd
import altair as alt
import os

class PlotRouge():
    def __init__(self) -> None:
        self.df = pd.DataFrame(columns=['spacy_uni_precision', 'nltk_uni_precision', 'spacy_lcs_precision', 'nltk_lcs_precision'])
        self.dirname = os.path.dirname(__file__)
        self.path = os.path.join(self.dirname,"../../figures/plots" )
    
    def extract_melt_rouge(self, spacy_rouge, nltk_rouge):
        """
        Plot the rouge scores for each commentary.

        Parameters:
        - rouge_scores (list): List of rouge scores for each commentary.
        - rouge_type (str): Rouge type (rouge-1, rouge-2, rouge-l).
        """
        spacy_uni_prec = spacy_rouge['uni_precision']
        nltk_uni_prec = nltk_rouge['uni_precision']
        spacy_lcs_prec = spacy_rouge['lcs_precision']
        nltk_lcs_prec = nltk_rouge['lcs_precision']
        
        rouge_extrac_df = pd.DataFrame(list(zip(spacy_uni_prec, nltk_uni_prec, spacy_lcs_prec, nltk_lcs_prec)),columns=['spacy_uni_precision', 'nltk_uni_precision', 'spacy_lcs_precision', 'nltk_lcs_precision'])
        rouge_extrac_df.reset_index(inplace=True)
        rouge_extrac_df.columns = ['match_id', 'spacy_uni_precision', 'nltk_uni_precision', 'spacy_lcs_precision', 'nltk_lcs_precision']
        return pd.melt(rouge_extrac_df,id_vars=['match_id'],value_name="score_type",)
    
    def plot_uni_rouge_score(self, df):
        click = alt.selection_multi(encodings=['color'])
        timeunit='date'
        
        rouge_extrac_df2 = df[((df["variable"] == "spacy_uni_precision")) | 
                                            ((df["variable"] == "nltk_uni_precision"))]
        fig4 = (
                alt.Chart(rouge_extrac_df2)
                .mark_point(width=1)
                .encode(
                    x = alt.X("match_id", title="Match ID"),
                    y=alt.Y("score_type", title="Precision",scale=alt.Scale(domain=[0, 0.6])),
                    color = alt.Color("variable", scale = alt.Scale(scheme = 'dark2'),title = "Unigram models"),
                    tooltip=[alt.Tooltip('variable')]
                )
            ).properties(width=alt.Step(30),title={
            "text": ["Extractive Summarization Performance"], 
            "subtitle": ["Plot of precision values of Unigram"]
            },).interactive()

        fig4 = alt.layer(
            fig4
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        )
        
        fig4.save(f"{self.path}/fig_uni.html")
        fig4.show()
    
    def plot_lcs_rouge_score(self, df):
        click = alt.selection_multi(encodings=['color'])
        timeunit='date'
        
        rouge_extrac_df3 = df[((df["variable"] == "spacy_lcs_precision")) | ((df["variable"] == "nltk_lcs_precision"))]
        fig4 = (
                alt.Chart(rouge_extrac_df3)
                .mark_point(width=1)
                .encode(
                    x = alt.X("match_id", title="Match ID"),
                    y=alt.Y("score_type", title="Precision",scale=alt.Scale(domain=[0, 0.6])),
                    color = alt.Color("variable", scale = alt.Scale(scheme = 'dark2'),title = "Unigram models"),
                    tooltip=[alt.Tooltip('variable')]
                )
            ).properties(width=alt.Step(30),title={
            "text": ["Extractive Summarization Performance"], 
            "subtitle": ["Plot of precision values of Unigram"]
            },).interactive()

        fig4 = alt.layer(
            fig4
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        )
        
        fig4.save(f"{self.path}/fig_lcs.html")
        fig4.show()