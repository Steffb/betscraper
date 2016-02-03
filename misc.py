__author__ = 'steffenfb'



#body =  soup.findAll(lambda tag: tag.name == 'table' and tag.get('class') == ['odds-table'])



def findElementByClass(soup,elementType, tclass):

    classElement =  soup.find(elementType, { "class" : tclass })

    return classElement



