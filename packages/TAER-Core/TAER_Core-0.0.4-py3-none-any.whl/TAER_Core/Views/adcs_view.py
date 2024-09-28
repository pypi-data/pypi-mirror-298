import wx
𧓻=super
𤪔=False
渍=str
ﺸ=True
𬠦=min
ߚ=range
𣵾=len
ܮ=abs
𐲒=max
𨅑=list
𰿰=zip
𐂿=wx.LEFT
𤠴=wx.ALIGN_RIGHT
ꃏ=wx.TOP
ࠔ=wx.ALIGN_LEFT
𐰬=wx.CheckBox
扆=wx.TE_READONLY
𰥨=wx.CENTER
𐪌=wx.StaticText
𩖉=wx.ALIGN_CENTER_VERTICAL
𝕵=wx.ID_APPLY
ڟ=wx.Button
𐬡=wx.TE_CENTRE
哆=wx.TextCtrl
ﹾ=wx.FlexGridSizer
𐺈=wx.StaticBoxSizer
𣉊=wx.Panel
𞤴=wx.ALL
䢖=wx.EXPAND
𰀫=wx.HORIZONTAL
𐦨=wx.VERTICAL
𘙞=wx.BoxSizer
𘔍=wx.NullColour
𐿄=wx.Size
𐀩=wx.MAXIMIZE_BOX
𭨬=wx.DEFAULT_FRAME_STYLE
욉=wx.NewId
𐼰=wx.lib
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
from 𐼰 import plot as wxplot
𗌧=wxplot.PlotGraphics
𰫆=wxplot.PolySpline
𐳘=wxplot.PlotCanvas
class ߋ(AuxViewBase):
 def __init__(𘨐,ﶚ):
  𧓻().__init__(parent=ﶚ,id=욉(),title="ADC signals",style=𭨬^𐀩,)
  𘨐.SetMinSize(𐿄(1000,300))
  𘨐.__create_layout()
 def __create_layout(𘨐):
  𘨐.SetBackgroundColour(𘔍)
  𘨐.panel_menu=ﰞ(𘨐)
  𘨐.panel_plot=𡾑(𘨐)
  𘨐.vbox=𘙞(𐦨)
  𘨐.hbox=𘙞(𰀫)
  𘨐.vbox.Add(𘨐.hbox,1,䢖|𞤴,5)
  𘨐.hbox.Add(𘨐.panel_menu,0,䢖)
  𘨐.hbox.Add(𘨐.panel_plot,1,䢖|𞤴,10)
  𘨐.SetSizerAndFit(𘨐.vbox)
  𘨐.Layout()
 def 𑘕(𘨐,values,ts):
  𘨐.panel_menu.update_channels(values,ts)
  𘨐.panel_plot.update_subplots(values)
 def 𐦌(𘨐,values):
  𘨐.panel_menu.update_isenabled(values)
  𘨐.panel_plot.update_panels(values)
 def 齀(𘨐):
  𘨐.panel_menu.to_default_color()
 def 籘(𘨐,state):
  𘨐.panel_menu.Enable(state)
class ﰞ(𣉊):
 def __init__(𘨐,ﶚ):
  𧓻().__init__(ﶚ)
  𘨐.__create_layout()
  𘨐.values_widgets={}
  𘨐.enable_widgets={}
  𘨐.init_flag=𤪔
 def __create_layout(𘨐):
  𘨐.SetBackgroundColour(𘔍)
  𘨐.hbox=𘙞(𰀫)
  𘨐.vbox=𘙞(𐦨)
  𘨐.adc_box=𐺈(𰀫,𘨐,"ADC channels")
  𘨐.grid_register=ﹾ(cols=3,hgap=0,vgap=0)
  𘨐.adc_box.Add(𘨐.grid_register,0,䢖|𞤴,10)
  𘨐.sizer_sampletime=𐺈(𰀫,𘨐,"Sample time")
  𘨐.sampletime_textbox=哆(𘨐,style=𐬡)
  𘨐.button_update=ڟ(𘨐,𝕵,"Update")
  𘨐.sizer_sampletime.Add(𘨐.sampletime_textbox,1,𩖉|𞤴,10)
  𘨐.sizer_sampletime.Add(𘨐.button_update,0,䢖|𞤴,10)
  𘨐.vbox.Add(𘨐.adc_box,0,䢖|𞤴,5)
  𘨐.vbox.Add(𘨐.sizer_sampletime,0,䢖|𞤴,5)
  𘨐.hbox.Add(𘨐.vbox,1,䢖|𞤴,1)
  𘨐.SetSizer(𘨐.hbox)
  𘨐.Layout()
 def __init_adc_values(𘨐,values):
  for 븟 in values.values():
   𡺄=𐪌(𘨐,label="CH"+渍(븟.channel)+": "+븟.label,style=𰥨,)
   ﳎ=哆(𘨐,value=渍(븟.value),style=扆)
   𐦨=𐰬(𘨐)
   𐦨.SetValue(븟.IsEnabled)
   𘨐.enable_widgets[븟.label]=𐦨
   𘨐.values_widgets[븟.label]=ﳎ
   𘨐.grid_register.Add(𡺄,1,䢖|ࠔ|ꃏ,5)
   𘨐.grid_register.Add(ﳎ,1,𩖉|𤠴|𐂿|ꃏ,5)
   𘨐.grid_register.Add(𐦨,1,䢖|𐂿|ꃏ,5)
  𘨐.Fit()
  𘨐.GetParent().Fit()
 def __inti_sampletime_value(𘨐,ts):
  𘨐.sampletime_textbox.SetValue(渍(ts))
 def ﻰ(𘨐,values,ts):
  if 𘨐.init_flag:
   for 𞹱 in values.values():
    𘨐.values_widgets[𞹱.label].SetValue(渍(𞹱.data_y[-1]))
  else:
   𘨐.__init_adc_values(values)
   𘨐.__inti_sampletime_value(ts)
   𘨐.init_flag=ﺸ
  𘨐.𩨐()
 def ﰩ(𘨐,values):
  for 𞹱 in values.values():
   𞹱.IsEnabled=𘨐.enable_widgets[𞹱.label].GetValue()
 def 𐰹(𘨐,𥗁):
  𥗁.SetBackgroundColour((128,255,0,50))
 def 𩨐(𘨐):
  [𥗁.SetBackgroundColour(𘔍)for 𥗁 in 𘨐.values_widgets.values()]
  𘨐.Refresh()
