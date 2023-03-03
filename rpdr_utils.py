# Util variables
EPISODE_FILENAME = "episode"
LIPSYNC_QUESTION = "Guess a Lip-sync Song performed this season (Guess #1) (5 Points)"

# Util methods and classes
class Competitor:
    def __init__(self, username: str, score: int):
        self.username = username
        self.score = score    