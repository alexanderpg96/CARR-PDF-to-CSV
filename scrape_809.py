##################################################################
##################################################################
## Author: Alexander Pearson-Goulart                            ##
## Version: 1.0.1                                               ##
## Date: March 11, 2018                                         ##
## Script to scape data from text files from a converted PDF    ##
## for CARR data analysis. For 809 files                        ##
##################################################################
##################################################################

import csv
import os
import re

# Instantiate variables
facilityName = ""
admin = ""
address = ""
city = ""
state = ""
census = ""
announced = ""
capacity = ""
visitType = ""
metWith = ""
facilityNum = ""
facilityType = ""
phone = ""
zipCode = ""
date = ""
beginT = ""
endT = ""
evalName = ""

fnameCount = 0          # Number of Facility Names collected
fnumCount = 0           # Number of Facility Nums collected
telCount = 0            # Number of Phone Nums collected
dateCount = 0           # Number of dates collected
rowCount = 0            # Number of rows counted
evalCount = 0

dataList = []           # Data sent to the csv file
fileList = []           # List of files in the directory

deficiency_count = 0    # Number of deficiencies counted in file
stopReadType = 0        # Marker to stop reading types
stopReadDesc = 0        # Marker to stop reading descriptions
stop = 0                # Marker to stop all reading
t = ""                  # Temp var for types data
d = ""                  # Temp var for description data
types = []              # Complete type description
descs = []              # Complete descrition data
numTypes = 0            # Number of types for deficiency

poc_count = 0           # Number of plan of corrections
stopPlanDesc = 0        # Marker to stop reading plan descriptions
stop_poc = 0            # Marker to stop plan of corrections reading
p = ""                  # Temp var for plan data
plans = []              # Complete plan description
count = 0               # Number of values in poc
numPlans = 0            # Number of plans counted

################# CHANGE BASED ON MACHINE SCRIPT IS RUN ON ########################
directory_string = "/Users/Alexander/Desktop/CARR/809/files"

for file in os.listdir(directory_string):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"): 
        fileList.append(os.path.join(directory_string, filename))
        continue
    else:
        continue

#### Column Data ####

