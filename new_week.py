import os
import re
import csv
import rpdr_utils
from typing import List



### 🛠️ Helper methods ###
def get_episode_range() -> List[int]:
    episode_range = [int(number_str) for number_str in input("➡️ Which episode(s) is this for? [For multi-week episodes, enter a range, e.g. 1-2]: ").split("-")]
    if len(episode_range) == 1:
        if episode_range[0] < 0:
            print("What? You can't have a negative episode number.")
            raise Exception("Invalid episode number.")
    elif len(episode_range) != 2 or episode_range[0] < 0 or episode_range[0] >= episode_range[1]:
        print("What? You can't have an episode range like that.")
        raise Exception("Invalid episode range.")
    return episode_range

def create_episode_directory(episode_range: List[int]) -> str:
    episode_directory = rpdr_utils.EPISODE_FILENAME + str(episode_range[0])
    if (len(episode_range) == 2):
        episode_directory = episode_directory + "_" + episode_range[1]
    
    return episode_directory

def find_previous_episode_directory(episode_range: List[int], episode_directory: str) -> str:
    episode_lower_range = episode_range[0]
    expected_directory = list(filter(lambda previous_episode_number: previous_episode_number == (episode_lower_range - 1), next(os.walk('.'))[1]))
    if len(expected_directory) == 1:
        previous_episode_directory = expected_directory[0]
        print("    🔎 Found previous episode directory to pull data from!", previous_episode_directory)
        return previous_episode_directory
    print("    🤷 No previous episode directory to pull remaining questions from.")
    return None

def get_previous_episode_remaining_questions(previous_episode_directory: str) -> List[str]:
    previous_episode_remaining_questions = list()
    with open(previous_episode_directory, 'r') as previous_episode_file:
        previous_episode_remaining_questions.extend(csv.reader(previous_episode_file)[0])
    return previous_episode_remaining_questions

def create_answer_key_default_questions_array(previous_episode_directory: str) -> List[List[str]]:
    question_row = [rpdr_utils.LIPSYNC_QUESTION]
    if previous_episode_directory and len(previous_episode_directory == 1):
        question_row.extend(get_previous_episode_remaining_questions(previous_episode_directory))
    answer_row = ["" * len(question_row)]
    default_questions_array = list()
    default_questions_array.append(question_row)
    default_questions_array.append(answer_row)
    return default_questions_array

def write_2d_array_to_csv(directory: str, filename: str, source_array: List[List[str]]):
    with open(directory + "/" + filename, "w", encoding="UTF8", newline="") as target_csv:
        writer = csv.writer(target_csv)
        writer.writerows(source_array)

# def create_scores_array(previous_episode_directory: str) -> List[List[str]]:
#     previous
#     header_row = ["Competitor", ]



### 👷‍♀️ Script ###
print("📁 Generating new week directory.")
episode_range = get_episode_range()
episode_directory = create_episode_directory(episode_range)
os.mkdir(episode_directory)

print("🔎 Looking for last week's directory.")
previous_episode_directory = find_previous_episode_directory(episode_range, episode_directory)

print("📊 Generating new answers.csv for week.")
default_questions_array = create_answer_key_default_questions_array(previous_episode_directory)
write_2d_array_to_csv(episode_directory, "answers.csv", default_questions_array)

print("📊 Generating new scores.csv for week.")
# TODO kp: Generate scores.csv file that copies last week's file and appends a new, empty column.

print("Success 🎉")