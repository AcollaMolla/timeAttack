NUMBER_OF_TESTS = 3 #How many login attempts to do per bit. 3 seems to work after a lot of testing. >20 is probably to much and will likely trigger rejection from the target server
TIMEOUT = 1
USERNAME = 'alice'
LENGTH_OF_TAG = 32 #Length of the hex tag
BE_VERBOSE = False #To show additional printout

#Dont touch any of below
WARNING = '\033[93m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
OKBLUE = '\033[94m'
ERROR = '\033[41m'
ENDC = '\033[0m'
