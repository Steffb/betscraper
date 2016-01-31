__author__ = 'steffenfb'

class Event(object):
    site = ''
    name = ''

    def __init__(self,site,name):

        self.site = site
        self.name = name
        self.matches = []


class Match(object):

    fighterOneName = ''
    fighterOneLine = 0
    fighterTwoName = ''
    fighterTwoLine = 0
    fightWinnerOne = None

    def __init__(self,fighterOneName, fighterTwoName, fighterOneLine, fighterTwoLine):
        self.fighterOneLine = fighterOneLine
        self.fighterOneName = fighterOneName
        self.fighterTwoLine = fighterTwoLine
        self.fighterTwoName = fighterTwoName



