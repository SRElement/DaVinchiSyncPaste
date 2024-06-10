#!/user/bin/env python

import keyboard
from AudioTimeline import AudioTimeline
from time import sleep
import json

#get project
proj = resolve.GetProjectManager().GetCurrentProject()

#get timeline
timeline = proj.GetTimelineByIndex(1)

#Create AudioTimeline
AudioTimeline = AudioTimeline(timeline, proj.GetSetting('timelineFrameRate'))

ClipTimeLine = AudioTimeline.GetTimeLine()


cwd = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Fusion\\Scripts\\Utility"

with open(cwd+"\\Data\\ProgramData.json", "r") as f:
    programDataDict = json.loads(f.read())
    f.close()

for clipStart in ClipTimeLine: #Find points to insert clips and insert them
    charactersNotUsed = [char for char in programDataDict["Characters"]]
    startTC = AudioTimeline.FindClipStart(clipStart)
    midTC = AudioTimeline.FindClipMid(clipStart)
    endTC = AudioTimeline.FindClipEnd(clipStart)

    timeline.SetCurrentTimecode(startTC)
    keyboard.send('i') #In Point hotkey
    sleep(1)

    timeline.SetCurrentTimecode(endTC)
    keyboard.send('o') #Out point hotkey
    sleep(1)

    keyboard.send('shift+f11') #Paste clip to fit between in & out points

    keyboard.send('alt+x') #Deselect hotkeys
    sleep(1)

    timeline.SetCurrentTimecode(midTC)
    sleep(1)

    for clip in ClipTimeLine[clipStart]:
        characterName = clip.clipOwner
        charactersNotUsed.remove(characterName)
        character = programDataDict["Characters"][characterName]
        audioFilePath = character["audioPath"]
        audioFileName = character["audioClips"][str(clip.index)]

        characterWAV = characterName + "WAV"

        comp = timeline.GetCurrentVideoItem().GetFusionCompByIndex(1)
        toExec = 'comp.'+characterWAV+'.WaveFile = ' + repr(audioFilePath+audioFileName)
        exec(toExec)


    for char in charactersNotUsed:
        characterWAV = char + "WAV"

        toExec = "comp."+characterWAV+".WaveFile =" + repr(cwd+ "\\Silence.wav")
        exec(toExec)

    sleep(1)

    
    