__author__ = 'steffenfb'

import pprint
from  marshmallow import fields,Schema,post_load
import datetime as dt
from Objects import *

import dexml

from dexml import fields



class xMatch(dexml.Model):

    fighterOneName = fields.String()
    fighterOneLine = fields.Float()
    fighterTwoName = fields.String()
    fighterTwoLine = fields.Float()
    fightWinnerWinner = fields.String()

    def fightUnderdog(self):

        if(self.fighterOneLine > self.fighterTwoLine ):
            return self.fighterOneName,self.fighterOneLine

        elif(self.fighterTwoLine > self.fighterOneLine):


            return self.fighterTwoName,self.fighterTwoLine

        else:
            return None

    def fightFavorite(self):

        if(self.fighterOneLine < self.fighterTwoLine ):
            return self.fighterOneName,self.fighterOneLine

        elif(self.fighterTwoLine < self.fighterOneLine):


            return self.fighterTwoName,self.fighterTwoLine

        else:
            return None


    def getFightWinner(self):
        return self.fightWinnerWinner

    def getFightLoser(self):

        if(self.fighterOneName != self.fightWinnerWinner):
            return self.fighterOneName
        elif(self.fighterTwoName != self.fightWinnerWinner):
            return self.fighterTwoName
        else:
            return None

class xEvent(dexml.Model):
    site = fields.String()
    name = fields.String()
    match =fields.List(xMatch)


class xWinnerLoser(dexml.Model):
    winner = fields.String()
    loser = fields.String()


class xAll(dexml.Model):
    eventList = fields.List(xEvent)


match = xMatch(fighterOneName='mrloser', fighterOneLine=1, fighterTwoName='mrloser', fighterTwoLine=2, fightWinnerWinner='mrwinner')
matches = []
matches.append(match)
event = xEvent(site= 'www.abc.com', name = 'yeye')

event.match.append(match)


print xMatch.parse(match.render())

xml =event.render()
obj = xEvent.parse(xml)

match = obj.match

print match[0].fighterOneName

def transformMatches(EventObject):

    for i in range(len(EventObject.match)):
        current = EventObject.match[i]
        EventObject.match[i] =  xMatch(fighterOneName = current.fighterOneName, fighterOneLine =current.fighterOneLine, fighterTwoName = current.fighterTwoName,
                                       fighterTwoLine=current.fighterTwoLine, fightWinnerWinner = current.fightWinnerWinner)

    return EventObject

def transformEvent(eventObject):
    xmlEvent = xEvent(site = eventObject.site ,name = eventObject.name)

    for match in eventObject.match:
        xmlEvent.match.append(match)

    return xmlEvent


match = Match(fighterOneName='f1n',fighterOneLine=1,fighterTwoLine=2,fighterTwoName='f2n')
match.fightWinnerWinner =   'fw1'
event = Event('site','name','ji')


event.match.append(match)
print event.match[0].fighterOneName
event = transformMatches(event)

event = transformEvent(event)



xml = event.render()

print xml


ee = xEvent.parse(xml)

