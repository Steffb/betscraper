__author__ = 'steffenfb'
from saveObject import xAll

#file  = open('bigobjTest','r')
file  = open('bigobj','r')
xml = file.read()

obj = xAll.parse(xml)

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

                    profit +=match.fightUnderdog()[1]
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

def betEqualOnFavoriteOnEvent(obj):

    profit = 0

    wins = 0
    loss= 0
    evals = 0
    for event in obj.eventList:
        for match in event.match:

            if(match.fightUnderdog()):
                evals+=1
                if(match.getFightWinner() == match.fightUnderdog()[0]):
                    profit -=1
                    loss+=1


                 #   print 'correct'
                elif(match.getFightLoser() == match.fightUnderdog()[0]):
                    profit +=match.fightFavorite()[1]
                    wins+=1
                #else:

               #     print 'wrong'

                #print 'status: '+str(profit)

    print '[Your profit] '+str(profit)
    print '[Your Wins] '+ str(wins)
    print '[Your losses]'+ str(loss)
    print '[Total evals ]'+ str(evals)

#print betEqualOnUnderdogOnEvent(obj)
print betEqualOnFavoriteOnEvent(obj)





