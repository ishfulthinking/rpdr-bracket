import os
import re
import csv
import rutils
from typing import List



### 🛠️ Helper methods ###
def get_previous_episode_remaining_questions(previous_episode_directory: str) -> List[str]:
    previous_episode_remaining_questions = list()
    with open(previous_episode_directory, 'r') as previous_episode_file:
        previous_episode_remaining_questions.extend(csv.reader(previous_episode_file)[0])
    return previous_episode_remaining_questions

def create_answer_key_default_questions_array(previous_episode_directory: str) -> List[List[str]]:
    question_row = [rutils.LIPSYNC_QUESTION]
    if previous_episode_directory and len(previous_episode_directory == 1):
        question_row.extend(get_previous_episode_remaining_questions(previous_episode_directory))
    answer_row = ["" * len(question_row)]
    default_questions_array = list()
    default_questions_array.append(question_row)
    default_questions_array.append(answer_row)
    return default_questions_array



### 👷‍♀️ Script ###
print("📁 Generating new week directory.")
episode_range = rutils.get_episode_range()
episode_directory = rutils.get_episode_directory(episode_range)

os.mkdir(episode_directory)

print("    🔎 Looking for last week's directory...")
previous_episode_directory = rutils.find_previous_episode_directory(episode_range, episode_directory)

print("    📊 Generating new answers.csv for week...")
# TODO: get deadline day and put it in answers.csv
default_questions_array = create_answer_key_default_questions_array(previous_episode_directory)
rutils.write_2d_array_to_csv(episode_directory, rutils.ANSWERS_FILENAME_CSV, default_questions_array)

print("🎉 Success!")