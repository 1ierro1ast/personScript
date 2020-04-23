import os
import re
import sys
import json
import shutil
import random
import requests
from bs4 import BeautifulSoup

pattern = {
			"social":{
				"name":"",
				"surname":"",
				"password":""
			},
			"basics":{
				"gender":"",
				"type":"",
				"nationality":"",
				"location":"",
				"language":""
			},
			"life":{
				"age":0,
				"birth_date":"",
			},
			"physical":{
				"height":"",
				"weight":"",
				"handedness":"",
				"blood_type":""
			},
			"future_outlook":{
				"death_date":"",
				"lifespan":0,
				"cause_of_death":""
			}
		}

def randomGen(lenght = 12, sChar = True):
	alp = "qwertyuiopasdfghjklzxcvbnm"
	specChar = "!@#$%^&/_=+-"
	rText = ""
	while len(rText) <= lenght:
		typeChar = random.randint(0,2)
		if typeChar == 0:
			k = random.randint(0,len(alp)-1)
			if random.randint(0,1) == 1:
				rText+=alp[k:k+1].upper()
			else:
				rText+=alp[k:k+1]
		elif typeChar == 1:
			rText+=str(random.randint(0,9))
		elif typeChar == 2 and sChar:
			k = random.randint(0,len(specChar)-1)
			rText+=specChar[k:k+1]
	return str(rText)


def createPersons():
	url = "https://www.behindthename.com/random/random.php?number=1&sets=1gender=f&surname=&randomsurname=yes&showextra=yes&norare=yes&nodiminutives=yes&usage_chi=1&usage_fre=1&usage_jap=1&usage_kaz=1&usage_pol=1&usage_ukr=1&usage_rus=1"
	page = requests.get(url)
	soup = BeautifulSoup(page.text,"html.parser")
	persons = soup.findAll("center")[0].text.replace(" ","_")

	personNames = soup.findAll("span", class_="random-result")
	name,surname = personNames[0].text.split(" ")[0],personNames[0].text.split(" ")[1]
	basics = re.search(r"Basics\s(\S*:\S*\s){5}",persons).group(0).replace("Basics","").replace(",_",",")
	life = re.search(r"Life_&_Times\s(\S*:\S*\s){2}",persons).group(0).replace("Life_&_Times","").replace(",_",",")
	physical = re.search(r"Physical\s(\S*:\S*\s){4}",persons).group(0).replace("Physical","").replace("_/_","/")
	future_outlook = re.search(r"Future_Outlook\s(\S*:\S*\s){3}",persons).group(0).replace("Future_Outlook","").replace(",_",",")

	pattern["social"]["name"] = name.replace("\n","")
	pattern["social"]["surname"] = surname.replace("\n","")
	pattern["social"]["password"] = randomGen(16)

	pattern["basics"]["gender"] = basics.split("\n")[1].split(":")[1]
	pattern["basics"]["type"] = basics.split("\n")[2].split(":")[1]
	pattern["basics"]["nationality"] = basics.split("\n")[3].split(":")[1]
	pattern["basics"]["location"] = basics.split("\n")[4].split(":")[1]
	pattern["basics"]["language"] = basics.split("\n")[5].split(":")[1]

	pattern["life"]["age"] = life.split("\n")[1].split(":")[1]
	pattern["life"]["birth_date"] = life.split("\n")[2].split(":")[1]

	pattern["physical"]["height"] = physical.split("\n")[1].split(":")[1]
	pattern["physical"]["weight"] = physical.split("\n")[2].split(":")[1]
	pattern["physical"]["handedness"] = physical.split("\n")[3].split(":")[1]
	pattern["physical"]["blood_type"] = physical.split("\n")[4].split(":")[1]

	pattern["future_outlook"]["death_date"] = future_outlook.split("\n")[1].split(":")[1]
	pattern["future_outlook"]["lifespan"] = future_outlook.split("\n")[2].split(":")[1]
	pattern["future_outlook"]["cause_of_death"] = future_outlook.split("\n")[3].split(":")[1]

	return pattern

def saveToExt(pattern):
	if os.path.exists("persons"):
		dirname = "%s_%s" % (pattern["social"]["name"],pattern["social"]["surname"])
		os.makedirs("persons/%s" % dirname)
	else:
		os.makedirs("persons")
		dirname = "%s_%s" % (pattern["social"]["name"],pattern["social"]["surname"])
		os.makedirs("persons/%s" % dirname)
	with open("persons/"+dirname+"/"+dirname+".json","w",encoding = "UTF-8") as dataFile:
		json.dump(pattern, dataFile, ensure_ascii = False, indent = 6)

	return "persons/%s/%s.json" % (dirname, dirname)

def saveDB(db):
	with open("db.json","w",encoding = "UTF-8") as dataFile:
		json.dump(db, dataFile, ensure_ascii = False, indent = 6)

def readDB(db = "db.json"):
	with open(db,"r",encoding = "UTF-8") as dataFile:
		return json.load(dataFile)


def main():
	dbPersons = readDB()
	dbPersonsTemp = {"persons":[]}
	while True:
		menu = input("| 1. Create persons\n| 2. List created persons(indev)\n|>> ")
		if menu == "1":
			countPersons = int(input("Enter count persons: "))
			for i in range(countPersons):
				p = createPersons()
				path = saveToExt(p)
				dbPersons["pathToPersons"].append(path)
			saveDB(dbPersons)
		elif menu == "2":
			dbPersons = readDB()
			for i in dbPersons["pathToPersons"]:
				with open(i, "r", encoding = "UTF-8") as dataFile:
					dbPersonsTemp["persons"].append(json.load(dataFile))
			for i in dbPersonsTemp["persons"]:
				print("| Name: %s\n| Surname: %s\n| Password: %s\n| Age: %s\n========\n"%(i["social"]["name"],i["social"]["surname"],i["social"]["password"],i["life"]["age"]))
			
if __name__ == "__main__":
	sys.exit(main())
