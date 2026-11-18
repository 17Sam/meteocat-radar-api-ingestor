from time import sleep
from datetime import datetime, timezone
from ingestor import *
import json
import os

iterations = 0
interval = 0 # Interval between each call, in seconds

projectPath = os.path.dirname(os.path.abspath(__file__))

with open(f"{projectPath}/vars.json", "r") as file:
    downloadVars = json.load(file)

    iterations = downloadVars["iterations"]
    interval = downloadVars["interval"]

while True:
    date = datetime.now(tz=timezone.utc)
    # Fifteen minutes ago
    targetDate = datetime.fromtimestamp(datetime.timestamp(date) - 900, tz=timezone.utc)

    startMinute = (targetDate.minute // 6) * 6

    success = DownloadImages(iterations, startMinute, targetDate.hour, targetDate.day, targetDate.month, targetDate.year)

    if (success):
        print("\033[31m***\033[0m Latest download starting at", targetDate, "with " + str(iterations) + " iterations \033[31m***\033[0m")
        print("Next call in", interval, "seconds, a.k.a.", interval//3600, "hours and", interval%3600//60, "minutes")

        sleep(interval)
    else:
        print("\033[31m!! Failed\033[0m to download images! Trying again in \033[31m10 minutes\033[0m.")

        sleep(600) # Sleep 10 minutes