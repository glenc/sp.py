# setprofileprop.py
"""
Set Profile Property
This script will set a property on all user profiles based on the pattern provided.

Usage:

	ipy setprofileprop.py --url http://myserver --prop Picture 
	                      --value http://myserver/pics/{Alias}.jpg

Arguments:

	url      - server url
	prop     - property to set
	value    - value to set the property to
	[--help] - show this help

"""

import sp
import re
from sp import sharedservices

__all__ = ["set_profile_prop"]

def main(argv):
	from scriptutil import getopt
	try:
		opts, args = getopt.getopt(argv, "u:p:v:?", ["url=", "prop=", "value=", "help"])
	except getopt.GetoptError:
		showhelp()
	
	# defaults
	url = ""
	prop = ""
	value = ""
	
	for o,a in opts:
		if o in ("-u", "--url"):
			url = a
		elif o in ("-p", "--prop"):
			prop = a
		elif o in ("-v", "--value"):
			value = a
		elif o in ("-?", "--help"):
			showhelp()
	
	if url == "" or prop == "":
		showhelp()
	
	set_profile_prop(url, prop, value)


def showhelp():
	print __doc__
	sys.exit()


def set_profile_prop(url, prop, value):
	"""Executes the script"""
	
	# walk over all profiles and call apply_value
	sharedservices.enum_profiles(url, lambda p: _apply_value(p, prop, value))


def _apply_value(profile, prop, value):
	"""Applies the value to the profile provided"""
	
	print "Processing", profile["AccountName"]
	
	# take the value, locate any {key} patterns, then
	# replace each with the property from the profile
	regex = re.compile("{(.*?)}")
	for match in regex.finditer(value):
		key = match.group(1)
		
		# handle special case where 'Alias' maps to 'AccountName'
		trim = False
		if key == "Alias":
			key = "AccountName"
			trim = True
		
		val = profile[key].Value
		
		if trim == True:
			val = val.split("\\")[1]	
		
		value = value.replace(match.group(0), val)
		
	# how apply updated value to the profile property
	profile[prop].Value = value
	profile.Commit()



if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
