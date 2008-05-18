# This script will backup all site collections in a web
# application.

import sp
from sp import stsadm

FILE_EXTENSION = ".bak"

def backup_sites(url, destination):
	"""Execute the script"""
	webapp = sp.get_webapplication(url)
	
	# make sure destination has a trailing slash
	if destination[-1] != "\\":
		destination = destination + "\\"
	
	def do_backup(site):
		backup_site(site, destination + _get_backup_filename(site.Url) + FILE_EXTENSION)
	
	sp.enum_sites(webapp, do_backup)


def _get_backup_filename(url):
	url = url.replace("http://", "")
	url = url.replace("https://", "")
	url = url.replace("/", "_")
	url = url.replace(":", ".")
	return url


def backup_site(site, filename):
	"""Back up a site collection to the specified location"""
	site = sp.get_site(site)
	
	print "Backing up site ", site.Url
	stsadm.run("backup", url=site.Url, filename=filename, overwrite=True)



if __name__ == '__main__':
	import sys
	
	if len(sys.argv) == 1:
		print HELPSTRING
	else:
		backup_sites(sys.argv[1], sys.argv[2])



HELPSTRING = """
Backup Sites
This script will backup all site collections in the specified web application.

Usage:

	ipy backupsites.py http://myserver \\network\share

Arguments:

	url         - web application url
	destination - location backups will be saved to

"""