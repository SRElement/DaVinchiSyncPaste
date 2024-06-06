#!/user/bin/env python

from AudioClip import AudioClip
class AudioTimeline:

    _audioTracks = {}
    _timeline = {}
    
    def __init__(self, timeline, frameRate):
        self._frameRate = frameRate
        self.GenerateTracks(timeline)
        self.GenerateAudioTimeline()

    def GenerateTracks(self, timeline):
        for i in range(1,timeline.GetTrackCount("audio")+1): #Create tracks
            if "Ready" in timeline.GetTrackName("audio",i): #If track is named Ready (So the user can control what tracks they want to use)
                clipsInTrack = timeline.GetItemListInTrack("audio",i)
                #TODO Add a way for user to select what clips they want excluded (Color them red?)
                self._audioTracks[i] = clipsInTrack

    def GenerateAudioTimeline(self):
        #Convert frames to timecode
        #https://gist.github.com/schiffty/c838db504b9a1a7c23a30c366e8005e8

        def frames_to_TC (frames):
            h = int(frames / 86400) 
            m = int(frames / 1440) % 60 
            s = int((frames % 1440)/self._frameRate) 
            f = frames % 1440 % self._frameRate
            return ( "%02d:%02d:%02d:%02d" % ( h, m, s, f))

        for track in self._audioTracks:
            for clip in self._audioTracks[track]:
                clipName = clip.GetName()
                clipStart = frames_to_TC(clip.GetStart())
                clipEnd = frames_to_TC(clip.GetEnd())
                toNearestSecond = clipStart[:-2] + '00' #Round to nearest second (All clips that start within that second will be grouped)

                index = 0

                if self._timeline.get(toNearestSecond) == None: #If clip start does not have a key yet (A clip starting at that time does not exist yet)
                    self._timeline[toNearestSecond] = [AudioClip(track,index,clipStart,clipEnd,clip.GetEnd())] #Create new key of start timecode
                else: #If it does exist
                    self._timeline[toNearestSecond].append(AudioClip(track,index,clipStart,clipEnd,clip.GetEnd())) #Append to starting timecode

    
    def FindClipStart(self, startTime):
        return self._timeline[startTime][0].startTimecode

    def FindClipEnd(self, startTime): #Find the latest timecode of a clip

        latest = None

        for clip in self._timeline[startTime]: #Find largest = latest
            if latest == None:
                latest = clip
            elif latest.endFrame < clip.endFrame:
                latest = clip
    
        return latest.endTimecode
    
    def GetTimeLine(self):
        return self._timeline