import sys
import time
import os

if sys.version_info[0] ==3:
	from urllib.request import urlopen
else:
	from urllib import urlopen

def internetcon():
	try:
		with urlopen("http://www.python.org", timeout =5) as url:
			return True
	except:
		return False
