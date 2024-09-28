import wx
E=super
D=False
import logging
class M(wx.Frame):
 def __init__(G,*args,**kw):
  E().__init__(*args,**kw)
  G.logger=logging.getLogger(__name__)
 def Q(G):
  G.Show()
 def N(G,destroy=D):
  G.logger.debug(f"On close frame {self.GetTitle()}")
  if destroy:
   G.Destroy()
  else:
   G.Hide()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
