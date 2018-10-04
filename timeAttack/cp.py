import requests
import timeit
from httplib2 import Http

user = 'alice'
url = "http://130.243.27.198/auth/200/" + user + "/02fee9a5642cf73db163a1422fa628fc"

def getUrl():
	user = 'alice'
	return "http://130.243.27.198/auth/200/" + user + "/02fee9a5642cf73db163a1422fa628fc"

for x in range (10):
	print requests.get("http://130.243.27.198/auth/200/alice/02fee9a5642cf73db163a1422fa628fc").elapsed.total_seconds()
user = 'alice'
t = timeit.Timer("requests.get('url')")#0=f
times_p2 = t.repeat(10,1)
print t
print times_p2 #Array with 10 time observations
minValue = min(times_p2)
print minValue
