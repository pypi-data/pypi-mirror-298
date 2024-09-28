import wx
m=super
A=False
b=str
K=True
N=min
i=range
O=len
v=abs
l=max
S=list
V=zip
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
from wx.lib import plot as wxplot
class P(AuxViewBase):
 def __init__(I,Y):
  m().__init__(parent=Y,id=wx.NewId(),title="ADC signals",style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX,)
  I.SetMinSize(wx.Size(1000,300))
  I.__create_layout()
 def __create_layout(I):
  I.SetBackgroundColour(wx.NullColour)
  I.panel_menu=E(I)
  I.panel_plot=p(I)
  I.vbox=wx.BoxSizer(wx.VERTICAL)
  I.hbox=wx.BoxSizer(wx.HORIZONTAL)
  I.vbox.Add(I.hbox,1,wx.EXPAND|wx.ALL,5)
  I.hbox.Add(I.panel_menu,0,wx.EXPAND)
  I.hbox.Add(I.panel_plot,1,wx.EXPAND|wx.ALL,10)
  I.SetSizerAndFit(I.vbox)
  I.Layout()
 def f(I,values,ts):
  I.panel_menu.update_channels(values,ts)
  I.panel_plot.update_subplots(values)
 def k(I,values):
  I.panel_menu.update_isenabled(values)
  I.panel_plot.update_panels(values)
 def X(I):
  I.panel_menu.to_default_color()
 def B(I,state):
  I.panel_menu.Enable(state)
class E(wx.Panel):
 def __init__(I,Y):
  m().__init__(Y)
  I.__create_layout()
  I.values_widgets={}
  I.enable_widgets={}
  I.init_flag=A
 def __create_layout(I):
  I.SetBackgroundColour(wx.NullColour)
  I.hbox=wx.BoxSizer(wx.HORIZONTAL)
  I.vbox=wx.BoxSizer(wx.VERTICAL)
  I.adc_box=wx.StaticBoxSizer(wx.HORIZONTAL,I,"ADC channels")
  I.grid_register=wx.FlexGridSizer(cols=3,hgap=0,vgap=0)
  I.adc_box.Add(I.grid_register,0,wx.EXPAND|wx.ALL,10)
  I.sizer_sampletime=wx.StaticBoxSizer(wx.HORIZONTAL,I,"Sample time")
  I.sampletime_textbox=wx.TextCtrl(I,style=wx.TE_CENTRE)
  I.button_update=wx.Button(I,wx.ID_APPLY,"Update")
  I.sizer_sampletime.Add(I.sampletime_textbox,1,wx.ALIGN_CENTER_VERTICAL|wx.ALL,10)
  I.sizer_sampletime.Add(I.button_update,0,wx.EXPAND|wx.ALL,10)
  I.vbox.Add(I.adc_box,0,wx.EXPAND|wx.ALL,5)
  I.vbox.Add(I.sizer_sampletime,0,wx.EXPAND|wx.ALL,5)
  I.hbox.Add(I.vbox,1,wx.EXPAND|wx.ALL,1)
  I.SetSizer(I.hbox)
  I.Layout()
 def __init_adc_values(I,values):
  for j in values.values():
   F=wx.StaticText(I,label="CH"+b(j.channel)+": "+j.label,style=wx.CENTER,)
   t1=wx.TextCtrl(I,value=b(j.value),style=wx.TE_READONLY)
   c1=wx.CheckBox(I)
   c1.SetValue(j.IsEnabled)
   I.enable_widgets[j.label]=c1
   I.values_widgets[j.label]=t1
   I.grid_register.Add(F,1,wx.EXPAND|wx.ALIGN_LEFT|wx.TOP,5)
   I.grid_register.Add(t1,1,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.TOP,5)
   I.grid_register.Add(c1,1,wx.EXPAND|wx.LEFT|wx.TOP,5)
  I.Fit()
  I.GetParent().Fit()
 def __inti_sampletime_value(I,ts):
  I.sampletime_textbox.SetValue(b(ts))
 def h(I,values,ts):
  if I.init_flag:
   for s in values.values():
    I.values_widgets[s.label].SetValue(b(s.data_y[-1]))
  else:
   I.__init_adc_values(values)
   I.__inti_sampletime_value(ts)
   I.init_flag=K
  I.to_default_color()
 def a(I,values):
  for s in values.values():
   s.IsEnabled=I.enable_widgets[s.label].GetValue()
 def u(I,c):
  c.SetBackgroundColour((128,255,0,50))
 def W(I):
  [c.SetBackgroundColour(wx.NullColour)for c in I.values_widgets.values()]
  I.Refresh()
class p(wx.Panel):
 def __init__(I,Y):
  wx.Panel.__init__(I,Y)
  I.__create_layout()
  I.init_flag=A
 def __create_layout(I):
  I.SetBackgroundColour(wx.NullColour)
  I.hbox=wx.BoxSizer(wx.HORIZONTAL)
  I.vbox=wx.BoxSizer(wx.VERTICAL)
  I.hbox.Add(I.vbox,1,wx.EXPAND|wx.ALL,5)
  I.canvas_list={}
  I.SetSizer(I.hbox)
  I.Layout()
 def __init_subplots(I,values):
  for j in values.values():
   R=r(I)
   I.canvas_list[j.label]=R
   I.vbox.Add(R,1,wx.EXPAND|wx.ALL,5)
  I.Fit()
  I.GetParent().Fit()
 def k(I,values):
  for s in values.values(): 
   if s.IsEnabled:
    I.canvas_list[s.label].Show()
   else:
    I.canvas_list[s.label].Hide()
  I.Layout()
 def M(I,values):
  if I.init_flag:
   for s in values.values():
    I.canvas_list[s.label].update_plot(s)
  else:
   I.__init_subplots(values)
   I.init_flag=K
class r(wxplot.PlotCanvas):
 def __init__(I,Y):
  wxplot.PlotCanvas.__init__(I,Y)
  I.SetMinSize(wx.Size(300,100))
  I.__create_layout()
  I.init_flag=A
 def __create_layout(I):
  I.SetBackgroundColour(wx.NullColour)
  I.enableLegend=K
 def n(I,s):
  if s.data_t[-1]<15:
   x=15
   U=0
  else:
   x=s.data_t[-1]
   U=x-15 
  o=N(i(O(s.data_t)),key=lambda i:v(s.data_t[i]-U)) 
  x=s.data_t[o::].copy()
  y=s.data_y[o::].copy()
  if l(y)==0:
   T=0.15
  elif l(y)>0:
   T=1.15*l(y)
  else:
   T=0.85*l(y)
  if N(y)==0:
   y=-0.15
  elif N(y)>0:
   y=0.85*N(y)
  else:
   y=1.15*N(y)
  x=s.data_t
  y=s.data_y
  D=S(V(x,y))
  g=wxplot.PolySpline(D,legend="CH"+b(s.channel),colour="blue",width=1)
  C=wxplot.PlotGraphics([g],xLabel="Time (s)",yLabel=s.label)
  I.Draw(C,xAxis=(U,x),yAxis=(y,T))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
