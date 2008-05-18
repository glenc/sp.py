# Set up References
import clr
clr.AddReference("System")
clr.AddReference("Microsoft.SharePoint")
from System import Uri
from Microsoft.SharePoint import *
from Microsoft.SharePoint.Administration import SPWebApplication


# Enumeration
# These are simple enumeration methods for walking over various SharePoint
# objects and collections.

def enum(col, fn):
	"""Enumerate a collection and call function fn for each item."""
	for x in col:
		fn(x)


def enum_sites(webapp, fn):
	"""
	Enumerate all site collections in the specified web application
	and call the specified function with each site collection.
	"""
	# just in case we were passed a URL, get the web app
	webapp = get_webapplication(webapp)
	enum(webapp.Sites, fn)



# Get Object Helper Methods
# These methods take in some sort of object identifier (usually a URL)
# and return the appropriate object instance

def get_webapplication(url):
	"""Gets a web application by its URL"""
	if type(url) is SPWebApplication:
		return url
	
	return SPWebApplication.Lookup(Uri(url))


def get_site(url):
	"""Gets a site collection by its URL"""
	if type(url) is SPSite:
		return url
	
	return SPSite(url)


def get_web(url):
	"""Gets a web by its URL"""
	if type(url) is SPWeb:
		return url
	
	if type(url) is SPSite:
		return url.RootWeb
	
	return SPSite(url).OpenWeb(url)


