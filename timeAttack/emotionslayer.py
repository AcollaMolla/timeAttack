import urllib2
import string
from requests.exceptions import HTTPError

def toHex(input):
	temp = []
	for item in correctTag:
		temp.append(hex(item)[2:])
	str1 = ''.join(temp)
	print temp
	print str1
	return str1
	
def compareTags(currentTag, correctTag):
	currentString = toHex(currentTag)
	correctString = toHex(correctTag)
	i=0
	for item in correctTag:
		print item
		if item == item in currentTag:
			print "EQUAL :)" 


username = 'alice'
correctTag = [13,7,7,12,4,5,7,0,4,8,15,13,1,4,0,14,2,12,15,8,2,10,3,5,15,2,8,6,12,11,6,5]#32 st
currentTag = [0]*32
#print username.encode('hex').zfill(32)
i=0

#Create the tag here
print currentTag
result = [(item + 1)for item in currentTag]
print result	

compareTags(currentTag, correctTag)

#Try the tag here
try:
	contents = urllib2.urlopen("http://130.243.27.198/auth/1/" + username + "/" + toHex(correctTag)).read()
	print contents
except urllib2.HTTPError as error:
	if error.code == 404:
		print 'We got a 404'
	else:
		print error
 

