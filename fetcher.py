
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
    body =  soup.find("table", { "class" : "odds-table" })

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

print getEventTitle(headersoup)


def getBettingSites():
    return

def getMatches():
    return



