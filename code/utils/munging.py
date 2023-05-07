import pandas as pd
import numpy as np
import re
import spacy


class SoccerEventExtractor:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def _clean_text(self, text):
        text = text.lower().strip()
        return text

    def _generate_match_ids(self, df):
        df_unique = pd.DataFrame(df["match"].unique())
        df_unique.reset_index(inplace=True)
        df_unique.columns = ["match_id", "match"]
        df = pd.merge(df, df_unique, on="match")
        return df

    # Named Entity Recognition
    def _extract_entities(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append((ent.text, ent.start_char, ent.end_char, ent.label_))
        return entities

    def _extract_event(self, comment):
        # Define regex patterns
        player_pattern = r"\b[A-Z][a-z]+\b"
        card_pattern = r"(yellow|red)\s+card"
        team_pattern = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?"  # Matches team names with one or two words
        goal_pattern = r"goal"

        # Extract player name and card type
        player_matches = re.search(player_pattern, comment)
        card_match = re.search(card_pattern, comment)
        team_matches = re.findall(team_pattern, comment)
        goal_match = re.search(goal_pattern, comment)

        # Check if this is a goal event
        if goal_match:
            result = ["Goal"]
            # Check if the player's team is mentioned in the comment
            if " for " in comment:
                team_name = comment.split(" for ")[1].strip(".")
                result.append(team_name)
            else:
                result.append("")

        if len(player_matches) == 2 and len(team_matches) == 2:
            # If there are two player matches and two team matches, assume this is a substitution event
            player_out = player_matches[0]
            player_in = player_matches[1]
            team_out = team_matches[0]
            team_in = team_matches[1]
            result = [f"{player_out} off ({team_out})", f"{player_in} on ({team_in})"]
        else:
            result = []

        if player_matches and card_match:
            player_name = player_matches.group()
            card_type = card_match.group().title()  # Convert to title case
            result = [player_name, card_type]

            # Check if the player's team is mentioned in the comment
            if " for " in comment:
                team_name = comment.split(" for ")[1].strip(".")
                result.append(team_name)
            else:
                result.append("")

        return result

    def _input_event(self, df):
        df["event"] = df["comment"].apply(self._extract_event)
        df["event_player"] = df["event"].apply(lambda x: x[0] if len(x) > 0 else "")
        df["card_type"] = df["event"].apply(lambda x: x[1] if len(x) > 0 else "")
        df["event_team"] = df["event"].apply(lambda x: x[2] if len(x) > 0 else "")
        return df

    # Extraction Soccer Formations of Home and Away Team
    def _extract_formation(self, df):
        text = " ".join(df["comment"].values)
        pattern = r"\(\d-\d-\d-\d\)|\(\d-\d-\d\)"
        away_formation = re.findall(pattern, text)[0].replace("(", "").replace(")", "")
        home_formation = re.findall(pattern, text)[1].replace("(", "").replace(")", "")
        return home_formation, away_formation
