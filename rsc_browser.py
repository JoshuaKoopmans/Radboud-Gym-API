import mechanize
import getpass
import time
import re
import os

howmany = 22 # how many options you want to see

# URLs needed
login         = "https://publiek.usc.ru.nl/publiek/login.php"
aanbod        = "https://publiek.usc.ru.nl/publiek/laanbod.php"
inschrijfpage = "https://publiek.usc.ru.nl/publiek/"
fitness       = "pack=a%3A5%3A%7Bs%3A6%3A%22n.naam%22%3Bs%3A7%3A%22Fitness%22%3Bs%3A12%3A%22jlap.pool_id%22%3Bs%3A2%3A%2213%22%3Bs%3A10%3A%22jlap.intro%22%3Bs%3A0%3A%22%22%3Bs%3A16%3A%22jlap.betaalwijze%22%3Bs%3A6%3A%22gratis%22%3Bs%3A10%3A%22jlap.prijs%22%3Bs%3A4%3A%220.00%22%3B%7D"

# Fancy colors for print statements
class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def createNewBrowser():
	# Create browser
	browser = mechanize.Browser()
	# Makes site know I am not a robot ;)
	browser.set_handle_robots(False) 
	return browser

def getLoginData():
	while True:
		try:
			username = str(input("Enter Username: "))
			password = getpass.getpass("Enter Password: ")
			sleeptime = int(input("Seconds between requests: "))
			if len(username) == 0 or len(password) == 0:
				raise Exception
			return username, password, sleeptime
		except:
			print('You typed something wrong :(')

# Login to RSC
def loginSite(browser, username, password):
	# Open the login page
	browser.open(login)
	# Select the form to fill
	browser.select_form( 'entryform' )
	# Fill the form and login
	browser.form['username'] = username
	browser.form['password'] = password
	browser.submit() 
	return browser

def retrieveRawFitnessData(browser):
	# Open site, select fitness and retrieve the html code
	browser.open(aanbod)
	browser.select_form(nr=0)
	browser.form.find_control(name="PRESET[Laanbod][where_naam_ibp][]").value = [fitness]
	browser.submit()
	html = browser.response().read().decode("utf-8")
	return html

# Retrieve all dates and times from the fitness page
def parsFitnessHtml(html):
	# Extract only the relevant part
	html = html.split('<tr valign=top class=')[1:-1]
	html = [i for i in html if 'Pop-up' not in i]
	choiceList = []
	# Go over all options and retrieve the link, date, time and location
	for line in html:
		link = re.findall('href=\".+\"', line)[0][6:-1]
		date = re.findall('\<td\>.+2020 ', line)[0][4:]
		tim3 = re.findall('\<td\>[0,1,2].+ ', line)[0][4:15]
		locn = re.findall('Fitness.+\</', line)[0][:-2]
		date_and_time = date[3:] + tim3 + date[:3]
		choiceList += [[date_and_time, locn, link]]
	# Sort by date and time
	choiceList.sort() 
	choiceList = [[i[0][-3:]+i[0][:-3], i[1],i[2]]for i in choiceList]
	return choiceList

# Print all fitness options and let user choose one.
# Return the link to the corresponding page
def chooseFitnessOption(browser, choiceList):
	while 1:
		try:
			for ind, sub in enumerate(choiceList[:howmany]):
				print(f"{bcolors.UNDERLINE}{sub[1]}{bcolors.ENDC}")
				print(f"{bcolors.WARNING}{sub[0]}{bcolors.ENDC}")
				print(f"{bcolors.BOLD}\n To subscribe use number: {str(ind)}{bcolors.ENDC}")
				print("\n"+"_-"*18+"\n")
			choice = input(':')
			choice = int(choice)
			link = choiceList[choice][2]
			return inschrijfpage+link
		except:
			print('Please provide a correct number')

# save the current browser-webpage
def savePage(browse, counter, name='sport.html'):
	write = open(name, 'w')
	html  = browser.response().read().decode("utf-8")
	write.write(html + str(counter))
	write.close()

# Press all buttons if position is free, otherwise error
def pressButtons(browser):
	link = [link for link in browser.links() if "Toevoegen aan Keuzelijst" in link.text][0]
	browser.click_link(link)
	browser.follow_link(link)
	browser.open("https://publiek.usc.ru.nl/publiek/bevestigen.php")
	browser.select_form(nr=0)
	browser.submit()

# Get new Ip adres if needed
def getNewIpAdres(waitXseconds=8):
	os.system('nordvpn c')
	time.sleep(waitXseconds)

if __name__ == "__main__":
	browser = createNewBrowser()
	username, password, sleeptime = getLoginData()
	browser = loginSite(browser, username, password)
	rawhtml = retrieveRawFitnessData(browser)
	choiceList = parsFitnessHtml(rawhtml)
	link = chooseFitnessOption(browser, choiceList)
	browser.open(link)
	counter = 0
	savePerMinute = int(60/sleeptime)
	# Send requests untill done 
	#TODO not tested if not success
	#TODO check if been send back to inlog page
	#TODO check if IP is blocked -> use nordvpn, go to login page, login again, go back to the link
	while True:
		try:
			pressButtons(browser)
			break
		except:
			time.sleep(sleeptime)
			browser.reload()
			if counter % savePerMinute == 0:
				savePage(browser, counter)
			counter += 1
	print(f"{bcolors.UNDERLINE}{bcolors.OKGREEN}Success!\n{bcolors.ENDC}")
	print('It took %i requests!' % counter)


