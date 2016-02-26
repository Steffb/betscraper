from Objects import WinnerLoser

__author__ = 'steffenfb'

import unittest
import fetcher
import datetime
from Objects import *
import pandas as pd
import dill
import json
from saveObject import xMatch,xEvent,xAll
import objectQuery

class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, True)



    def test_pageFetching(self):
        self.assertEqual(200, fetcher.getContentFromURL('https://www.bestfightodds.com/events/ufc-on-fox-18-johnson-vs-bader-1038')[1])



    def test_tableparsing(self):

        obj = fetcher.createSoups(fetcher.useLocalHTMLFile())

        headersoup = obj[0]
        tablesoup = obj[1]
        print 'here comes header'
        self.assertTrue ('UFC' in headersoup.find("div", { "class" : "table-header" }).find('a').contents[0])

    def testheaderparsingofSites(self):
        obj = fetcher.createSoups(fetcher.useLocalHTMLFile())
        tablesoup = obj[1]
        self.assertEqual('5Dimes' , fetcher.getSiteFromHeader('5Dim',tablesoup)[0])

    def testFightFetching(self):
        obj = fetcher.createSoups(fetcher.useLocalHTMLFile())
        tablesoup = obj[1]
        matches = fetcher.getfights(1, tablesoup)
        self.assertEqual('Donald Cerrone', matches[0].fighterOneName)
        self.assertEqual(2.50, matches[0].fighterOneLine)
        self.assertEqual('Rafael Dos Anjos', matches[0].fighterTwoName)
        self.assertEqual(1.59, matches[0].fighterTwoLine)


    def testLineConverter(self):

        self.assertEqual(2.50, fetcher.convertToOdds('+150'))
        self.assertEqual(1.59, fetcher.convertToOdds('-170'))

    def testWinnerOfEvent(self):
        None





    def testDateToWikiDateConvertions(self):
        self.assertEqual(datetime.date(2010,8,28), fetcher.convertMmaDateToWikiDate('Aug 28, 2010'))
        self.assertEqual(datetime.date(2010,8,28), fetcher.convertMmaDateToWikiDate('Aug 28th 2010'))

        self.assertEqual(datetime.date(2009,12,12), fetcher.convertMmaDateToWikiDate('Dec 12th 2009	'))
        self.assertEqual(datetime.date(2009,1,31), fetcher.convertMmaDateToWikiDate('Jan 31st 2009'))
        self.assertEqual(datetime.date(2013,2,2), fetcher.convertMmaDateToWikiDate('Feb 2nd 2013'))

    @unittest.skip
    def testGetWikiEvents(self):
        events = fetcher.getWikiFightByName()

        self.assertEqual('UFC on Fox: Johnson vs. Bader',fetcher.findEventByName('UFC on Fox: Johnson vs. Bader', events).name)

        self.assertEqual('/wiki/UFC_on_Fox:_Johnson_vs._Bader', events[0].site)
        self.assertEqual(datetime.date(2016,1,30), events[0].date)
        self.assertEqual('UFC on Fox: Johnson vs. Bader', events[0].name)


    def testWinnerLoserFindByName(self):
        wl = WinnerLoser('winnerName', 'LoserName')
        self.assertEqual('winnerName', wl.findByNames('winnerName'))

        self.assertEqual('LoserName', wl.findByNames('LoserName'))
        
    def testGetFightsByUrl(self):
        fights = fetcher.getWikiFightResults('https://en.wikipedia.org/wiki/UFC_on_Fox:_Johnson_vs._Bader')

        self.assertEqual('Anthony Johnson',fights[0].winner)

        self.assertEqual('Ryan Bader',fights[0].loser)



    def testGetEventpageByName(self):

        eventPage = fetcher.getEventPageFromName('UFC Fight Night: Dillashaw vs. Cruz')

        eventName = eventPage[0]
        eventUrl = eventPage[1]
        self.assertEqual('UFC FIGHT NIGHT 81: DILLASHAW VS. CRUZ',eventName.upper())

        self.assertEqual('/events/ufc-fight-night-81-dillashaw-vs-cruz-1022',eventUrl)

    @unittest.skip
    def testEventMatching(self):
        events = fetcher.getWikiFightByName()

        for event in events:

            eventname = event.name.encode('utf-8')
            fetchedEvent = fetcher.getEventPageFromName(eventname)[0].encode('utf-8')
            ratio = fetcher.compareStringSimilarity(eventname, fetchedEvent)

            if(ratio< 0.9):
                print eventname+" |\t | "+fetchedEvent+'|\t ratio:'+str(ratio)
            #print '%s \t matched with %s \t %s'%(,fetcher.compareStringSimilarity(event.name, fetcher.getEventPageFromName(eventname)[0]))

    @unittest.skip
    def testUnicode(self):
        events = fetcher.getWikiFightByName()


        for e in events:

            if('illa'.decode() in e.name ):
                print e.name



    def testCompareString(self):
        ratio  = fetcher.compareStringSimilarity('hello','hello')

        self.assertEqual(1,ratio)

