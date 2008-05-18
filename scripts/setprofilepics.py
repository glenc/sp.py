# This script will set everyone's profile picture
# based on a given pattern

import sp
import re
from sp import sharedservices

def main(url, pattern):
	"""Executes the script"""
	
	# walk over all profiles and call apply_pattern
	sharedservices.enum_profiles(url, lambda p: apply_pattern(p, pattern))


def apply_pattern(profile, pattern):
	"""Applies the pattern to the profile provided"""
	
	# take the {pattern}, locate any {key} patterns, then
	# replace each with the property from the profile
	
	regex = re.compile("{(.*?)}")
	for match in regex.finditer(pattern):
		key = match.group(1)
		val = profile[key].Value
		pattern = pattern.replace(match.group(0), val)
		
	print(pattern)
	



if __name__ == '__main__':
	import sys
	
	if len(sys.argv) == 1:
		print HELPSTRING
	else:
		main(sys.argv[1], sys.argv[2])


HELPSTRING = """Set Profile Pics
This script will set all user's profile picture based on the pattern provided.

Usage:

	ipy setprofilepics.py http://myserver http://myserver/pics/{account_name}.jpg

Arguments:

	url     - server url
	pattern - pattern to use when setting the picture profile property

"""