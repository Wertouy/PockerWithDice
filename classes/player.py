import string
import configparser

from die import Die

config = configparser.ConfigParser()
config.read("global.ini")


class Player(object):

    def __init__(self, humanity, name):
        self.name = name
        self.humanity = humanity
        self.dice = [Die() for i in range(5)]

    def total_dice_value(self):
        total = 0
        for die in self.dice:
            total += die.value
        return total

    def report(self):
        print (self.name + " dice are:")
        diceNum = 1
        for die in self.dice:
            print ("Die " + str(diceNum) + ": [" + str(die.value + "].\n"))
            diceNum += 1

    def make_rolls(self, rolls_need_str=''):
        rolls_nedded = []
        for char in rolls_need_str:
            if char in string.digits and int(char) in range(1, 6):
                rolls_nedded.append(self.dice[int(char) - 1])
            for die in rolls_nedded:
                die.need_roll = True
            for die in self.dice:
                die.roll()

    def score(self):
        # funtion that takes a list of die and returns a score based off the dice
        numPairs = 0
        trip = False

        # Five of Kind Check
        five = True
        checkVal = self.dice[0].value
        for die in self.dice[1::]:
            if die.value != checkVal:
                five = False
                break
        if five == True:
            return config["scores"]["FIVEOFKIND"]

        # Four of Kind/Full House/Trips/Pair Check
        count = 0
        for die1 in self.dice:
            for die2 in self.dice:
                if die1.value == die2.value:
                    count += 1
            if count == 4:
                return config["scores"]["FOUROFKIND"]
            if count == 3:
                trip = True
            if count == 2:
                numPairs += 1
            count = 0
        if trip and numPairs == 2:
            return config["scores"]["FULLHOUSE"]
        if trip:
            return config["scores"]["THREEOFKIND"]
        if numPairs == 4:
            return config["scores"]["TWOPAIR"]
        if numPairs == 2:
            return config["scores"]["PAIR"]

        # six or five high straight (2-6)/(1-5) check
        diceVals = []
        for die in self.dice:
            diceVals.append(die.value)
        diceVals.sort()
        if diceVals == range(2, 7):
            return config["scores"]["SIXHIGHSTRAIGHT"]
        if diceVals == range(1, 6):
            return config["scores"]["FIVEHIGHSTRAIGHT"]

        return config["scores"]["NOTHING"]

    def score_report(self, score):
        if score == config["scores"]["NOTHING"]:
            print (self.name, "has nothing\n")
        elif score == config["scores"]["PAIR"]:
            print (self.name, "has a Pair\n")
        elif score == config["scores"]["TWOPAIR"]:
            print (self.name, "has Two Pairs\n")
        elif score == config["scores"]["THREEOFKIND"]:
            print (self.name, "has A Three of A Kind\n")
        elif score == config["scores"]["SIXHIGHSTRAIGHT"]:
            print (self.name, "has A Five High Straight\n")
        elif score == config["scores"]["SIXHIGHSTRAIGHT"]:
            print (self.name, "has A Six High Straight\n")
        elif score == config["scores"]["FULLHOUSE"]:
            print (self.name, "has A Full House\n")
        elif score == config["scores"]["FOUROFKIND"]:
            print (self.name, "has A Four of A Kind\n")
        elif score == config["scores"]["FIVEOFKIND"]:
            print (self.name, "has A Five of A Kind! WOAWH!\n")

    def full_report(self):
        self.report()
        self.score_report(self.score())

    def find_best_roll(self):
        ''' figures out what the best possible rolls are currently.
        to keep things simple it just keeps the dice that are relevent to it's current score
        and rolls the ones that don't currently help it.

        It goes through each die and sets it's value temporarly to -1. If the dice score is the same then
        that die can be rerolled.'''
        currentDie = 1
        dieValSave = -1
        baseScore = self.score()
        needRolls = ''
        for die in self.dice:
            dieValSave = die.value
            die.value = -1
            if self.score() == baseScore:
                needRolls = needRolls + str(currentDie)
            die.value = dieValSave
            currentDie += 1
        return needRolls
