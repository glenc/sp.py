# Script for working with SSP stuff

# Set up references
import clr
import utils
clr.AddReference("Microsoft.Office.Server")
from Microsoft.Office.Server import ServerContext
from Microsoft.Office.Server.UserProfiles import UserProfileManager


# People and Profiles
def _get_profile_manager(site):
	"""Gets a new UserProfileManager"""
	site = utils.get_site(site)
	context = ServerContext.GetContext(site)
	return UserProfileManager(context)


def enum_profiles(site, fn):
	"""Enumerate all user profiles"""
	manager = _get_profile_manager(site)
	enumerator = manager.GetEnumerator()
	while enumerator.MoveNext():
		fn(enumerator.Current)

