from Objects import *
import urllib2
from bs4 import BeautifulSoup
import re
import datetime
import urllib
import misc
# Used for fetching the page content

from difflib import SequenceMatcher


def useLocalHTMLFile():

    html = readLocal('html')
    return html

def getContentFromURL(url):

    page  = urllib2.urlopen(url)
    if(page.getcode() != 200):
        print 'Error code %d when fetching page '% (page.getcode())
        return

    html = page.read()
    return html, page.getcode()

def saveHTMLToLocal(url, filename):
    content  = getContentFromURL(url)
    file = open(filename,'w')
    file.write(content)
    file.close()

def readLocal(filename):
    file = open(filename,'r')
    html = file.read()
    file.close()
    return html

def getEventName(headerSoup):

    return headerSoup.find('a').string

    #Returns the table header, the table and the whole soup
def createSoups(html):
    if (html is None):
        print 'No html in createsoups'
        return None
    soup = BeautifulSoup(html,"html.parser")
    header =  soup.find("div", { "class" : "table-header" })
    body =  soup.findAll(lambda tag: tag.name == 'table' and tag.get('class') == ['odds-table'])


    headerSoup = BeautifulSoup(str(header),"html.parser")
    tableSoup = BeautifulSoup(str(body),"html.parser")




    return headerSoup,tableSoup,soup

 # returns the winne of a fight
def getWinner(fighterOneName, fighterTwoName, Event):
    None



#Convert from string to datetime object

#Not currently used
def convertMmaDateToWikiDate(datestring):

    month = datestring[:3]

    monthsList = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    month = month.lower()
    pos = None
    for i in range(len(monthsList)):
        if(monthsList[i] in month):
            pos = i+1

    if not (pos):
        print ' Error when finding month in string %s'%(datestring)
        return None

    day = re.search('\D\d\d\D|\D\d\D',datestring).group()
    if(len(day) is 3):
        day = re.search('\d',day).group()
    else:
        day = re.search('\d\d',day).group()


    year = re.search('\d\d\d\d',datestring).group()

    return datetime.date(int(year),int(pos),int(day))

    # TODO:Split on space, keep first three letters. keep next number, prob by regex.



def getEventTitleAndDate(headersoup):
    if(len(headersoup.find_all('a'))==1):
        date = headersoup.find('span', {'class':'table-header-date'}).contents[0]

        return headersoup.find_all('a')[0].text,date
    else:
        print 'Incorrect amount of header title found'

#obj = createSoups(useLocalHTMLFile())

#headersoup = obj[0]
#tablesoup = obj[1]

#print getEventTitleAndDate(headersoup)

# Returns name of the betting site and the table index position
def getSiteFromHeader(siteName, tablesoup):

    headers = tablesoup.find('thead').findAll('th')

    bettinSites = []

    for h in headers:

        if h.find('a') != None:
            bettinSites.append( h.find('a').contents[0])
        else:
            bettinSites.append('Empty')

    for site in bettinSites:
        if siteName in site:
            return site, bettinSites.index(site)
    return None



#From bestfigh odds.com
def getfights(siteIndex, tablesoup):

    fights = []
    tablerowseven = tablesoup.find('tbody').findAll('tr', {'class' : 'even' })
    tablerowsodd= tablesoup.find('tbody').findAll('tr', {'class' : 'odd' })


    fighterOne =''
    lineOne = 0
    fighterTwo = ''
    lineTwo = 0
#TODO: Make flexible to get other bettin lines
    for i in range(len(tablerowseven)):
        if tablerowseven[i].find('th').find('a').find('span') is not None:
            fighterOne = tablerowseven[i].find('th').find('a').find('span').contents[0]
            lineOne = tablerowseven[i].find('td').find('a').find('span').find('span').contents[0]
        if tablerowsodd[i].find('th').find('a').find('span') is not None:
           fighterTwo = tablerowsodd[i].find('th').find('a').find('span').contents[0]
           lineTwo = tablerowsodd[i].find('td').find('a').find('span').find('span').contents[0]

        fights.append(Match(fighterOne, fighterTwo, convertToOdds(lineOne), convertToOdds(lineTwo)))


        #print tablerow.find('th').find('a').find('span').contents[0]

    return fights


def convertToOdds(line):

    symbol = line[:1]

    number = float(line[1:])

    if('+' in symbol):
        return number/100 + 1
    elif('-' in symbol):
        return float("{0:.2f}".format(100/number + 1))


    else:
        return None


def getWikiFightByName():

    events = []

    url = 'https://en.wikipedia.org/wiki/List_of_UFC_events'
    wikiSoup = createSoups( getContentFromURL(url)[0])[2]


    tables = wikiSoup.findAll('table', {'class': 'sortable wikitable succession-box'})
    upcomingEventTable = tables[0]
    pastEventTable = tables[1]

    pastBody = pastEventTable.findAll('tr')



    for row in pastBody:
        fields = row.findAll('td')
        if len(fields)>2:
            link = 'https://en.wikipedia.org'
            name = fields[1].find('a').contents[0]
            link = fields[1].find('a')['href']
            date = convertMmaDateToWikiDate(fields[2].find('span',{'style':'white-space:nowrap'}).contents[0])

            events.append(Event(link,name,date))

    return events

    # Compares the name to event name on wikiSite

def findEventByName(name, events):
    ratio = -1
    bestEvent = None
    for event in events:

        if (event.name is name):
            return event

        seq=SequenceMatcher(a=name.lower(), b=event.name.lower())
        if(ratio < seq.ratio()):
            ratio = seq.ratio()
            bestEvent = event

        #print 'checking |%s| \t vs \t |%s| similarity %d'%(name,event.name,ratio)

    return bestEvent

    #table = misc.findElementByClass(wikiSoup,'table','sortable wikitable succession-box')

def compareStringSimilarity(stringOne, stringTwo):
    seq=SequenceMatcher(a=stringOne.lower(), b=stringTwo.lower())
    return seq.ratio()

def getWikiFightResults(url):
    soup = createSoups(getContentFromURL(url)[0])[2]

    fights = []

    table = soup.find('table',{'class':'toccolours'})

    tablerows = table.findAll('tr')

    for row in  tablerows:
        fields = row.findAll('td')
        if (len(fields)> 3 ):

            if(len(fields[1].contents) is 0 or len(fields[3].contents) is 0):
                continue

            winner = fields[1].text
            loser = fields[3].text




            fights.append(WinnerLoser(winner,loser))

    return fights

#Assumes that the first event hit on search is the correct one
def getEventPageFromName(eventName):
    query = urllib.quote_plus(eventName)
    url = 'http://www.bestfightodds.com/search?query='
    url+=query
    #print 'current url is :%s'%(url)
    content = getContentFromURL(url)[0]
    soup = createSoups(content)[2]
    tables = soup.findAll('table',{'class':'content-list'})
    table = None
    # Find event table
    for t in tables:

        if(len(t.find('td',{'class':'content-list-date'}).contents) is not 0):

            table = t
            break
    if(table is None):
        print 'Did not find table '
        return None
    firstRow = table.find('tr')
    rowParts = firstRow.findAll('td')
    link = rowParts[1].find('a')
    url = link['href']
    name = link.contents[0]


    return name,url


def getEventDataByName(eventName):

    #getContentFromURL('www.bestfightodds.com'+getEventPageFromName(eventName)[1])
    return None


#getWikiFightByName()

