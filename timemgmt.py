import icalendar
import os
import datetime

class event:
    def __init__(self, dateS, dateE, summary, flexibilityFactor=False):
        self.isFlexible = flexibilityFactor
        self.dateStart = dateS
        self.dateEnd = dateE
        timeTypes = ["sleep", "meal", "exercise", "leisure", "study", "class", "obligation", "gap", "transition", "earlyWakeTime", "lateWake", "earlySleep", "lateSleep"]
        matched = False
        for category in timeTypes:
            if '%'+category+'%' in summary:
                self.timeType = category
                matched = True
                break
        if not matched:
            #Prompt user for category type
            self.timeType = "obligation"
        #Also prompt user for missing necessary categories

    def deconstruct():
        #Need to store auxiliary information so as not to perform lossy transformations
        return "BEGIN:VEVENT\nEND:VEVENT"
        

if os.path.exists("wfholman@umail.iu.edu.ics"):
    print("Load the string")
    with open('wfholman@umail.iu.edu.ics', 'r') as myfile:
        data=myfile.read()
    the_calendar = icalendar.Calendar().from_ical(data)
    for key in the_calendar:
        print(key)
    print()
    events_raw = data.split("BEGIN:VEVENT")[1::]
    events = []
    for event in events_raw:
        for line in event.splitlines():
            if "DTSTART:" in line:
                print(line)
            elif "DTEND:" in line:
                print(line)
        #initialize date objects and compare
else:
    print("Prompt the user; GO MAKE AN ICAL FILE")
