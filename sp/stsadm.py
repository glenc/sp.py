# Interface for STSADM.EXE
#
# Allows users to execute STSADM operations by calling the
# run method.  The run method takes an operation argument
# and a list of name-value pairs for the operation arguments
#

# import references
import clr
clr.AddReference("System")
from System import Environment
from System.IO import Path
from System.Diagnostics import Process


# Get Path to stsadm.exe
common_dir = Environment.GetFolderPath(Environment.SpecialFolder.CommonProgramFiles)
STSADMPATH = Path.Combine(common_dir, "Microsoft Shared\\Web Server Extensions\\12\\Bin\\stsadm.exe")


def run(operation, **args):
	"""Execute a STSADM operation"""
	argstring = "-o " + operation
	argstring += " " + _format_args(args)
	_execute_command(argstring)


def _format_args(**args):
	"""Formats a series of arguments as an STSADM argument string"""
	argstring = ""
	for kw in args.keys():
		if type(args[kw]) is bool:
			argstring += "-" + kw
		else:
			argstring += "-" + kw + " \"" + args[kw] + "\""
		argstring += " "
		
	return argstring


def _execute_command(argstring, workingDir=None):
	"""Executs an STSADM command"""
	proc = Process()
	
	proc.StartInfo.UseShellExecute = False
	proc.StartInfo.FileName = "\"" + STSADMPATH + "\""
	proc.StartInfo.Arguments = argstring
	
	if workingdir != None:
		proc.StartInfo.WorkingDirectory = workingdir
	
	proc.Start()
	proc.WaitForExit()
