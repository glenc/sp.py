import sys
import getopt

__all__ = ["ArgsError", "getargs", "showhelp"]

class ArgsError(Exception):
	arg = ''
	msg = ''

	def __init__(self, msg, arg=''):
		self.msg = msg
		self.arg = arg
		Exception.__init__(self, msg, arg)

	def __str__(self):
		return self.msg


def getargs(argv, required, optional=[], helptext="", show_help_on_error=False):
	"""Gets command line arguments and returns a dict"""
	
	# get arguments using getopt
	try:
		full_args = required + optional
		if not "help" in full_args:
			full_args += ["help"]
		opts, args = getopt.getopt(argv, "", full_args)
	except getopt.GetoptError:
		if show_help_on_error:
			showhelp(helptext)
		else:
			raise
	
	# parse provided values into dict
	args = dict()
	for o,a in opts:
		if o == "--help":
			showhelp(helptext)
		key = o.lstrip('-')
		args[key] = a
	
	# check that all required args were provided
	for arg in required:
		if not args.has_key(arg.rstrip('=')):
			if show_help_on_error:
				showhelp(helptext)
			else:
				raise ArgsError("Required argument was not provided", arg)
	
	return args


def showhelp(msg):
	print msg
	sys.exit()

