import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expectedCon

driverCF = webdriver.Firefox('/usr/local/')
apiRequestLink = "https://codeforces.com/api/contest.list?gym=false"

# At least in my computer, the api request page
# loads differently in different browsers.
# It would be easier for me to fetch data with Chrome



# [This should be the only function that interacts with Codeforces API]
def requestCF ():
	
	# Super important function that queries Codeforces API
	# and returns the contest list in JSON format
	
	global driverCF
	driverCF.get(apiRequestLink)
	
	# waits at most 5 seconds for desired element to load
	WebDriverWait(driverCF, 5).until(
		expectedCon.presence_of_element_located((By.ID, 'rawdata-tab'))
	)
	
	# change the tabs in the page
	dataTabElement = driverCF.find_element_by_id('rawdata-tab')
	dataTabElement.click()
	
	# waits at most 5 seconds for desired element to load
	WebDriverWait(driverCF, 5).until(
		expectedCon.presence_of_element_located((By.CLASS_NAME, 'data'))
	)
	
	return driverCF.find_element_by_class_name('data').text



def CodeforcesFail (CFmessage):
	# [THIS IS UNTESTED] because I wasn't able to get a 'FAILED'
	# Prints API 'FAILED' comment
	return ("[ERRO] Codeforces: " + CFmessage)



def getTime(timeInfo):

	timeInfo *= -1
	
	if timeInfo < 0:
		return
	
	daysToStart = int(timeInfo/(60*60*24))
	timeInfo %= 60*60*24
	
	if daysToStart == 1:
		dayString = str(daysToStart) + " dia, "
	else:
		dayString = str(daysToStart) + " dias, "
	
	
	hoursToStart = int(timeInfo/(60*60))
	timeInfo %= 60*60
	
	if hoursToStart == 1:
		hourString = str(hoursToStart) + " hora, "
	else:
		hourString = str(hoursToStart) + " horas, "
	
	
	minutesToStart = int(timeInfo/60)
	
	if minutesToStart == 1:
		minuteString = str(minutesToStart) + " minuto"
	else:
		minuteString = str(minutesToStart) + " minutos"
	
	fullTimeString = ""
	
	if daysToStart > 0:
		fullTimeString += dayString
	
	if hoursToStart > 0:
		fullTimeString += hourString
	
	if minutesToStart > 0:
		fullTimeString += minuteString
	
	return fullTimeString



def activeContests():

	# Checks for active contests
	# Returns a list:
	
	# If it's first element is "error", comment is the second element
	
	apiReturn = requestCF()
	
	# json.loads() parses the information 
	# into a python dictionary
	CFReturn = json.loads(apiReturn)
	
	currentlyRunning = []
	
	if CFReturn["status"] == "FAILED":
		currentlyRunning.append("error")
		currentlyRunning.append(CodeforcesFail(CFReturn["comment"]))
	
	else :
		
		for contest in CFReturn["result"]:
			
			contestPhase = contest["phase"]
			contestName = contest["name"]
			
			if contestPhase == "CODING":
				currentlyRunning.append(contestName)
			elif contestPhase != "BEFORE":
				break
	
	return currentlyRunning



def upcomingContests():
	
	# Checks most recent 4 upcoming contests
	
	apiReturn = requestCF()
	
	# json.loads() parses the information 
	# into a python dictionary
	CFReturn = json.loads(apiReturn)
	
	upcoming = []
	
	if CFReturn["status"] == "FAILED":
		upcoming.append("error")
		upcoming.append(CodeforcesFail(CFReturn["comment"]))
	
	else :
		
		upcomingListIndex = 0
		
		for contest in CFReturn["result"]:
			
			contestPhase = contest["phase"]
			contestName = contest["name"]
			
			if (contestPhase == "BEFORE") and (len(upcoming) < 4):
				upcoming.append(contestName + " começará em " +
				getTime(contest["relativeTimeSeconds"]))
				
			elif contestPhase == "BEFORE":
				upcoming[upcomingListIndex] = contestName + " começará em " + getTime(contest["relativeTimeSeconds"])
				
				upcomingListIndex += 1
				
				if upcomingListIndex == 4:
					upcomingListIndex = 0
				
			else:
				break
	
	
	return upcoming
