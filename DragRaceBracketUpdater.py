import csv
import numpy as np
import re

class Answer:
    # Answer object contains a set "answers" and an int "pointValue"
    def __init__(self, answers, pointValue):
        self.answers = answers
        self.pointValue = pointValue

class Competitor:
    def __init__(self, username, row):
        self.username = username
        self.row = row
        # TODO ip: Add feature for checking if submission was on time
        self.submittedOnTime = False
        self.pointsWon = int(0)

    def setSubmittedOnTime(self, value):
        self.submittedOnTime = value

    def incrementPoints(self, value):
        self.pointsWon += int(value)

def createAnswerKeyDict(answerKeyCsvFilepath):
    answerKeyCsv = open(answerKeyCsvFilepath, newline='')
    answerKey2dArray = list(csv.reader(answerKeyCsv))
    answerKeyDict = dict()
    # For each column in the answerkey 2D array,
    col = 0
    while col < len(answerKey2dArray[0]):
        # get question text and points value first
        rawQuestion = answerKey2dArray[0][col]
        questionText = getQuestionText(rawQuestion)
        pointValue = getPointValue(rawQuestion)
        # If there are no points available, don't add this to the answer key. It might be a just-for-fun question.
        if pointValue == -1:
            col += 1
            continue
        # Otherwise, grab all possible answers for that question:
        answerSet = set()
        # First, scan the next columns to see if the questions are identical besides their parentheses substrings.
        # If they're identical, the question is the same, so the answer is another possible correct answer.
        while col < len(answerKey2dArray[0]) and questionText == getQuestionText(answerKey2dArray[0][col]):
            answerSet.add(answerKey2dArray[1][col])
            col += 1
        # At this point we're either out of bounds or we've found a different question, so put the found answers in the dict.
        answerKeyDict[questionText] = Answer(answerSet, pointValue)
    return answerKeyDict

def getCompetitors(bracketArray):
    col = int(0)
    while col < len(bracketArray[0]):
        if "Username" in bracketArray[0][col]:
            competitorList = []
            row = 1
            while row < len(bracketArray):
                username = bracketArray[row][col]
                competitorList.append(Competitor(username, row))
                row += 1
            return competitorList
        col += 1

def calculateCompetitorScore(competitor, firstQuestionCol, answerArray, answerKey):
    # We can skip the timestamp/email/username columns since we know when the questions begin. Small time-saver.
    col = firstQuestionCol
    while col < len(answerArray[0]):
        question = answerArray[0][col]
        questionText = getQuestionText(question)
        userAnswer = answerArray[competitor.row][col]

        if userAnswer in answerKey[questionText].answers:
            competitor.incrementPoints(answerKey[questionText].pointValue)
        col += 1
    print(competitor.username, " earned ", competitor.pointsWon, " in this bracket.")

def getQuestionText(question):
    questionText = re.findall(r'^[^\(]*', question)
    questionText = questionText[0].strip()
    return questionText

def getPointValue(question) -> int:
    parenthesesSubstrings = re.findall('\(.*\)*', question)
    lastParenthesesSubstring = parenthesesSubstrings[len(parenthesesSubstrings) - 1]
    rawPointValue = re.findall(r'\d+', lastParenthesesSubstring)
    pointValue = rawPointValue[len(rawPointValue) - 1]
    if not pointValue:
        print("    WARN: No point value for ", question)
        return -1
    return pointValue

print("Drag Race Bracket Updater!\n")
answerKeyFilename = "answers.csv"
bracketFilename = "bracket.csv"

answerKeyDict = createAnswerKeyDict(answerKeyFilename)
bracketCsv = open(bracketFilename, newline='')
bracketArray = list(csv.reader(bracketCsv))
competitors = getCompetitors(bracketArray)
# TODO ip: Calculate first question column.
firstQuestionCol = 2
for competitor in competitors:
    calculateCompetitorScore(competitor, 2, bracketArray, answerKeyDict)