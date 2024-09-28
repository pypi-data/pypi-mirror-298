import wx
A=super
C=False
V=wx.Frame
import logging
N=logging.getLogger
class D(V):
 def __init__(U,*args,**kw):
  A().__init__(*args,**kw)
  U.logger=N(__name__)
 def u(U):
  U.Show()
 def g(U,destroy=C):
  U.logger.debug(f"On close frame {self.GetTitle()}")
  if destroy:
   U.Destroy()
  else:
   U.Hide()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
