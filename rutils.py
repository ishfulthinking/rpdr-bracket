import os
import csv
from typing import List

### Variables ###
EPISODE_FILENAME = "episode"
ANSWERS_FILENAME_CSV = "answers.csv"
RESPONSES_FILENAME_CSV = "responses.csv"
SCORES_FILENAME_CSV = "scores.csv"
LIPSYNC_QUESTION = "Guess a Lip-sync Song performed this season (Guess #1) (5 Points)"



### Classes ###
class Answer:
    def __init__(self, answers, point_value):
        self.answers = answers
        self.point_value = point_value

# Competitor contains username (unique key) and row to be used for scores.py
class Competitor:
    def __init__(self, username, response_row):
        self.username = username
        self.response_row = response_row
        # TODO ip: Add feature for checking if submission was on time
            # self.submittedOnTime = False
        self.score = int(0)

    def __str__(self):
        return "Competitor [username: " + self.username + ", response_row: " + str(self.response_row) + "]"

    def increment_score(self, points):
        self.score += int(points)



### Methods ###
def abort_with_reason(reason: str):
    print("⛔️ ERROR: " + reason + "\n")
    os.abort()
def warn_with_reason(reason: str):
    print("📣 WARN: " + reason + "\n")

def get_episode_range() -> List[int]:
    episode_range = [int(number_str) for number_str in input("    ➡️ Which episode(s) is this for? [For multi-week episodes, enter a range, e.g. 1-2]: ").split("-")]
    if len(episode_range) == 1:
        if episode_range[0] < 0:
            print("What? You can't have a negative episode number.")
            abort_with_reason("Invalid episode number.")
    elif len(episode_range) != 2 or episode_range[0] < 0 or episode_range[0] >= episode_range[1]:
        print("What? You can't have an episode range like that.")
        abort_with_reason("Invalid episode range.")
    return episode_range

def get_episode_directory(episode_range: List[int]) -> str:
    episode_directory = EPISODE_FILENAME + str(episode_range[0])
    if (len(episode_range) == 2):
        episode_directory = episode_directory + "_" + EPISODE_FILENAME + str(episode_range[1])
    return episode_directory

def find_previous_episode_directory(episode_range: List[int], episode_directory: str) -> str:
    episode_lower_range = episode_range[0]
    expected_directory = list(filter(lambda previous_episode_number: previous_episode_number == (episode_lower_range - 1), next(os.walk('.'))[1]))
    if len(expected_directory) == 1:
        previous_episode_directory = expected_directory[0]
        print("    🔎 Found previous episode directory.", previous_episode_directory)
        return previous_episode_directory
    print("    🔍 No previous episode directory.")
    return None

def write_2d_array_to_csv(directory: str, filename: str, source_array: List[List[str]]):
    with open(directory + "/" + filename, "w", encoding="UTF8", newline="") as target_csv:
        writer = csv.writer(target_csv)
        writer.writerows(source_array)