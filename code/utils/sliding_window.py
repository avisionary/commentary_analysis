import pandas as pd
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

class SlidingWindow():

    def __init__(self, folder):
        self.folder = folder
        self.df = pd.read_csv(Path(folder))
        self.df = self.df[self.df['match_id'] != 95]


    def window_df(self, df, start_timer, end_timer):
        # Convert time column to str
        df['time'] = df['time'].astype(str)
        comments = []
        for i in range(df.shape[0]):
            time = df['time'][i]
            if time != 'nan':
                if '+' in time:
                    time = time[:2]
                if int(time) >= start_timer and int(time) < end_timer:
                    if df['comment_desc'][i] == 'timer':
                        comments.append(df['comment'][i])
        return " ".join(comments)

    def create_window(self):
        all_comm = []
        match_ids = self.df['match_id'].unique()
        for id in match_ids:
            # Filter the dataframe w.r.t match_id
            match_df = self.df[self.df['match_id'] == id]
            match_df.reset_index(inplace = True, drop = True)

            # Divide the dataframe into 6 separate dfs, each corresponding to 15 minutes of the match.
            comm_15 = self.window_df(match_df, 0, 16)
            comm_30 = self.window_df(match_df, 16, 31)
            comm_45 = self.window_df(match_df, 31, 46)
            comm_60 = self.window_df(match_df, 46, 61)
            comm_75 = self.window_df(match_df, 61, 76)
            comm_90 = self.window_df(match_df, 76, 91)

            # Append the respective live tickers to a list
            all_comm.append([comm_15, comm_30, comm_45, comm_60, comm_75, comm_90])
        
        return all_comm

    def get_full_match_summ(self):
        all_ft_comm = []
        match_ids = self.df['match_id'].unique()
        for id in match_ids:
            # Filter the dataframe w.r.t match_id
            match_df = self.df[self.df['match_id'] == id]
            all_ft_comm.append(" ".join(match_df[match_df['comment_desc'] == 'full time summary']['comment']))
        
        return all_ft_comm
