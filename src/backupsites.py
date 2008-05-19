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

import sp
from sp import stsadm
import scriptutil
import sys

__all__ = ["backup_sites", "backup_site"]

# file extension for backup files
FILE_EXTENSION = ".bak"


def main(argv):
	args = scriptutil.getargs(argv, ["url=", "destination="], ["overwrite"], __doc__, True)
	backup_sites(args["url"], args["destination"], args.has_key("overwrite"))


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
	
	print "Backing up site", site.Url
	stsadm.run("backup", url=site.Url, filename=filename, overwrite=overwrite)



if __name__ == '__main__':
	main(sys.argv[1:])

