import os
import re
import csv
import rutils
from typing import List, Dict, Tuple

# Helper
def get_tidy_question(raw_question: str) -> str:
    tidy_question = re.findall(r'^[^\(]*', raw_question)
    tidy_question = tidy_question[0].strip()
    return tidy_question

def get_point_value(raw_question: str) -> int:
    # TODO: Clean this regex to include "points" OR "point"
    parentheses_substrings = re.findall('\(.*\)*', raw_question)
    # Usually, the point value is in the ultimate parentheses substring, e.g. "Tops of the Week (Pick #1) (2 points)"
    ultimate_parentheses_substring = parentheses_substrings[len(parentheses_substrings) - 1]
    parentheses_integers = re.findall(r'\d+', ultimate_parentheses_substring)
    point_value = parentheses_integers[len(parentheses_integers) - 1]
    # If a point value wasn't retrieved, the question probably doesn't have a value, e.g. "Wanna do prizes?". So just return -1.
    if not point_value:
        rutils.warn_with_reason("No point value for " + raw_question)
        return -1
    return point_value

def create_answer_dict(episode_directory: str) -> Dict[str, rutils.Answer]:
    answer_filepath = episode_directory + "/" + rutils.ANSWERS_FILENAME_CSV
    answer_csv = open(answer_filepath, newline='')
    answer_2d_array = list(csv.reader(answer_csv))
    answer_dict = dict()
    for col in range(0, len(answer_2d_array[0])):
        raw_question = answer_2d_array[0][col]
        tidy_question = get_tidy_question(raw_question)
        point_value = get_point_value(raw_question)
        answer = answer_2d_array[1][col]
        # If the question is already in the dict, it must have multiple answers - so skip ahead and add the answer.
        if tidy_question in answer_dict:
            answer_dict[tidy_question].answers.add(answer)
            continue
        # Otherwise, create a new dictionary entry for the question, its answer set, and point value.
        # If there are no points available, don't add it to the dict. It might be a just-for-fun question.
        if point_value == -1:
            continue
        answer_set = set()
        answer_set.add(answer)
        answer_dict[tidy_question] = rutils.Answer(answer_set, point_value)
    return answer_dict

def get_responses_2d_array(episode_directory: str) -> List[List[str]]:
    responses_filepath = episode_directory + "/" + rutils.RESPONSES_FILENAME_CSV
    responses_csv = open(responses_filepath, newline='')
    responses_2d_array = list(csv.reader(responses_csv))
    return responses_2d_array

def create_competitor_list(responses_2d_array: List[List[str]]) -> Tuple[List[rutils.Competitor], int]:
    # Go through the matrix until the "usernames" column(s) are found.
    for col in range(0, len(responses_2d_array[0])):
        if "Username" in responses_2d_array[0][col]:
            # # If the next column is for newbies to type their username,
            # set a flag to overwrite the competitor in the first column with the second.
            has_newbie_column = col < len(responses_2d_array[0]) - 1 and "Username" in responses_2d_array[0][col + 1]
            competitor_list = list()
            row = 1
            while row < len(responses_2d_array):
                username = ""
                if (has_newbie_column and len(responses_2d_array[row][col + 1]) > 0):
                    username = responses_2d_array[row][col + 1]
                else:
                    username = responses_2d_array[row][col]
                competitor_list.append(rutils.Competitor(username, row))
                row += 1
            first_question_col = col + 2 if has_newbie_column else col + 1
            return competitor_list, first_question_col
        col += 1
    # If we got here, we didn't find a "Username" column, so we can't score anything...!
    rutils.abort_with_reason("Couldn't find \"Username\" column.")

def create_competitor_scores_dict(competitor_list: List[rutils.Competitor], responses_2d_array: List[List[str]], first_question_col: int, answer_dict: Dict[str, rutils.Answer]) -> Dict[str, int]:
    competitor_scores_dict = dict()
    for competitor in competitor_list:
        competitor_responses = responses_2d_array[competitor.response_row]
        # For every question
        for col in range(first_question_col, len(responses_2d_array)):

            raw_question = responses_2d_array[0][col]
            tidy_question = get_tidy_question(raw_question)
            # check if the tidy question is in the answer_dict because non-scored questions can be in responses csv,
            # but not in the answer_dict... it'll cause KeyError otherwise.
            if tidy_question not in answer_dict:
                continue
            # check if the competitor's answer is in the answer_dict for that question.
            # If so, they got it right, so give them the corresponding points!
            if competitor_responses[col] in answer_dict[tidy_question].answers:
                competitor.increment_score(answer_dict[tidy_question].point_value)
        competitor_scores_dict[competitor.username] = competitor.score
    return competitor_scores_dict

def generate_score_csv(episode_directory: str, competitor_scores_dict: Dict[str, int]) -> None:
    score_array = list()
    score_array.append(("Username", episode_directory))
    for competitor in competitor_scores_dict:
        competitor_score_row = [competitor, str(competitor_scores_dict[competitor])]
        score_array.append(competitor_score_row)
    rutils.write_2d_array_to_csv(episode_directory, rutils.SCORES_FILENAME_CSV, score_array)



# Script
print("📝 Calculating scores for the week.")
episode_range = rutils.get_episode_range()
episode_directory = rutils.get_episode_directory(episode_range)

responses_2d_array = get_responses_2d_array(episode_directory)
print("    🔑 Creating answer key dictionary...")
answer_dict = create_answer_dict(episode_directory)

print("    🎖️ Creating competitor list...")
competitor_list, first_question_col = create_competitor_list(responses_2d_array)
print("    🏆 Creating competitor scores dictionary...")
competitor_scores_dict = create_competitor_scores_dict(competitor_list, responses_2d_array, first_question_col, answer_dict)

print("    📊 Generating new scores.csv for the week...")
generate_score_csv(episode_directory, competitor_scores_dict)
print("🎉 Success!")