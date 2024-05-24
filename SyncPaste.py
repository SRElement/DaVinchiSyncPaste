#!/user/bin/env python

import keyboard
from AudioTimeline import AudioTimeline
from time import sleep

#get project
proj = resolve.GetProjectManager().GetCurrentProject()

#get timeline
timeline = proj.GetTimelineByIndex(1)

#Create AudioTimeline
AudioTimeline = AudioTimeline(timeline, proj.GetSetting('timelineFrameRate'))

ClipTimeLine = AudioTimeline.GetTimeLine()

sleep(2) #Wait before starting to allow menu to close 
#TODO Change to hotkey to begin?

for clipStart in ClipTimeLine: #Find points to insert clips and insert them
    startTC = AudioTimeline.FindClipStart(clipStart)
    endTC = AudioTimeline.FindClipEnd(clipStart)

    timeline.SetCurrentTimecode(startTC)
    keyboard.send('i') #In Point hotkey
    sleep(0.1)

    timeline.SetCurrentTimecode(endTC)
    keyboard.send('o') #Out point hotkey
    sleep(0.1)

    keyboard.send('shift+f11') #Paste clip to fit between in & out points

    keyboard.send('alt+x') #Deselect hotkeys
    