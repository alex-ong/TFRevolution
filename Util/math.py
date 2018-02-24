#todo move this copy to Util.
def tryGetInt(x):
    try:
        return (True, int(x))
    except:
        return (False, 0)

def tryGetFloat(x):
    try:
        return (True, float(x))
    except:
        return (False, 0)