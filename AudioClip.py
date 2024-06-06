#!/user/bin/env python

class AudioClip:
    
   def __init__(self, track, index, startTC, endTC, endFrame):
      self._track = track
      self._index = index
      self._startTimecode = startTC
      self._endTimecode = endTC
      self._endFrame = endFrame

   @property
   def track(self):
      return self._track
   
   @property
   def index(self):
      return self._index
   
   @property
   def startTimecode(self):
      return self._startTimecode
   
   @property
   def endTimecode(self):
      return self._endTimecode
   
   @property
   def endFrame(self):
      return self._endFrame