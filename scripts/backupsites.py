# backupsites.py
"""
Backup Sites
This script will backup all site collections in the specified web application.

Usage:

	ipy backupsites.py --url http://myserver --destination \\\\network\share

Arguments:

	--url         - web application url
	--destination - location backups will be saved to
	[--overwrite] - if passed, backups will be overwriten if they exist
	[--help]      - shows this help

"""

import getopt
import sp
from sp import stsadm

__all__ = ["backup_sites", "backup_site"]

# file extension for backup files
FILE_EXTENSION = ".bak"


def main(argv):
	try:
		opts, args = getopt.getopt(argv, "u:d:o?", ["url=", "destination=", "overwrite", "help"])
	except getopt.GetoptError:
		showhelp()
	
	# defaults
	overwrite = False
	url = ""
	destination = ""
	
	for o,a in opts:
		if o in ("-u", "--url"):
			url = a
		elif o in ("-d", "--destination"):
			destination = a
		elif o in ("-o", "--overwrite"):
			overwrite = True
		elif o in ("-?", "--help"):
			showhelp()
	
	if url == "" or destination == "":
		showhelp()
	
	backup_sites(url, destination, overwrite)


def showhelp():
	print __doc__
	sys.exit()


def backup_sites(url, destination, overwrite=True):
	"""Execute the script"""
	webapp = sp.get_webapplication(url)
	
	# make sure destination has a trailing slash
	if destination[-1] != "\\":
		destination = destination + "\\"
	
	def do_backup(site):
		backup_site(site, destination + _get_backup_filename(site.Url) + FILE_EXTENSION, overwrite)
	
	sp.enum_sites(webapp, do_backup)


def _get_backup_filename(url):
	url = url.replace("http://", "")
	url = url.replace("https://", "")
	url = url.replace("/", "_")
	url = url.replace(":", ".")
	return url


def backup_site(site, filename, overwrite=True):
	"""Back up a site collection to the specified location"""
	site = sp.get_site(site)
	
	print "Backing up site ", site.Url
	stsadm.run("backup", url=site.Url, filename=filename, overwrite=overwrite)



if __name__ == '__main__':
	import sys
	main(sys.argv[1:])