for file in fileList:
    # Analyze columns
    if file.endswith("t.txt"):  
        with open(file, errors='ignore') as f:
            for line in f:  
                if re.search("FACILITY NAME:",line) and fnameCount == 0 and fnumCount == 0:   
                    before = line.split("NAME:",1)[1]
                    facilityName = before.split("FACILITY")[0].strip()
                    facilityNum = before.split("NUMBER:")[1].strip()
                    fnameCount += 1
                    fnumCount += 1
                elif re.search("ADMINISTRATOR:",line):    
                    before = line.split("ADMINISTRATOR:",1)[1]
                    admin = before.split("FACILITY")[0].strip()
                    facilityType = before.split("TYPE:")[1].strip()
                elif re.search("ADDRESS:",line) and telCount == 0:    
                    before = line.split("ADDRESS:",1)[1]
                    address = before.split("TELEPHONE")[0].strip()
                    phone = before.split("TELEPHONE:")[1].strip()
                    telCount += 1
                elif re.search("CAPACITY:",line) and dateCount == 0:    
                    before = line.split("CAPACITY:",1)[1]
                    capacity = before.split("CENSUS")[0].strip()
                    before = line.split("CENSUS:",1)[1]
                    census = before.split("DATE")[0].strip()
                    date = before.split("DATE:")[1].strip()
                    dateCount += 1
                elif re.search("CITY:",line):   
                    before = line.split("CITY:",1)[1]
                    city = before.split("STATE")[0].strip()
                    before = line.split("STATE:",1)[1]
                    state = before.split("ZIP")[0].strip()
                    zipCode = before.split("CODE:")[1].strip()
                elif re.search("TYPE OF VISIT:",line):   
                    before = line.split("VISIT:",1)[1]
                    visitType = before.split("TIME")[0].strip()
                    beginT = before.split("BEGAN:")[1].strip()
                elif re.search("TIME VISIT BEGAN:",line) and beginT == "":
                    beginT = line.split("BEGAN:",1)[1].strip()
                    visitType = line.split("TIME",1)[0].strip()
                elif re.search("MET WITH:",line):    
                    before = line.split("WITH:",1)[1]
                    metWith = before.split("TIME")[0].strip()
                    endT = before.split("COMPLETED:")[1].strip()
                elif re.search("LICENSING EVALUATOR NAME:",line) and evalCount == 0:  
                    before = line.split("EVALUATOR NAME:",1)[1]
                    evalName = before.split("TELEPHONE")[0].strip()
                    evalCount += 1

        dataList = [evalName, facilityName, facilityNum, phone, address, city, state, zipCode, visitType, metWith, date, beginT, endT]

        facilityName = ""
        admin = ""
        address = ""
        city = ""
        state = ""
        census = ""
        announced = ""
        capacity = ""
        visitType = ""
        metWith = ""
        facilityNum = ""
        facilityType = ""
        phone = ""
        zipCode = ""
        date = ""
        beginT = ""
        endT = ""
        evalName = ""

        fnameCount = 0
        fnumCount = 0
        telCount = 0
        dateCount = 0

    #### Deficiency Data ####
    if file.endswith("t.txt"): 
        continue
    elif file.endswith("tz.txt"): 
        with open(file, errors='ignore') as f:
            for line in f:  
                if re.search("DEFICIENCIES",line) and deficiency_count == 0:    
                    deficiency_count += 1
                elif "DEPARTMENT OF SOCIAL SERVICES COMMUNITY" in line and deficiency_count > 0:
                        stop = 1
                        descs.append(d)
                elif deficiency_count > 0 and stopReadType == 0 and stop == 0:
                    if ")" in line:
                        stopReadType = 1
                        stopReadDesc = 0
                        t += (line.strip()) # end of type
                        types.append(t)
                        numTypes += 1
                        t = ""
                    else:
                        t += (line.strip() + " ")
                elif deficiency_count > 0 and stopReadType > 0 and stopReadDesc == 0 and stop == 0:
                    if not line.strip():
                        continue
                    elif "Type " in line:
                        descs.append(d)
                        d = ""
                        t += (line.strip() + " ") # start of next type
                        stopReadDesc = 1
                        stopReadType = 0
                    else:
                        d += (line.strip() + " ")

        #### Solution Data ####
        with open(file, errors='ignore') as f:
            for line in f:  
                if re.search("PLAN OF CORRECTIONS",line) and poc_count == 0:
                    poc_count += 1
                elif "Failure to correct the cited deficiency(ies)" in line and deficiency_count > 0:
                    stop_poc = 1
                    plans.append(p)
                    numPlans += 1
                elif poc_count > 0 and stopPlanDesc == 0 and stop_poc == 0:
                    if not line.strip():
                        continue
                    else:
                        p += line.strip() + " "
        
        for x in range(0,numTypes):
            dataList.append(types[x])
            dataList.append(descs[x])

        for y in range(0,numPlans-1):
            dataList.append(plans[y])

        with open("data_809.csv", "a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')

            if rowCount == 0:
                header = ["Licensing Evaluator Name", "Facility Name", "Facility Number", "Phone Number", "Address", "City", "State", "Zip Code", "Visit Type", "Met With", "Date", "Time Began", "Time Ended"]
                writer.writerow(header)
                rowCount += 1
            writer.writerow(dataList)

        deficiency_count = 0
        stopReadType = 0
        stopReadDesc = 0
        stop = 0
        t = ""
        d = ""
        types = []
        descs = []
        numTypes = 0

        poc_count = 0
        stopPlanDesc = 0
        stop_poc = 0
        p = ""
        plans = []
        count = 0
        dataList = []
