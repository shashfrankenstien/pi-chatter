# list online
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print bcolors.OKBLUE + "Warning: No active frommets remain. Continue?" + bcolors.ENDC


# \e[39m
print "\033[38;5;11mHello!"+bcolors.ENDC