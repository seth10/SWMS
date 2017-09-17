import icalendar
import os
import datetime
import string

"""
This program imports a native .ics Ical file, and preprocesses it to form a basic schedule. Using machine learning, we attempt to let the AI choose which activities to schedule throughout the day. User feedback iteratively improves the resulting schedules.
"""

class eventobj:
    def __init__(self, dateS, dateE, summary, flexibilityFactor=False):
        self.isFlexible = flexibilityFactor
        self.dateStart = dateS
        self.dateEnd = dateE
        timeTypes = ["sleep", "meal", "exercise", "leisure", "study", "class", "obligation", "gap", "transition", "earlyWakeTime", "lateWake", "earlySleep", "lateSleep"]
        matched = False
        for category in timeTypes:
            if '#'+category+'#' in summary or '#'+category+'#' == summary:
                self.timeType = category
                matched = True
                break
        if not matched:
            #Prompt user for category type
            print(summary + ": obligation")
            self.timeType = "obligation"
        #Also prompt user for missing necessary categories

    def deconstruct():
        #Need to store auxiliary information so as not to perform lossy transformations
        return "BEGIN:VEVENT\nEND:VEVENT"

    def __repr__(self):
        return '\n'.join([str(self.dateStart), str(self.dateEnd), self.timeType, str(self.isFlexible)])
        #return str(self.dateStart) + '\n' + str(self.dateEnd) + '\n' + self.timeType + '\n' + str(self.isFlexible)



        

