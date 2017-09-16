import icalendar
import os
import datetime
import string


class eventobj:
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
            process = False
            if "DTSTART:" in line:
                process = True
                print(line)
                line = str(line.split("DTSTART:")[1][:15:])
                #line2 = ''.join(c for c in line if c not in string.ascii_letters)
                #print(line2)
                #print(line[1][13::15])
                print(line)
                #date_start = datetime.datetime(int(str(line[0::4])), int(str(line[4::6])), int(str(line[6::8])), int(str(line[9::11])), int(str(line[11::13])), int(str(line[13::15])))
                date_start = datetime.datetime.strptime(line, "%Y%m%dT%H%M%S")
                print(date_start)    
            elif "DTEND:" in line:
                print(line)
                line = str(line.split("DTEND:")[1][:15:])
                date_end = datetime.datetime.strptime(line, "%Y%m%dT%H%M%S")
                print(date_end)
            elif "SUMMARY:" in line:
                summary = line.split("SUMMARY:")[1]
        if not process:
            continue
        now = datetime.datetime.today()#Add one day for tomorrow? TODO
        if (now.year == date_end.year and now.month == date_end.month and now.day == date_end.day) or (now.year == date_start.year and now.month == date_start.month and now.day == date_start.day):
            events.append(eventobj(date_start, date_end, summary))
            print("APPLIES TO TODAY!")
        else:
            continue #Event is not applicable to today
        #initialize date objects and compare
        print("Now is " + now)
    print(events)
else:
    print("Prompt the user; GO MAKE AN ICAL FILE")
