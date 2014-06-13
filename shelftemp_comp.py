import string, re, os, itertools
from operator import itemgetter

#front only has 3 fans!!

# storing temperatures
temp_array = []
# stores array of a temperature, fanspeed, and count
format_array_count = []
format_array_server = []
output_count = []
output_server = []

def extract(inFile):
    temp_idx = 0
    # there are only 4 fans, but sometimes the log file
    # finds more than that number of fans for whatever reason
    fancount = 0

    server = ""

    for linenum, line in enumerate(inFile):
        if (linenum == 2):
            server = line.split()[-1]
        # lines that start with a space contain the speed for fans 
        # that don't even exist...
        elif (linenum > 5 and line[0] != ' '):
            word1 = line.partition(' ')[0]
            pos = re.findall(r'\'(.+?)\'', line)

            if (word1 == "Shelf"):
                fancount = 0
                numarray = re.split('[^\d]+', line) #hooray for regex! 
                temperature = int(numarray[-2:][0])

                temp_array.append(temperature)
                temp_idx += 1
            elif (not(pos == "front" and fancount >= 3) and 
                word1 == "Actual" and fancount < 4):
                numarray = re.split('[^\d]+', line)
                fanspeed = int(numarray[1])

                format_array_count.append([temp_array[temp_idx-1], fanspeed, 1])
                format_array_server.append([temp_array[temp_idx-1], fanspeed, server])
                fancount += 1

def getFiles():
    folders = filter(lambda x: not x.startswith('.'), os.listdir('shelftemp_logs'))

    for folder in folders:
        files = filter(lambda x: not x.startswith('.'), os.listdir('shelftemp_logs/'+folder))
        for filename in files:
            temp_array = []
            inFile = open('shelftemp_logs/'+folder+ "/"+ filename, 'r')
            extract(inFile)
            inFile.close()

def processList():
    sorted_counts = sorted(format_array_count, key = lambda x: (x[0], x[1]))
    output_server = [list(x) for x in set(tuple(x) for x in format_array_server)]

    out_idx = 0

    for i in range(len(sorted_counts)-1):
        if (i == 0):
            output_count.append(sorted_counts[i])
        elif (output_count[out_idx][0] == sorted_counts[i][0] and 
            output_count[out_idx][1] == sorted_counts[i][1]):
            output_count[out_idx][2] += 1
        else:
            out_idx += 1
            output_count.append(sorted_counts[i])

    print output_count
    print output_server

getFiles()
processList()

#print output_server

