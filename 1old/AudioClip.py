#!/user/bin/env python

class AudioClip:
    
   def __init__(self, clipOwner, index, startTC, midTC, endTC, endFrame):
      self._clipOwner = clipOwner
      self._index = index
      self._startTimecode = startTC
      self._midTimecode = midTC
      self._endTimecode = endTC
      self._endFrame = endFrame

   @property
   def clipOwner(self):
      return self._clipOwner
   
   @property
   def index(self):
      return self._index
   
   @property
   def startTimecode(self):
      return self._startTimecode
   
   @property
   def midTimecode(self):
      return self._midTimecode
   
   @property
   def endTimecode(self):
      return self._endTimecode
   
   @property
   def endFrame(self):
      return self._endFrame