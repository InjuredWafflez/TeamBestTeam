class Scores(object):
    def __init__(self, file_name):
        self.file_name = file_name

    @property
    def file_name(self):
        return file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    # Return the top 10 high scores and names in a list
    def get_top_10(self):
        score_file = open(self._file_name, 'r')
        lines = score_file.readlines()

        scores = []

        # Get the scores and names from the file
        for line in lines:
            score, name, unwanted = line.split(",")
            score = int(score)
            scores.append([score, name])

        score_file.close()

        scores.sort(reverse = True)     # Sort the scores from high to low
        top_10 = scores[:10]            # Get the top 10 scores

        return top_10           # Return the 10 ten scores and associated name in a 2D array
    
    # Check if a given score is a new high score
    # I.e. if its in the top 10
    # returns true or false
    def check_score(self, score):
        score_file = open(self._file_name, "r+")
        lines = score_file.readlines()

        scores = []

        # Get the scores and names from the file
        for line in lines:
            score, name, unwanted = line.split(",")
            score = int(score)
            scores.append([score, name])

        score_file.close()

        scores.sort(reverse = True)     # Sort the scores from high to low

        # If the player score is greater than the 10th best score then the player score
        # is a new highscore
        if len(scores) < 10 or score >= scores[9]:
            return True
        else:
            return False

    # Add a score to the score list
    def add_score(self, name, score):
        score_file = open(self._file_name, "a+")
        score_file.write(str(score) + "," + str(name) + ",\n")
        score_file.close()



# Run the highscores code to test it
##scores = Scores("scores.txt")
##
##scores.add_score("Bob", 100)
##scores.add_score("Mark", 80)
##scores.add_score("Jim", 90)
##
##top = scores.get_top_10()
##
##print top
##
##print top[1][0]


    
