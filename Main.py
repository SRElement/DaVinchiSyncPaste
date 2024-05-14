#!/user/bin/env python

import keyboard
from AudioTimeline import AudioTimeline
from time import sleep

#get project
proj = resolve.GetProjectManager().GetCurrentProject()

#get timeline
timeline = proj.GetTimelineByIndex(1)

#Create AudioTimeline
AudioTimeline = AudioTimeline(timeline)



# #get audio items from track
# audioClips = timeline.GetItemListInTrack("audio",1)

#For each clip
# for clip in audioClips:
#     #Get start and end times as timecode
#     clipStart = frames_to_TC(clip.GetStart())
#     clipEnd = frames_to_TC(clip.GetEnd())

#     #Set in and out timecodes for clip
#     timeline.SetCurrentTimecode(clipStart)
#     keyboard.send('i') #In hotkey
#     sleep(0.1)

#     timeline.SetCurrentTimecode(clipEnd)
#     keyboard.send('o') #Out hotkey
#     sleep(0.1)

#     #Paste clip between them
#     keyboard.send('ctrl+v')
#     sleep(0.1)
#     keyboard.send('alt+i') #Deselect hotkeys
#     keyboard.send('alt+o')


