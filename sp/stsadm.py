# Interface for STSADM.EXE

# references
import clr
clr.AddReference("System")
from System import Environment
from System.IO import Path

# Get Path to stsadm.exe
common_dir = Environment.GetFolderPath(Environment.SpecialFolder.CommonProgramFiles)
STSADMPATH = Path.Combine(common_dir, "Microsoft Shared\\Web Server Extensions\\12\\Bin\\stsadm.exe")