if os.path.exists("test_calendar.ics"):
    print("Load the string")
    with open('test_calendar.ics', 'r') as myfile:
        data=myfile.read()
    """the_calendar = icalendar.Calendar().from_ical(data)
    for key in the_calendar:
        print(key)"""
    print()
    events_raw = data.split("BEGIN:VEVENT")[1::]
    events = []
    for event in events_raw:
        process = False
        for line in event.splitlines():
            if "DTSTART:" in line:
                process = True
                #print(line)
                line = str(line.split("DTSTART:")[1][:15:])
                #line2 = ''.join(c for c in line if c not in string.ascii_letters)
                #print(line2)
                #print(line[1][13::15])
                #print(line)
                #date_start = datetime.datetime(int(str(line[0::4])), int(str(line[4::6])), int(str(line[6::8])), int(str(line[9::11])), int(str(line[11::13])), int(str(line[13::15])))
                date_start = datetime.datetime.strptime(line, "%Y%m%dT%H%M%S")
                #print(date_start)    
            elif "DTEND:" in line:
                print(line)
                line = str(line.split("DTEND:")[1][:15:])
                date_end = datetime.datetime.strptime(line, "%Y%m%dT%H%M%S")
                #print(date_end)
            elif "DESCRIPTION:" in line:
                #print("desc line " + line)
                summary = line.split("DESCRIPTION:")[1]
                #print(summary)
        if not process:
            continue
        now = datetime.datetime.today()#Add one day for tomorrow? TODO
        if (now.year == date_end.year and now.month == date_end.month and now.day == date_end.day) or (now.year == date_start.year and now.month == date_start.month and now.day == date_start.day):
            events.append(eventobj(date_start, date_end, summary))
            #print("APPLIES TO TODAY!")
        else:
            continue #Event is not applicable to today
    #print("\nAbout to list events\n")
    #print(events)
    events = sorted(events, key=lambda x: x.dateStart)#TODO check if properly sorts for more than one variable
    print("\nSorted events:")
    print(events)
    the_clone = events
    #Insert padding to generate and place Transition/Gap objects- use timedelta
    skip = False
    offset = 1
    for i in range(len(events)-1):#start at 0 and stop before final object- assume first and last objects are wake/sleep? TODO
        if skip:
            skip = False
            i += offset
            offset += 1
        difference = events[i+1].dateStart-events[i].dateEnd
        print(str(events[i+1].dateStart) + ", " + str(events[i].dateEnd) + ", " + str(i))
        print("Difference is " + str(difference.total_seconds()))
        if difference.total_seconds() == 0:
            continue
        elif difference.total_seconds() < 0:
            print("CONFLICT! ABORT ABORT!")
        elif difference.total_seconds() <= 30*60:#30 minutes or less is a TRANSITION period
            #create event Transition object
            the_clone.insert(i+1, eventobj(events[i].dateEnd, events[i+1].dateStart, "#transition#"))
            skip = True
        else:
            #create event Gap object
            print("Made a gap")
            the_clone.insert(i+1, eventobj(events[i].dateEnd, events[i+1].dateStart, "#gap#", True))
            skip = True
    print()
    print(the_clone)
    print()
    current_freqs = {}
    #TODO implement sleep wake times
    desired_freqs = {"meal":2, "exercise":1, "leisure":5, "study":3, "class":3, "obligation":1}
    total = 0
    for key in desired_freqs.keys():
        total += desired_freqs[key]
    #print(total)
    dfreqs = desired_freqs #Stores desired RELATIVE frequencies
    for key in desired_freqs.keys():
        dfreqs[key] /= total
    print("dfreqs originally made here: " + str(dfreqs))
    for event in events:
        if event.timeType not in ["gap", "transition"]:
            if event.timeType not in current_freqs.keys():
                current_freqs.update({event.timeType:1})
            else:
                current_freqs[event.timeType] += 1
    for key in desired_freqs.keys():#For events that aren't scheduled at all, and need to be represented by 0
        if key not in current_freqs.keys():
            current_freqs.update({key:0})
    print("currently observed freqs: " + str(current_freqs))
    total = 0
    for key in current_freqs.keys():
        total += current_freqs[key]
    #print(total)
    cfreqs = current_freqs
    for key in current_freqs.keys():
        cfreqs[key] /= total
    print("Currently observed RELATIVE freqs: " + str(cfreqs))
    spareTime = [] #Stores lists of [gap length, position in master event list]
    for i in range(len(the_clone)):
        #print(the_clone[i].timeType)
        if the_clone[i].timeType == "gap":
            spareTime.append([(the_clone[i].dateEnd - the_clone[i].dateStart).total_seconds(), i])
    #print(spareTime)
    spareTime = sorted(spareTime, key=lambda x: x[0], reverse=True)#Sort by the largest gap, in seconds
    print("Initial spareTime: " + str(spareTime))
    totalTime = 0
    for gap in spareTime:
        totalTime += gap[0]
    print(totalTime)
    numOfParts = 5
    equal_piece = totalTime / numOfParts #Iterate multiple times to better distribute time where needed
    offset = 0 #Use an offset value since we'll be increasing the number of Event objects- POSSIBLE POTENTIAL PROBLEM
    for i in range(numOfParts):
        not_enough = []
        gift = equal_piece
        for key in dfreqs.keys():
            #print(key)
            #print(str(dfreqs[key]) + " " + str(cfreqs[key]))
            diff = (dfreqs[key] - cfreqs[key])
            if diff > .1:#POSSIBLE POTENTIAL PROBLEM- some relative frequencies are small so subtracting zero would lead to them being excluded
                not_enough.append([key, diff])
        print("Relative percentage discrepancies: " + str(not_enough))
        j = 0
        while(gift > 30*60) and (len(spareTime) != 0):
            #This loop replaces gap objects with a Transition Object, an Activity Object, and then another Gap object if time remains
            print("spare time while loop")
            max_time = spareTime[0][0]
            desired_act = not_enough[j%len(not_enough[0])][0]#Iterate through activities currently lacking in time
            print(str(desired_act))
            j += 1
            if max_time > 90*60+30*60 and gift > 90*60:
                #Pluck out 90 minute period by creating a transition first
                the_clone.insert(spareTime[0][1]+offset, eventobj(the_clone[spareTime[0][1]+offset].dateStart, the_clone[spareTime[0][1]+offset].dateStart + datetime.timedelta(minutes=15), "#transition#"))
                offset += 1
                #Insert new activity
                print(the_clone[spareTime[0][1]+offset])
                the_clone.insert(spareTime[0][1]+offset, eventobj(the_clone[spareTime[0][1]+offset-1].dateEnd, the_clone[spareTime[0][1]+offset-1].dateEnd + datetime.timedelta(minutes=90), "#"+desired_act+"#", True))
                #offset += 1
                gift -= (90 + 15) * 60
                #change Gap's start time
                the_clone[spareTime[0][1]+offset+1].dateStart = the_clone[spareTime[0][1]+offset].dateEnd
                print("A NEW GAP: " + str(the_clone[spareTime[0][1]+offset]))
                #OFFSET IS THE PROBLEM- WE SORT BY GAP SIZE NOT BY GAP ORDER; OFFSET MAY NOT NEED TO BE TAKEN INTO ACCOUNT
                the_diff = (the_clone[spareTime[0][1]+offset].dateEnd - the_clone[spareTime[0][1]+offset].dateStart).total_seconds()
                gift -= the_diff
                #spareTime[0][0] = the_diff
                if the_diff > 30*60:
                    spareTime.append([the_diff, spareTime[0][1]+offset+1])
                    print("SHOULD BE A GAP: " + str(spareTime[0][1]+offset+1))
                    print(the_clone)
                    #spareTime.append([the_diff, eventobj(the_clone[spareTime[0][1]+offset].dateStart, the_clone[spareTime[0][1]+offset].dateEnd, "#gap#", True)])
                    spareTime = sorted(spareTime, key=lambda x: x[0])
                else:
                    print("SPARE TIME")
                    print(spareTime)
                    spareTime = spareTime[1::]
                    #offset -= 1 #EXPERIMENTAL
                print("the clone follows " + str(the_clone))
                    
            elif max_time > 60*60+30*60:
                #Pluck out 60 minute period
                print("placeholder")
                spareTime = ""
                gift = 0
                break
            elif max_time > 30*60+30*60:
                #Pluck out 30 minute period
                print("placeholder")
                spareTime = ""
                gift = 0
                break
            #Update the frequencies to better decide where to spend remaining time on
            for event in events:
                if event.timeType not in ["gap", "transition"]:
                    if event.timeType not in current_freqs.keys():
                        current_freqs.update({event.timeType:1})
                    else:
                        current_freqs[event.timeType] += 1
            for key in desired_freqs.keys():
                if key not in current_freqs.keys():
                    current_freqs.update({key:0})
            print("current freqs: " + str(current_freqs))
            total = 0
            for key in current_freqs.keys():
                total += current_freqs[key]
            print(total)
            cfreqs = current_freqs
            for key in current_freqs.keys():
                cfreqs[key] /= total
            print("cfreqs: " + str(cfreqs))
        print(the_clone)
        print(spareTime)
        print(len(spareTime))
        print(gift)
else:
    print("Prompt the user; GO MAKE AN ICAL FILE")
