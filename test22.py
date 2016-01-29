__author__ = 'steffenfb'

import unittest
import fetcher

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





if __name__ == '__main__':
    unittest.main()
