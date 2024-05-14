#!/user/bin/env python

#Convert frames to timecode
#https://gist.github.com/schiffty/c838db504b9a1a7c23a30c366e8005e8
def frames_to_TC (frames):
    h = int(frames / 86400) 
    m = int(frames / 1440) % 60 
    s = int((frames % 1440)/24) 
    #Set frame access as to 00 to ensure clips group to the second not frame
    return ( '%02d:%02d:%02d:00' % (h, m, s))

class AudioTimeline:

    _audioTracks = []
    _timeline = {}
    
    def __init__(self, timeline):
        self.GenerateTracks(timeline)
        self.GenerateAudioTimeline(timeline)
        print(self.GetAudioTimeline())

    def GenerateTracks(self, timeline):
        for i in range(1,timeline.GetTrackCount("audio")+1): #Create tracks
            if "Ready" in timeline.GetTrackName("audio",i): #If track is named Ready (So the user can control what tracks they want to use)
                clipsInTrack = timeline.GetItemListInTrack("audio",i)
                #TODO Add a way for user to select what clips they want excluded (Color them red?)
                self._audioTracks.append(clipsInTrack)

    def GenerateAudioTimeline(self, timeline):
        for track in self._audioTracks:
            for clip in track:
                clipName = clip.GetName()
                clipStart = frames_to_TC(clip.GetStart())
                clipEnd = frames_to_TC(clip.GetEnd())
                if self._timeline.get(clipStart) == None: #If clip start does not have a key yet (A clip starting at that time does not exist yet)
                    self._timeline[clipStart] = [{"ClipName":clipName,"ClipEnd":clipEnd}]
                else:
                    self._timeline[clipStart].append({"ClipName":clipName,"ClipEnd":clipEnd})

    def GetAudioTimeline(self):
        return(self._timeline)