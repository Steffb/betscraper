__author__ = 'steffenfb'
from saveObject import xAll

#file  = open('bigobjTest','r')




def readxAll(filename):
    file  = open(filename,'r')
    xml = file.read()

    return xAll.parse(xml)


def printOutEvent(obj):

    for e in obj.eventList:
        print '[NEW EVENT]: %s'%(e.name)
        for match in  e.match:



            print '\t'+match.fighterOneName+'\t'+str(match.fighterOneLine)

            print '\t'+match.fighterTwoName+'\t'+str(match.fighterTwoLine)

            print '\t[Winner] '+str(match.fightWinnerWinner)
            print


#printOutEvent(obj)





def betEqualOnUnderdogOnEvent(obj):

    profit = 0

    wins = 0
    loss= 0
    evals = 0
    for event in obj.eventList:
        for match in event.match:

            if(match.fightUnderdog()):
                evals+=1
                if(match.getFightWinner() == match.fightUnderdog()[0]):

                    profit +=(match.fightUnderdog()[1] -1 )
                    wins+=1
                 #   print 'correct'
                elif(match.getFightLoser() == match.fightUnderdog()[0]):
                #else:
                    profit -=1
                    loss+=1
               #     print 'wrong'

                #print 'status: '+str(profit)

    print '[Your profit] '+str(profit)
    print '[Your Wins] '+ str(wins)
    print '[Your losses]'+ str(loss)
    print '[Total evals ]'+ str(evals)


def betonFavoriteOnOneEvent(event):
    evals = 0
    profit = 0
    wins = 0
    loss =0
    for match in event.match:


            if(match.fightUnderdog()):
                evals+=1
                if(match.getFightWinner() == match.fightUnderdog()[0]):
                    profit -=1
                    loss+=1

                 #   print 'correct'
                elif(match.getFightLoser() == match.fightUnderdog()[0]):
                    #Removed bet when adding up profit.
                    profit +=(match.fightFavorite()[1] -1)
                    wins+=1


    return wins,loss,profit,evals

def betEqualOnFavoriteOnEvent(obj):

    profit = 0

    wins = 0
    loss= 0
    evals = 0
    counter = 0
    winEvent =0
    lossEvent =0
    for event in obj.eventList:
        counter+=1
        if(counter%20 == 0):
            print '[Your profit] '+str(profit)
            print '[Your Wins] '+ str(wins)
            print '[Your losses]'+ str(loss)
            print '[Total evals ]'+ str(evals)
            print '============================='
            profit = 0

            wins = 0
            loss= 0
            evals = 0
            counter = 0

        result = betonFavoriteOnOneEvent(event)

        wins+=result[0]
        loss+=result[1]
        profit+=result[2]
        evals+=result[3]

    print '[Your profit] '+str(profit)
    print '[Your Wins] '+ str(wins)
    print '[Your losses]'+ str(loss)
    print '[Total evals ]'+ str(evals)

    print '[EvenWins] '+str(winEvent)
    print '[EventLoss] '+str(lossEvent)

#print betEqualOnUnderdogOnEvent(obj)


obj = readxAll('bigobj')
#print betEqualOnFavoriteOnEvent(obj)

print betEqualOnUnderdogOnEvent(obj)





