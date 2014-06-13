import string
import re
#need this later for extracting file names?
#import os
#os.walk(subdir)

inFile = open('shelftemp_logs/20140611_13-05', 'r')
outFile = open('output20140611_13-05.txt', 'w')

# associative arrays for the temperatures and fans, respectively
temp_array = [0 for i in range(22)]
fan_array = [[0 for i in range(4)] for j in range(22)]
format_array = [[0 for i in range(3)] for j in range(88)]

def extract():
    global inFile
    shelf = 0
    prevdisk = 0

    temp_idx = 0
    fan_idx = 0
    format_idx = 0
    fancount = 0

    for linenum, line in enumerate(inFile):
        # turns out that lines that start with a space,
        # contain the speed for fans that don't even exist...
        if (line[0] != ' ' and linenum > 3):
            word1 = line.partition(' ')[0]
            if (word1 == "Shelf"):
                fancount = 0
                numarray = re.split('[^\d]+', line) #hooray for regular expressions! 
                temperature = int(numarray[-2:][0])

                temp_array[temp_idx] = temperature
                temp_idx += 1
            elif (fancount < 4 and word1 == "Actual"):
                #if fan_idx > 3:
                #    fan_idx = 0
                numarray = re.split('[^\d]+', line)
                fanspeed = int(numarray[1])

                #fan_array[temp_idx-1][fan_idx] = fanspeed

                format_array[format_idx] = [temp_array[temp_idx-1], fanspeed, 1]

                format_idx += 1
                fancount += 1
                #fan_idx += 1

def writeToFile():
    global outFile
    for elem in format_array:
        outFile.write(str(elem[0]) + " " + str(elem[1]) + "\n")

def processList():
    sorted_array = sorted(format_array, key = lambda x: (x[0], x[1]))
    output = []
    out_idx = 0
    print sorted_array

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


extract()
processList()
#writeToFile()

inFile.close(), outFile.close()
#print format_array
#print temp_array
#print fan_array

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
'''
