# This script will set a given property to the same value
# or pattern on all user profiles

import sp
import re
from sp import sharedservices

def main(url, prop, value):
	"""Executes the script"""
	
	# walk over all profiles and call apply_value
	sharedservices.enum_profiles(url, lambda p: apply_value(p, prop, value))


def apply_value(profile, prop, value):
	"""Applies the value to the profile provided"""
	
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
	
	if len(sys.argv) == 1:
		print HELPSTRING
	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3])



HELPSTRING = """
Set Profile Property
This script will set a property on all user profiles based on the pattern provided.

Usage:

	ipy setprofileprop.py http://myserver Picture http://myserver/pics/{Alias}.jpg

Arguments:

	url      - server url
	property - property to set
	value    - value to set the property to

"""