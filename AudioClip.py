#!/user/bin/env python

class AudioClip:
    
   def __init__(self, character, index, startTC, endTC, endFrame):
      self._character = character
      self._index = index
      self._startTimecode = startTC
      self._endTimecode = endTC
      self._endFrame = endFrame

   @property
   def character(self):
      return self._character
   
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