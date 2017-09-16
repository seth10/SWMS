import icalendar
import os
import datetime

class event:
    #dateStart
    #dateEnd
    #type
    #Flexibility Boolean
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
        

if os.path.exists("wfholman@umail.iu.edu.ics"):
    print("Load the string")
    with open('wfholman@umail.iu.edu.ics', 'r') as myfile:
        data=myfile.read()
    the_calendar = icalendar.Calendar().from_ical(data)
    for key in the_calendar:
        print(key)
    print()
    events = data.split("BEGIN:VEVENT")[1::]
    for event in events:
        print(event)
        print()
else:
    print("Prompt the user")
