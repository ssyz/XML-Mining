import xml.etree.ElementTree as ET
import tempfile


'''Retrieve Patent ID as a string'''
def getID(root):
    return root[0][0][0][1].text

'''Retrieve invention title as a string'''
def getTit(root):
    return root[0][6].text

'''Retrieve inventor(s) as a string'''
def getInv(root):
    #formatted as lastName, firstName
    invs = ""
    last = ""
    first = ""
    for i in root[0][12][0]:
        if i.attrib['app-type'] == "applicant-inventor":
            last = i[0][0].text
            first = i[0][1].text
            invs += last + ", " + first + "; "
    return "{" + invs + "}"

'''Retrieve citation pacit num, document number and names as a string'''
# what is nplcit???
def getCit(root):
    cits = ""
    for c in root[0][7]:
        if c[0].tag == 'nplcit':
            num = c[0].attrib['num']
            dN = c[1].text
            #long, so omitted
            #nN = c[0][0].text
            nN = "nplcit"
            cits += num + " (" + dN + ") " + nN + "; "
        else:
            #pacit num
            num = c[0].attrib['num']
            #document number
            dN = c[0][0][1].text
            #names
            nN = c[0][0][3].text
            cits += num + " (" + dN + ") " + nN + "; "
    return "{" + cits + "}"


'''main method'''
def main():
    f = open("ex2.xml")
    xml = ""

    '''Find the start of each XML file'''
    lines = f.readlines()
    #print (lines)
    indexes = [i for i,x in enumerate(lines) if x.startswith("<?xml ")]
    #print (indexes)


    '''Retrieve necessary data'''
    arr = []
    #first file
    first = '\n'.join(lines[:indexes[1]])
    firstRoot = ET.fromstring(first)
    fArr = [getID(firstRoot), str(firstRoot.attrib), getTit(firstRoot), getInv(firstRoot), getCit(firstRoot)]
    arr.append(fArr)

    j = 0
    k = 1
    while j+2 < len(indexes):
        j += 1
        k += 1
        #print (indexes[j],indexes[k])
        #temporary file
        #print ('creating a temporary file #' + str(k) + '...')
        temp = tempfile.TemporaryFile()
        try:
               #data = '\n'.join(lines[:indexes[1]])
               data = '\n'.join(lines[indexes[j]:indexes[k]])
               #data = '\n'.join(lines[indexes[2]:])
               temp.write(data.encode('utf-8'))
               temp.seek(0)
               #byte file
               pt = temp.read()
               #string file
               ptS = pt.decode()
               #TODO: process temporary file
               #print (ptS)
               root = ET.fromstring(ptS)
               miniArr = [getID(root), str(root.attrib), getTit(root), getInv(root), getCit(root)]
               arr.append(miniArr)
        finally:
               temp.close()

    #last file
    last = '\n'.join(lines[indexes[len(indexes)-1]:])
    #print (last)
    lastRoot = ET.fromstring(last)
    lArr = [getID(lastRoot), str(lastRoot.attrib), getTit(lastRoot), getInv(lastRoot), getCit(lastRoot)]
    arr.append(lArr)

    print (arr)


# call main method
if __name__ == '__main__':
    main()