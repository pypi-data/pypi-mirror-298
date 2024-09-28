import wx
𐮃=super
𑤨=False
ꪦ=wx.Frame
import logging
𘘼=logging.getLogger
class 𮒭(ꪦ):
 def __init__(𐢕,*args,**kw):
  𐮃().__init__(*args,**kw)
  𐢕.logger=𘘼(__name__)
 def 𞠀(𐢕):
  𐢕.Show()
 def 𐰙(𐢕,destroy=𑤨):
  𐢕.logger.debug(f"On close frame {self.GetTitle()}")
  if destroy:
   𐢕.Destroy()
  else:
   𐢕.Hide()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
