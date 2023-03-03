# rpdr-bracket
Coding a way to calculate and maintain scores for a friendly bracket of RuPaul's Drag Race

## Instructions
1. Run __🐍 new_week.py__, which
    - creates __📁 epNUMBER__ directory.
    - (inside __📁 epNUMBER__) creates __📊 answers.csv__. Pre-fills first column with "lip sync" question.
        - If there's a previous episode directory, it also appends the previous week's __📊 remaining.csv__ question row to __📊 answers.csv__'s question row.
    - (inside __📁 epNUMBER__) creates __📊 scores.csv__.
        - If there's a previous episode directory, it also copies the previous week's __📊 scores.csv__ into __📁 epNUMBER__.
2. Download this week's Google Forms responses as __📊 responses.csv__ into the new __📁 epNUMBER__ directory, 
3. If a new user has entered this week, overwrite their dummy dropdown username with their actual username. Delete the column after.
4. If a question in __📊 responses.csv__ overwrites a previous round of questions (e.g. new guess for season winner), copy the original question phrasing and append the keyword __[OVERWRITE]__.
5. Copy the question row from __📊 responses.csv__ into __📊 answers.csv__.
(Enjoy the episode)
6. In __📊 answers.csv__, write all available answers - episode winner, lip sync song(s), etc. Leave unanswered questions blank.
7. Run __🐍 calculate_scores.py__, which
    - calculates scores based on correct answers in __📊 answers.csv__ vs __📊 responses.csv__.
    - creates a new column in __📊 scores.csv__ and places this week's scores in it.
    - puts unanswered questions in a new __📊 remaining.csv file__.

## Contents
_TODO kp: Add this!_