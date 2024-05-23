from ManifestDecryptor import doDecrypt
from MaskedHeaderStream import unObfuscate, rename
from AssetsDownloader import downloadAll
from eDiffMode import DiffMode
from eWorkingMode import WorkingMode

# Configurations
# Diff, All
diffMode = DiffMode.All
# Local, Remote
workingMode = WorkingMode.Local
# Adjust this param according to your PC's spec
maxDownloadThread = 20

jDict = doDecrypt(diffMode)
if workingMode == WorkingMode.Remote:
    downloadAll(jDict, maxDownloadThread)
unObfuscate(jDict)
rename(jDict)