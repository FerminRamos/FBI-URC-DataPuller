# TODO: This program utilizes the FBI's API to pull data
#  API Documentation: https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi
import csv
import requests
import json
import time


# Given a JSON object -> prints w/ JSON formatting to console. Useful for seeing raw data.
def printJSON(r):
    print(json.dumps(r, indent=2))


#
# START AGENCY DATA
#

# Gets ALL departments in the United States + writes to CSV file
def getAllDepartments():
    states = ["AK", "AL", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
              "PR"]

    dataset = []
    for state in states:
        for agency in getAgencies(state):
            ori = agency['ori']
            agencyName = agency['agency_name']
            stateName = agency['state_name']
            divisionName = agency['division_name']
            regionName = agency['region_name']
            regionDesc = agency['region_desc']
            countyName = agency['county_name']
            agencyTypeName = agency['agency_type_name']
            nibrs = agency['nibrs']
            nibrsStartDate = agency['nibrs_start_date']
            latitude = agency['latitude']
            longitude = agency['longitude']

            print(">> (" + countyName + ", " + stateName + ") " + agencyName + ", " + ori)
            dataset.append([stateName, countyName, agencyName, ori, divisionName, regionName,
                            regionDesc, agencyTypeName, nibrs, nibrsStartDate,
                            latitude, longitude])

    with open("List of ALL U.S. Agencies.csv", "w", newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        dataset.insert(0, ["State", "County", "Agency Name", "Ori" , "Division Name", "Region Name",
                           "Region Description", "Agency Type Name", "NIBRS", "NIBRS Start Date",
                           "Latitude", "Longitude"])
        csvWriter.writerows(dataset)

    return None


# Gets list of agencies within a state, given a state Abbr.
def getAgencies(stateAbbr):
    r = requests.get(BASE_URL + "agency/byStateAbbr/" + stateAbbr + "?API_KEY=" + API_KEY).json()
    return r


#
# End Agencies Data
#


#
# START SUMMARIZED DATA
#

# Opens "List of ALL U.S. Agencies.csv" and calls "getAgencySummary()" to get total count of offenses for
#  EVERY department on file, for any given time period.
def getSummarizedData(startYear, endYear):
    dataset = []

    # Calls getAgencySummary() for every Agency in our file
    with open("My Agencies.csv", "r") as csvFile:  # TODO: Make sure this file contains YOUR departments that you want data for
        csvReader = csv.reader(csvFile)
        csvFile.readline()  # Pop Headers
        for line in csvReader:
            dataset.append([line[0], line[1], line[2], line[3]] + getAgencySummary(line[3], startYear, endYear) + [line[10], line[11]])
            time.sleep(5)  # Prevents us from being rate-limited

    # Creates Custom Headers
    headers = ["State", "County", "Agency", "Ori"]
    for offense in getListOfOffenses():
        headers.append("total " + offense + " crimes (" + str(startYear) + "-" + str(endYear) + ")")
        headers.append("total " + offense + " cleared crimes (" + str(startYear) + "-" + str(endYear) + ")")
        headers.append("total " + offense + " actual crimes (" + str(startYear) + "-" + str(endYear) + ")")

    headers += ["Latitude", "Longitude"]
    dataset.insert(0, headers)

    with open("List of Crimes per Agency.csv", "w", newline='') as csvFile:  # TODO: It'll output data to this location
        csvWriter = csv.writer(csvFile)
        csvWriter.writerows(dataset)

    return None


# List of offenses applicable for "Summary Data"
def getListOfOffenses():
    listOfOffenses = ["aggravated-assault",
                      "violent-crime",
                      "arson",
                      "human-trafficing",
                      "rape-legacy",
                      "homicide",
                      "burglary",
                      "motor-vehicle-theft",
                      "larceny",
                      "rape",
                      "property-crime"]
    return listOfOffenses


# Gets called by getSummarizedData() function.
#  gets total count of offenses for a specific department (ORI) & specific crime (OFFENSE) & range of years.
def getAgencySummary(ori, startYear, endYear):
    dataset = []
    for crime in getListOfOffenses():
        r = requests.get(BASE_URL + "summarized/agency/" + ori + "/" + crime + "?from=" + str(startYear) + "&to=" + str(endYear) + "&API_KEY=" + API_KEY).json()

        total = 0
        totalCleared = 0
        totalActual = 0
        rapeExclusiveCount = False  # Used to separate rape w/ rape-legacy when data is scrambled together
        subset = []
        for yearlyData in r:
            if yearlyData['offense'] != "rape" and not rapeExclusiveCount:
                cleared = yearlyData['cleared']
                actual = yearlyData['actual']

                totalCleared += int(cleared)
                totalActual += int(actual)
                total = totalCleared + totalActual

                subset += [total, totalCleared, totalActual]

                print(yearlyData)
            elif yearlyData['offense'] == "rape":  # Handles scrambled data when offense = "Rape"
                rapeExclusiveCount = True  # Reserves vars to only count rape offenses in next iteration
                cleared = yearlyData['cleared']
                actual = yearlyData['actual']

                totalCleared += int(cleared)
                totalActual += int(actual)
                total = totalCleared + totalActual

                subset += [total, totalCleared, totalActual]
                print("***" + str(yearlyData))

        rapeExclusiveCount = False
        dataset += [total, totalCleared, totalActual]
        print([total, totalCleared, totalActual])
        print("\n")

    return dataset

#
# End Summarized Data
#


# TODO: This is main. Run EITHER one of these two methods:
#  1. "getAllDepartments()" - To get list of ALL Law Enforcement Departments in the U.S.
#  2. "getSummarizedData()" - To get statistics on all offenses documented per each department. If you only want data
#                             for 1 department, just run it w/ 1 department in the CSV file (including headers ofc)
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.usa.gov/crime/fbi/cde/"

# getAllDepartments()
getSummarizedData(startYear=2015, endYear=2023)
