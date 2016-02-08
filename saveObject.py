__author__ = 'steffenfb'

import pprint
from  marshmallow import fields,Schema,post_load
import datetime as dt
from Objects import *

import dexml

from dexml import fields








class xMatch(dexml.Model):

    fighterOneName = fields.String()
    fighterOneLine = fields.Integer()
    fighterTwoName = fields.String()
    fighterTwoLine = fields.Integer()
    fightWinnerWinner = fields.String()

class xEvent(dexml.Model):
    site = fields.String()
    name = fields.String()
    match =fields.List(xMatch)


class xWinnerLoser(dexml.Model):
    winner = fields.String()
    loser = fields.String()


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

