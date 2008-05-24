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


def enum_webs(site, fn):
	"""
	Enumerate all webs beneath the site or web specified
	and call te specified function with each web.
	"""
	# do different things based on the type of object provided
	if type(site) is SPWeb:
		enum(site.Webs, fn)
	else:
		site = get_site(site)
		enum(site.RootWeb.Webs, fn)


def enum_all_webs(site, fn):
	"""Enumerate all webs in a site collection"""
	site = get_site(site)
	enum(site.AllWebs, fn)


def enum_lists(web, fn):
	"""Enumerate all lists in the web specified"""
	web = get_web(web)
	enum(web.Lists, fn)



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
	
	site = get_site(url)
	relative_url = url.replace(site.Url, "")
	
	return site.OpenWeb(relative_url)


def get_list(web, list_name):
	"""Gets a list within a web"""
	web = get_web(web)
	return first(web.Lists, lambda l: l.Title == list_name)


def try_get_site(url):
	"""Tries to get a site collection but returns false if no site was found"""
	try:
		site = get_site(url)
		return True, site
	except:
		return False, None


def try_get_web(url):
	"""Tries to get a web but returns false if no web was found"""
	web = get_web(url)
	if web.Exists:
		return True, web
	else:
		return False, None


def try_get_list(web, list_name):
	"""Tries to get a list but returns false if no list was found"""
	l = get_list(web, list_name)
	return l != None, l



# Find Object Helper Methods
# These methods are used to find objects in collections

def list_exists(web, list_name):
	"""Checks if a list exists"""
	web = get_web(web)
	match = first(web.Lists, lambda l: l.Title == list_name)
	return match != None


# List/Collection helper methods

def collect(collection, fn):
	"""Collects items where the function evalueates as true"""
	results = []
	for item in collection:
		if fn(item):
			results << item
	return results


def first(collection, fn):
	"""Finds the first item in the collection where the function evaluates as true"""
	for item in collection:
		if fn(item):
			return item
	return None