class 𡾑(𣉊):
 def __init__(𘨐,ﶚ):
  𣉊.__init__(𘨐,ﶚ)
  𘨐.__create_layout()
  𘨐.init_flag=𤪔
 def __create_layout(𘨐):
  𘨐.SetBackgroundColour(𘔍)
  𘨐.hbox=𘙞(𰀫)
  𘨐.vbox=𘙞(𐦨)
  𘨐.hbox.Add(𘨐.vbox,1,䢖|𞤴,5)
  𘨐.canvas_list={}
  𘨐.SetSizer(𘨐.hbox)
  𘨐.Layout()
 def __init_subplots(𘨐,values):
  for 븟 in values.values():
   𞸘=𬱏(𘨐)
   𘨐.canvas_list[븟.label]=𞸘
   𘨐.vbox.Add(𞸘,1,䢖|𞤴,5)
  𘨐.Fit()
  𘨐.GetParent().Fit()
 def 𐦌(𘨐,values):
  for 𞹱 in values.values(): 
   if 𞹱.IsEnabled:
    𘨐.canvas_list[𞹱.label].Show()
   else:
    𘨐.canvas_list[𞹱.label].Hide()
  𘨐.Layout()
 def ﵮ(𘨐,values):
  if 𘨐.init_flag:
   for 𞹱 in values.values():
    𘨐.canvas_list[𞹱.label].update_plot(𞹱)
  else:
   𘨐.__init_subplots(values)
   𘨐.init_flag=ﺸ
class 𬱏(𐳘):
 def __init__(𘨐,ﶚ):
  𐳘.__init__(𘨐,ﶚ)
  𘨐.SetMinSize(𐿄(300,100))
  𘨐.__create_layout()
  𘨐.init_flag=𤪔
 def __create_layout(𘨐):
  𘨐.SetBackgroundColour(𘔍)
  𘨐.enableLegend=ﺸ
 def 𒁗(𘨐,𞹱):
  if 𞹱.data_t[-1]<15:
   𗵩=15
   ﭭ=0
  else:
   𗵩=𞹱.data_t[-1]
   ﭭ=𗵩-15 
  𘞃=𬠦(ߚ(𣵾(𞹱.data_t)),key=lambda i:ܮ(𞹱.data_t[i]-ﭭ)) 
  פֿ=𞹱.data_t[𘞃::].copy()
  忭=𞹱.data_y[𘞃::].copy()
  if 𐲒(忭)==0:
   濻=0.15
  elif 𐲒(忭)>0:
   濻=1.15*𐲒(忭)
  else:
   濻=0.85*𐲒(忭)
  if 𬠦(忭)==0:
   𭹕=-0.15
  elif 𬠦(忭)>0:
   𭹕=0.85*𬠦(忭)
  else:
   𭹕=1.15*𬠦(忭)
  פֿ=𞹱.data_t
  忭=𞹱.data_y
  𮄼=𨅑(𰿰(פֿ,忭))
  坿=𰫆(𮄼,legend="CH"+渍(𞹱.channel),colour="blue",width=1)
  𤻿=𗌧([坿],xLabel="Time (s)",yLabel=𞹱.label)
  𘨐.Draw(𤻿,xAxis=(ﭭ,𗵩),yAxis=(𭹕,濻))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
