from pathlib import Path
import os.path
import pandas as pd


def getOpenSkyData(folderpath, logpath, conditionalfunction):
    file_Paths = [x for x in Path(folderpath).glob("flightlist_*.csv.gz") if not conditionalfunction(logpath,os.path.basename(x))]
    flightdict = {}
    if len(file_Paths) > 0:
        for f in file_Paths:
            flightdict[os.path.basename(f)] = pd.read_csv(f, parse_dates=["firstseen", "lastseen", "day"])
        return flightdict
    else:
        return flightdict