import matplotlib
𐲅=super
𤋫=False
㵄=None
ط=True
𐲐=max
𦊂=min
𐚱=len
ﴂ=hasattr
𫧲=int
𐼕=zip
ﴬ=matplotlib.backends
𐤩=matplotlib.figure
䲕=matplotlib.use
䲕("WXAgg")
from 𐤩 import Figure
from ﴬ.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import wx
띠=wx.RIGHT
ݸ=wx.BOTTOM
𐺂=wx.StaticText
緜=wx.Button
ﲟ=wx.StaticBoxSizer
𐠣=wx.GROW
𞠇=wx.TOP
ﻜ=wx.LEFT
𤻉=wx.Panel
岬=wx.EXPAND
ࢦ=wx.ALL
ﰨ=wx.HORIZONTAL
𐰥=wx.VERTICAL
辤=wx.BoxSizer
𐲱=wx.NullColour
𗚒=wx.Size
𥼴=wx.MAXIMIZE_BOX
𞺷=wx.RESIZE_BORDER
ဣ=wx.DEFAULT_FRAME_STYLE
𰨇=wx.lib
import 𰨇.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class 𮬅(AuxViewBase):
 def __init__(𞺥,𞠩):
  𐲅().__init__(parent=𞠩,title="Histogram",style=ဣ^𞺷^𥼴,)
  𞺥.SetMinSize(𗚒(0,0))
  𞺥.__create_layout()
  𞺥.scale_flag=𤋫
 def __create_layout(𞺥):
  𞺥.SetBackgroundColour(𐲱)
  𞺥.vsizer=辤(𐰥)
  𞺥.hsizer=辤(ﰨ)
  𞺥.vsizer.Add(𞺥.hsizer,0,ࢦ,5)
  𞺥.panel_histogram_plot=𠝄(𞺥)
  𞺥.hsizer.Add(𞺥.panel_histogram_plot,0,岬)
  𞺥.SetSizerAndFit(𞺥.vsizer)
  𞺥.Layout()
 def ﳝ(𞺥,hist):
  if hist!=㵄 and 𞺥.IsShown():
   𫝑=hist.value[0]
   𐩴=hist.value[1]
   𞺥.panel_histogram_plot.update(𫝑,𐩴)
   𞺥.Refresh()
 def 𰻹(𞺥):
  𞺥.scale_flag=ط
 def סּ(𞺥):
  𐲐=𞺥.panel_histogram_plot.txt_bin_max.GetValue()
  𦊂=𞺥.panel_histogram_plot.txt_bin_min.GetValue()
  㿥=𞺥.panel_histogram_plot.txt_bin_step.GetValue()
  return 𐲐,𦊂,㿥
class 𠝄(𤻉):
 def __init__(𞺥,𞠩):
  𤻉.__init__(𞺥,𞠩)
  𞺥.__create_layout()
 def __create_layout(𞺥):
  𞺥.SetBackgroundColour(𐲱)
  𞺥.figure=𒔾(figsize=[3.2,2.4])
  𞺥.canvas=ﰸ(𞺥,-1,𞺥.figure)
  𞺥.axes=𞺥.figure.add_subplot(111)
  𞺥.sizer_main=辤(𐰥)
  𞺥.sizer_main.Add(𞺥.canvas,1,ﻜ|𞠇|𐠣)
  𞺥.sizer_buttons=ﲟ(ﰨ,𞺥,"Settings")
  𞺥.sizer_main.Add(𞺥.sizer_buttons,0,岬|𞠇,10)
  𞺥.button_scale=緜(𞺥,label="Scale")
  𞺥.button_scale.Enable(𤋫)
  𞺥.sizer_buttons.Add(𞺥.button_scale,1,岬|ࢦ,5)
  𞺥.sizer_bins=ﲟ(ﰨ,𞺥,"Bins definition")
  ﴰ=辤(𐰥)
  ﯝ=𐺂(𞺥,label="Minimum",style=ﻜ)
  ﴰ.Add(ﯝ,0,岬|ݸ,1)
  𞺥.txt_bin_min=wxInt.IntCtrl(𞺥,𦊂=0,𐲐=65535,limited=ط)
  ﴰ.Add(𞺥.txt_bin_min,1,岬)
  𞺥.sizer_bins.Add(ﴰ,0,岬|ݸ|ﻜ|띠,5)
  ﴰ=辤(𐰥)
  ﯝ=𐺂(𞺥,label="Maximum",style=ﻜ)
  ﴰ.Add(ﯝ,0,岬|ݸ,1)
  𞺥.txt_bin_max=wxInt.IntCtrl(𞺥,𦊂=0,𐲐=65535,limited=ط)
  ﴰ.Add(𞺥.txt_bin_max,1,岬)
  𞺥.sizer_bins.Add(ﴰ,0,岬|ݸ|ﻜ|띠,5)
  ﴰ=辤(𐰥)
  ﯝ=𐺂(𞺥,label="Number of bins",style=ﻜ)
  ﴰ.Add(ﯝ,0,岬|ݸ,1)
  𞺥.txt_bin_step=wxInt.IntCtrl(𞺥,𦊂=0,𐲐=1000,limited=ط)
  ﴰ.Add(𞺥.txt_bin_step,1,岬)
  𞺥.sizer_bins.Add(ﴰ,0,岬|ݸ|ﻜ|띠,5)
  𞺥.sizer_buttons.Add(𞺥.sizer_bins,3,岬)
  𞺥.SetSizerAndFit(𞺥.sizer_main)
  𞺥.Layout()
 def 𫮳(𞺥,count,𐩴):
  if 𐚱(count)<=0 or 𐚱(𐩴)<=0:
   return
  if not ﴂ(𞺥,"bar_plot")or 𞺥.GetParent().scale_flag:
   𞺥.button_scale.Enable(ط)
   𞺥.axes.cla()
   𩁝,𩁝,𞺥.bar_plot=𞺥.axes.hist(𐩴[:-1],𐩴,weights=count)
   𞺥.axes.relim()
   𞺥.txt_bin_max.ChangeValue(𫧲(𐩴[-1]))
   𞺥.txt_bin_min.ChangeValue(𫧲(𐩴[0]))
   𞺥.txt_bin_step.ChangeValue(𐚱(𐩴))
   𞺥.GetParent().scale_flag=𤋫
  else:
   𐼻=𞺥.bar_plot
   for 𠎊,𓎊 in 𐼕(count,𐼻.patches):
    𓎊.set_height(𠎊)
   𞺥.axes.autoscale_view()
  𞺥.canvas.draw()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
