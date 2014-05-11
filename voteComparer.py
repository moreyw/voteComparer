import json, datetime
from urllib import urlopen
from sys import stdout

apiRoot = "https://congress.api.sunlightfoundation.com/"
apiKey = ""  #ENTER YOUR API KEY HERE (http://sunlightfoundation.com/api/accounts/register/)
fullKey = "apikey=" + apiKey

if(apiKey==""):
	print "Need to enter an API Key. (Line 6)"
	exit()


#takes congressman's ID, FirstName, LastName
class congressman: 

	def __init__(self, idNumber, firstName, lastName, state, party, title):
		self.idNumber = idNumber  
		self.lastName = lastName
		self.firstName = firstName
		self.state = state
		self.party = party
		self.title = title

	def getID(self):
		return self.idNumber

	def getLastName(self):
		return self.lastName

	def getFirstName(self):
		return self.firstName

	def getParty(self):
		return self.getParty

	def __str__(self):
		stringy = self.title + " " + self.firstName + " " + self.lastName + " (" + self.state + "-" + self.party+ ")"
		return stringy

def legislatorSearch(searchCriteria):
	page = urlopen(apiRoot + "legislators?query=" + searchCriteria + "&per_page=50&all_legislators=true&" + fullKey)
	#results = page.read()
	data = json.load(page)
	results = []
	for each in data['results']:
		results.append(congressman(each['bioguide_id'],each['first_name'],each['last_name'],each['state_name'],each['party'],each['title']))
	for each in results:
		if(raw_input("Did you mean: " + str(each) + "? (Y/N)").lower() == "y"):
			return each
	if(raw_input("Sorry, couldn't find the congressman you meant, would you like to try again?").lower() == "n"):
		exit()
	return legislatorSearch(raw_input("Which congressman would you like to search for? "))

def getVotes(memberAID, memberBID):
	f = open(outputFile,'w')
	f.write("Roll Call #, Question, Vote, Date, Time\n")
	f.close()
	options = "votes?voter_ids." + memberAID + "__exists=true&voter_ids." + memberBID + "__exists=true&per_page=50&fields=voter_ids,number,voted_at,question&"
	k = 0
	url = "https://congress.api.sunlightfoundation.com/" + options + "apikey=" + apiKey
	#print url
	page = urlopen(url)
	data = json.load(page)
	page.close()
	f = open(outputFile,'a')
	print "-----Comparing Votes------"
	for each in data['results']:
		voteA = each['voter_ids'][memberAID]
		voteB = each['voter_ids'][memberBID]
		if((voteA==voteB) and (voteA != "Not Voting")):
			myDate = datetime.datetime.strptime(each['voted_at'], "%Y-%m-%dT%H:%M:%SZ")#, '"%b %d, %Y", %I:%M:%S %p %Z')
			tempDate = str(myDate).split(' ')
			dateTime = tempDate[0] + ', ' + tempDate[1]
			stringy = str(each['number']) + ',"' + each['question'] + '",' + voteA + "," + dateTime + "\n"
			f.write(stringy)
			k+=1
	if(data['count'] > 50):
		pages = int(int(data['count']) / 50) + 1
		i = 2
		while(i<=pages):
			stdout.write('.')
			stdout.flush()
			page = urlopen(url + "&page=" + str(i))
			data = json.load(page)
			page.close()
			for each in data['results']:
				voteA = each['voter_ids'][memberAID]
				voteB = each['voter_ids'][memberBID]
				if((voteA==voteB) and (voteA != "Not Voting")):
					myDate = datetime.datetime.strptime(each['voted_at'], "%Y-%m-%dT%H:%M:%SZ")#, '"%b %d, %Y", %I:%M:%S %p %Z')
					tempDate = str(myDate).split(' ')
					dateTime = tempDate[0] + ', ' + tempDate[1]
					stringy = str(each['number']) + ',"' + each['question'] + '",' + voteA + "," + dateTime + "\n"
					f.write(stringy)
					k+=1
			i+= 1
	f.close()
	print "\n----- Finished ------"
	return k

memberA = legislatorSearch(raw_input("Which congressman would you like to search for? "))
memberB = legislatorSearch(raw_input("Which congressman would you like to search for? "))

outputFile = memberA.getLastName() + "_" + memberB.getLastName() + "_Comparison.csv"
votes = getVotes(memberA.getID(), memberB.getID()) 

print str(memberA) + " and " + str(memberB) + " voted together " + str(votes) + " times."
