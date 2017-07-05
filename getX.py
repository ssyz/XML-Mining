from xml.dom.minidom import parse
import xml.dom.minidom
import tempfile


#TODO: remove junk after document -- probably the repeated XML headers

# Open XML document using minidom parser
#DOMTree = xml.dom.minidom.parse("exOnly.xml")


#TODO: print in order
#   (1) header - e.g. <us-patent-grant lang="EN" dtd-version="v4.2 2006-08-23" file="USD0584026-20090106.XML" status="PRODUCTION" id="us-patent-grant" country="US" date-produced="20081222" date-publ="20090106">
#   (2) invention title
#   (3) inventor(s)
#   (4) citations?
#
# getElementsByTagName finds every element by name, regardless of heirarchy
# use hasAttribute to only extract certain tagged items


'''(1) Retrieve all header items as a string'''
def getHea():
    headList = DOMTree.getElementsByTagName("us-patent-grant")
    for headItem in headList:
        items = headItem.attributes.items()
        strItems = ' '.join(str(e) for e in items)
        print(strItems)

'''Retrieve Patent ID as a string'''
def getID():
    pubRefList = DOMTree.getElementsByTagName("publication-reference")
    for elem in pubRefList:
        print(elem.firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling.firstChild.data)

'''(2) Retrieve invention titles as a string'''
def getTit():
    titleList = DOMTree.getElementsByTagName("invention-title")
    for title in titleList:
        print (title.firstChild.data)

'''(3) Retrieve inventor names as a string'''
def getInv():
    inventorList = DOMTree.getElementsByTagName("applicant")
    invs = ""
    for inventor in inventorList:
        if (inventor.getAttribute("app-type") == "applicant-inventor"):
            last = inventor.firstChild.nextSibling.firstChild.nextSibling
            first = inventor.firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling
            full = last.firstChild.data + ", " + first.firstChild.data
            invs += full

    return invs

'''(4) Retrieve citation pacit num, document number and names as a string'''
def getCit():
    citList = DOMTree.getElementsByTagName("citation")
    cits = ""
    for citation in citList:
        n = citation.childNodes
        #print (n)
        # patcit num
        num = n[1].getAttribute("num")
        #print (num)
        # doc-number
        dN = n[1].firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling.firstChild.data
        # name
        nN = n[1].firstChild.nextSibling.firstChild.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.firstChild.data
        cits += num + " (" + dN + ") " + nN + "; "

    #return cits

#def createXML():



# main method
def main():
    f = open("ex2.xml")
    xml = ""
    line = 0
    lines = f.readlines()
    #print (lines)
    indexes = [i for i,x in enumerate(lines) if x.startswith("<?xml ")]
    print (indexes)

    #temporary file
    print ('creating a temporary file...')
    temp = tempfile.TemporaryFile()
    try:
           #data = '\n'.join(lines[:indexes[1]])
           #data = '\n'.join(lines[indexes[1]:indexes[2]])
           data = '\n'.join(lines[indexes[2]:])
           temp.write(data.encode('utf-8'))
           temp.seek(0)
           #byte file
           pt = temp.read()
           #string file
           ptS = pt.decode()
           #TODO: process temporary file
           print (ptS)
    finally:
           temp.close()


# call main method
if __name__ == '__main__':
    main()
