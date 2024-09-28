import wx
m=super
U=False
Q=wx.Frame
import logging
N=logging.getLogger
class z(Q):
 def __init__(E,*args,**kw):
  m().__init__(*args,**kw)
  E.logger=N(__name__)
 def o(E):
  E.Show()
 def v(E,destroy=U):
  E.logger.debug(f"On close frame {self.GetTitle()}")
  if destroy:
   E.Destroy()
  else:
   E.Hide()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
