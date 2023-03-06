# rpdr-bracket
Coding a way to calculate and maintain scores for a friendly bracket of RuPaul's Drag Race

## Instructions
1. Run __🐍 new_week.py__, which
    - creates __📁 episodeNUMBER__ directory.
    - (inside __📁 episodeNUMBER__) creates __📊 answers.csv__. Pre-fills first column with "lip sync" question.
        - If there's a previous episode directory, it also appends the previous week's __📊 remaining.csv__ question row to __📊 answers.csv__'s question row.
2. Download this week's Google Forms responses as __📊 responses.csv__ into the new __📁 episodeNUMBER__ directory, 
3. If a question in __📊 responses.csv__ overwrites a previous round of questions (e.g. new guess for season winner), copy the original question phrasing and append the keyword __[OVERWRITE]__. (*TODO: Add this functionality, lol*)
4. Copy the question row from __📊 responses.csv__ into __📊 answers.csv__.
5. In __📊 answers.csv__, write all available answers - episode winner, lip sync song(s), etc. Leave unanswered questions blank.
6. Run __🐍 calculate_scores.py__, which
    - (inside __📁 episodeNUMBER__) creates __📊 scores.csv__.
    - creates a new column in __📊 scores.csv__ and places this week's scores in it, using __📊 answers.csv__ vs __📊 responses.csv__.

## Contents
_TODO kp: Add this!_

## To-do functionality
- Add function to note if submission was marked on time - so final score factors it in
- Process unanswered questions and put them into remaining.csv
    - Add remaining.csv questions into answers.csv at generation time
    - Add [OVERWRITE] functionality for competitors' old responses in remaining.csv to be updated
- Copy previous week's scores.csv and append this week's scores so cumulative total is visible