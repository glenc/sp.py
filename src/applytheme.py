# applytheme.py
"""
Apply Theme
This script will apply the specified theme to all webs in the
specified web application.

Usage:

	ipy applytheme.py --url http://myserver --theme Petal

Arguments:

	--url      - web application url
	--theme    - theme to apply
	[--force]  - apply the theme even if it is already applied
	[--help]   - display this message

"""
#

import sys
import sp
import scriptutil

__all__ = ["apply_theme"]

def main(argv):
	args = scriptutil.getargs(argv, ["url=", "theme="], ["force"], __doc__, True)
	apply_theme(args["url"], args["theme"], args.has_key("force"))


def apply_theme(url, theme, force=False):
	"""Applies the theme to all webs within the web application"""
	
	# always compare to lower case
	theme = theme.lower()
	
	def do_work(web):
		# make sure we're comparing to lower case
		wtheme = web.Theme.lower()
		if (theme == "none" and wtheme != "") or (theme != "none" and wtheme != theme) or force == True:
			print "Applying theme to", web.Url
			web.ApplyTheme(theme)
	
	# iterate over all sites, then all webs
	sp.enum_sites(url, 
		lambda s: 
			sp.enum_all_webs(s, do_work))



if __name__ == '__main__':
	main(sys.argv[1:])

