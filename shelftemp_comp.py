import string
import re
import os

# storing temperatures
temp_array = []
# stores array of a temperature, fanspeed, and count
format_array = []

def extract(inFile):
    shelf = 0
    prevdisk = 0

    temp_idx = 0
    fan_idx = 0
    format_idx = 0
    fancount = 0

    server = ""

    for linenum, line in enumerate(inFile):
        # turns out that lines that start with a space,
        # contain the speed for fans that don't even exist...
        if (linenum == 2):
            server = line.split()[-1]
        elif (linenum > 5 and line[0] != ' '):
            word1 = line.partition(' ')[0]
            if (word1 == "Shelf"):
                fancount = 0
                numarray = re.split('[^\d]+', line) #hooray for regular expressions! 
                temperature = int(numarray[-2:][0])

                temp_array.append(temperature)
                temp_idx += 1
            elif (fancount < 4 and word1 == "Actual"):

                numarray = re.split('[^\d]+', line)
                fanspeed = int(numarray[1])

                format_array.append([temp_array[temp_idx-1], fanspeed, 1])

                format_idx += 1
                fancount += 1

    #print format_array

def getFiles():
    temp_array = []
    list_dir = filter(lambda x: not x.startswith('.'), os.listdir('shelftemp_logs'))

    for filename in list_dir:
        inFile = open('shelftemp_logs/' + filename, 'r')
        extract(inFile)
        inFile.close()

def processList():
    sorted_array = sorted(format_array, key = lambda x: (x[0], x[1]))
    output = []
    out_idx = 0

    for i in range(len(sorted_array)-1):
        if (i == 0):
            output.append(sorted_array[i])
        elif (output[out_idx][0] == sorted_array[i][0] and 
            output[out_idx][1] == sorted_array[i][1]):
            output[out_idx][2] += 1
        else:
            out_idx += 1
            output.append(sorted_array[i])

    print output

getFiles()
processList()
#writeToFile()


'''
# counts entries (used for determining array size)
def count():
    global inFile, outFile
    count = 0

    for linenum, line in enumerate(inFile):
        # turns out that lines that start with a space,
        # contain the speed for fans that don't even exist...
        if (line[0] != ' ' and linenum > 3):
            word1 = line.partition(' ')[0]
            if (word1 == "Shelf"):
                count += 1
                
            #elif (word1 == "Actual"):
    print count

count()

def writeToFile():
    global outFile
    for elem in format_array:
        outFile.write(str(elem[0]) + " " + str(elem[1]) + "\n")

'''
