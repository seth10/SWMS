import icalendar
import os

if os.path.exists("event.ics"):
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
