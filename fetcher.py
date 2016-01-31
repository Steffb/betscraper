from Objects import *
import urllib2
from bs4 import BeautifulSoup
# Used for fetching the page content




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
    soup = BeautifulSoup(html,"html.parser")
    header =  soup.find("div", { "class" : "table-header" })
    body =  soup.findAll(lambda tag: tag.name == 'table' and tag.get('class') == ['odds-table'])


    headerSoup = BeautifulSoup(str(header),"html.parser")
    tableSoup = BeautifulSoup(str(body),"html.parser")

    headerSoup.find('a').string



    return headerSoup,tableSoup,soup






def getEventTitle(headerSoup):
    if(len(headersoup.find_all('a'))==1):

        return headersoup.find_all('a')[0].text
    else:
        print 'Incorrect amount of header title found'

obj = createSoups(useLocalHTMLFile())

headersoup = obj[0]
tablesoup = obj[1]

#print getEventTitle(headersoup)

# Returns name of the site and the table index position
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

        fights.append(Match(fighterOne, fighterTwo, lineOne, lineTwo))


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

