__author__ = 'steffenfb'

import datetime
class Event(object):
    site = ''
    name = ''
    match =[]

    def __init__(self,site,name,date):

        self.site = site
        self.name = name
        self.matches = []
        self.date = date



class Match(object):

    fighterOneName = ''
    fighterOneLine = 0
    fighterTwoName = ''
    fighterTwoLine = 0
    fightWinnerWinner = ''


    def __init__(self,fighterOneName, fighterTwoName, fighterOneLine, fighterTwoLine):
        self.fighterOneLine = fighterOneLine
        self.fighterOneName = fighterOneName
        self.fighterTwoLine = fighterTwoLine
        self.fighterTwoName = fighterTwoName


class WinnerLoser(object):

    def __init__(self, winner, loser):
        self.winner = winner
        self.loser = loser
    #TODO:Find the correct figther

    def findByNames(self, name):

        if (name in self.winner):
            return self.winner
        elif (name in self.loser):
            return self.loser

        else:
            print 'No name match on |%s| in find by names'%(name)
            return None

