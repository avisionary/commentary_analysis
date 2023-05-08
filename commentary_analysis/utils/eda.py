import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from wordcloud import WordCloud, STOPWORDS

class MatchAnalysis:
    def __init__(self, commentary_file):
        # read data from a CSV file and add it into a Pandas DataFrame
        self.commentary_df = pd.read_csv(commentary_file)
    
    #method to create word cloud
    def generate_word_cloud(self):
        # concatenate all comments into a single string
        text = " ".join(str(comment) for comment in self.commentary_df['comment'])

        # generate word cloud
        word_cloud = WordCloud(
            width=3000,
            height=2000,
            random_state=1,
            background_color="black",
            colormap="Pastel1",
            collocations=False,
            stopwords=STOPWORDS,
        ).generate(text)

        # display the word cloud
        plt.imshow(word_cloud)
        plt.axis("off")
        plt.show()
 
    

    #method to filter dataframe
    def filter_commentary(self, match_id):
        # filter the commentary dataframe based on the match_id
        filtered_commentary_df = self.commentary_df[self.commentary_df['match_id'] == match_id]
        # drop rows where the 'event' column is empty
        filtered_commentary_df = filtered_commentary_df.dropna(subset=['event'])
        # replace underscores with spaces and capitalize the first letter of each word in the 'event' column
        filtered_commentary_df['event'] = filtered_commentary_df['event'].str.replace('_', ' ').str.title()
        # replace periods with plus signs in the 'time' column
        filtered_commentary_df['time'] = filtered_commentary_df['time'].str.replace('.', '+')
        # store the filtered commentary dataframe in the instance variable
        self.filtered_commentary_df = filtered_commentary_df

    #method to plot bar chart for event count
    def plot_event_counts(self, output_file):
        # create a bar chart using Altair library
        bar2 = (
            alt.Chart(self.filtered_commentary_df)
            .mark_bar()
            .encode(
                # set the X-axis to display the event type
                x=alt.X('event', axis=alt.Axis(title='Event')),
                # set the Y-axis to display the count of events
                y=alt.Y('count()', axis=alt.Axis(title='Event Count')),
                # set the color of the bars to represent the team
                color=alt.Color('event_team:N', legend=alt.Legend(title='Team', labelFontSize=9, titleFontSize=10, labelLimit=100), scale=alt.Scale(range=['#55a868', '#4c72b0'])),
            )
            # rotate the X-axis labels to 45 degrees for better readability
            .configure_axisX(labelAngle=45)
            # remove the grid lines from the chart
            .configure_axis(grid=False, gridColor=None)
        )
        # save the chart to an HTML file
        bar2.save(output_file)
        # display the bar chart
        bar2.show()
        

    #method to convert event time in a desired format
    def get_time_values(self):
        # Define a custom key function to sort the time values in descending order
        def custom_key(value):
            # Remove spaces and replace plus signs with periods
            value = value.replace(' ', '')
            value = value.replace('+', '.')
            try:
                # Convert the value to a float
                return float(value)
            except ValueError:
                # If the value cannot be converted to a float, return a large number
                return 1000
        # Get all unique time values from the filtered commentary data frame and sort them using the custom key function
        time_values = sorted(self.filtered_commentary_df['time'].unique(), key=custom_key, reverse=True)
        # Set the time_values attribute to the sorted list of time values
        self.time_values = time_values
    
    #method to get the players involved in the event
    def extract_player_involved(self):
        # create an empty list to store player names
        player_involved_list = []
        # iterate over each row of the filtered commentary dataframe
        for index, row in self.filtered_commentary_df.iterrows():
            # extract the list of players involved in the event
            event_player_list = row["event_player"][2:-2].split(',')
            # check if the event is a substitution
            if row["event"]=="Substitution":
                # extract the names of the two players involved in the substitution
                first_string = event_player_list[0].strip().strip("'")
                second_string = event_player_list[1].strip().strip("'")
                # concatenate the two player names with a "with" in between
                concatenated_string = "{} with {}".format(first_string, second_string)
                player_involved_list.append(concatenated_string)
            else:
                 # if the event is not a substitution, extract the name of the first player in the list
                first_string = event_player_list[0].strip().strip("'")
                player_involved_list.append(first_string)
         # add the player_involved column to the filtered commentary dataframe
        self.filtered_commentary_df["player_involved"] = player_involved_list

    def get_team_events(self, team_name):
        # Filter the commentary to only include events by the specified team
        team_events = self.filtered_commentary_df.loc[self.filtered_commentary_df['event_team'] == team_name]
        # Group events by time and type, and concatenate the names of all players involved in each event
        team_events = team_events.groupby(['time', 'event']).agg({'player_involved': ', '.join}).reset_index()
        # Store the resulting dataframe as an attribute of the object
        self.team_events = team_events

    #method to plot chart for different events on minute-by-minute basis 
    def plot_temporal_analysis(self):
        #dictionary of event colors for use in the chart
        event_colors = {
            'Assist': '#7fbf7b',
            'Goal': '#3690c0',
            'Red Card': '#fb6a4a',
            'Substitution': '#8c6bb1',
            'Own Goal':'#e0f3f8',
            'Yellow Card': '#fcf4a3',
            'Penalty Goal':'#91bfdb',
            'Penalty Miss':'#c51b7d',
            'Penalty Save':'#e9a3c9',
        }

        line_chart = (
            alt.Chart(self.team_events)
            # bar chart to show events over time
            .mark_bar()
            .encode(
                x=alt.X('event', axis=alt.Axis(title='Event')),
                y=alt.Y('time', scale=alt.Scale(domain=self.time_values), axis=alt.Axis(title='Match time (in minutes)')),
                # Color-code the events
                color=alt.Color('event', legend=None, scale=alt.Scale(domain=list(event_colors.keys()), range=list(event_colors.values()))),
                # Show event, player involved, and match time in tooltip
                tooltip=[alt.Tooltip('event', title='Event'), alt.Tooltip('player_involved', title='Event Player(s)'), alt.Tooltip('time', title='Match Time')]
            )
            .properties(width=400, height=300, title='Temporal Analysis of Match Events')
            # Set axis label orientation to horizontal
            .configure_axis(labelAngle=0)
        )
        return line_chart

if __name__ == "__main__":
    # Path to the data file
    commentary_file = "../data/commentory_matchid.csv"
    # Create MatchAnalysis object and filter the commentary for a specific match
    analysis = MatchAnalysis(commentary_file)
    analysis.filter_commentary(match_id=2)
    # Extract the time values and players involved in each event
    analysis.get_time_values()
    analysis.extract_player_involved()
    # Get the events for a specific team
    analysis.get_team_events(team_name='Young Boys')
    chart = analysis.plot_temporal_analysis()
    analysis.plot_event_counts(output_file='event_counts.html')
    analysis.generate_word_cloud()
    # Display the temporal analysis chart
    chart.show()
    
    