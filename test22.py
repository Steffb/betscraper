from Objects import WinnerLoser

__author__ = 'steffenfb'

import unittest
import fetcher
import datetime
from Objects import *

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


    def testEventMatching(self):
        events = fetcher.getWikiFightByName()

        for event in events:

            print '%s \t matched with %s'%(event.name,fetcher.getEventPageFromName(event.name)[0])


#Convert from
# January 17th
#Jan 17, 2016


if __name__ == '__main__':
    unittest.main()