#Convert from
# January 17th
#Jan 17, 2016

    def testCreateEvent(self):

        events = fetcher.getWikiFightByName()
        event =  events[0]
        wlobjs = fetcher.getWikiFightResults(event.site)
        #url = fetcher.getEventPageFromName(event.name)
        data =fetcher.getEventDataByName(event.name)
        result = fetcher.joinResultAndLines(data,wlobjs)

        self.assertEqual('Stephen Thompson',result[0].fightWinnerWinner)
        self.assertEqual(1.34,result[0].fighterOneLine)
        self.assertEqual(3.45,result[0].fighterTwoLine)





    def testGetEventLines(self):
        matches = fetcher.getEventDataByName('UFC 190: Rousey vs. Correia')
        m1 = matches[0]
        self.assertEqual('Bethe Correia',m1.fighterOneName)
        self.assertEqual('Ronda Rousey',m1.fighterTwoName)
        self.assertEqual(12 ,m1.fighterOneLine)
        self.assertEqual(1.06 ,m1.fighterTwoLine)
        m1 = matches[-1]
        self.assertEqual('Guido Cannetti',m1.fighterOneName)
        self.assertEqual('Hugo Viana',m1.fighterTwoName)
        self.assertEqual(5.5 ,m1.fighterOneLine)
        self.assertEqual(1.17 ,m1.fighterTwoLine)



    def testJson(self):

        wl = WinnerLoser('one','two')
        ww = dill.dump_session('dill.pkl')
        print ww


    def testXmatchfightUnderdog(self):
        match = xMatch(fighterOneName='f1n',fighterOneLine=1,fighterTwoLine=2,fighterTwoName='f2n')
        self.assertEqual(match.fighterTwoName, match.fightUnderdog()[0])


    def testBetOnFavoriteOnOneEvent(self):


        obj = objectQuery.readxAll('bigobj')

        for event in obj.eventList:
            if('Marquardt vs. Palhares' in event.name):
                result = objectQuery.betonFavoriteOnOneEvent(event)

                wins=result[0]
                loss=result[1]
                profit=result[2]
                evals=result[3]

        self.assertEqual(3,wins)


    def testBetScopeRange(self):

        match = xMatch(fighterOneName='mrwinner', fighterOneLine=1, fighterTwoName='mrloser', fighterTwoLine=2, fightWinnerWinner='mrwinner')

        event = xEvent(site= 'www.abc.com', name = 'yeye')

        event.match.append(match)
        eventlist = []
        eventlist.append(event)
        obj = xAll(eventList = eventlist)
        res = objectQuery.scopeBetRange(obj,0.9,1.1)

        self.assertEqual(1,res)



if __name__ == '__main__':
    unittest.main()
