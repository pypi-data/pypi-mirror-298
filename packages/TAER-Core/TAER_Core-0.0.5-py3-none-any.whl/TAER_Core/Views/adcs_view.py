import wx
uS=super
uL=False
uf=str
uX=True
up=min
uT=range
uK=len
ui=abs
ua=max
uV=list
uQ=zip
ud=wx.LEFT
uD=wx.ALIGN_RIGHT
uh=wx.TOP
uk=wx.ALIGN_LEFT
uo=wx.CheckBox
ut=wx.TE_READONLY
ue=wx.CENTER
uU=wx.StaticText
uW=wx.ALIGN_CENTER_VERTICAL
uJ=wx.ID_APPLY
b=wx.Button
C=wx.TE_CENTRE
B=wx.TextCtrl
z=wx.FlexGridSizer
x=wx.StaticBoxSizer
n=wx.Panel
I=wx.ALL
E=wx.EXPAND
H=wx.HORIZONTAL
R=wx.VERTICAL
w=wx.BoxSizer
G=wx.NullColour
y=wx.Size
N=wx.MAXIMIZE_BOX
r=wx.DEFAULT_FRAME_STYLE
j=wx.NewId
Y=wx.lib
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
from Y import plot as wxplot
uO=wxplot.PlotGraphics
uc=wxplot.PolySpline
um=wxplot.PlotCanvas
class l(AuxViewBase):
 def __init__(J,u):
  uS().__init__(parent=u,id=j(),title="ADC signals",style=r^N,)
  J.SetMinSize(y(1000,300))
  J.__create_layout()
 def __create_layout(J):
  J.SetBackgroundColour(G)
  J.panel_menu=W(J)
  J.panel_plot=U(J)
  J.vbox=w(R)
  J.hbox=w(H)
  J.vbox.Add(J.hbox,1,E|I,5)
  J.hbox.Add(J.panel_menu,0,E)
  J.hbox.Add(J.panel_plot,1,E|I,10)
  J.SetSizerAndFit(J.vbox)
  J.Layout()
 def K(J,values,ts):
  J.panel_menu.update_channels(values,ts)
  J.panel_plot.update_subplots(values)
 def i(J,values):
  J.panel_menu.update_isenabled(values)
  J.panel_plot.update_panels(values)
 def a(J):
  J.panel_menu.to_default_color()
 def V(J,state):
  J.panel_menu.Enable(state)
class W(n):
 def __init__(J,u):
  uS().__init__(u)
  J.__create_layout()
  J.values_widgets={}
  J.enable_widgets={}
  J.init_flag=uL
 def __create_layout(J):
  J.SetBackgroundColour(G)
  J.hbox=w(H)
  J.vbox=w(R)
  J.adc_box=x(H,J,"ADC channels")
  J.grid_register=z(cols=3,hgap=0,vgap=0)
  J.adc_box.Add(J.grid_register,0,E|I,10)
  J.sizer_sampletime=x(H,J,"Sample time")
  J.sampletime_textbox=B(J,style=C)
  J.button_update=b(J,uJ,"Update")
  J.sizer_sampletime.Add(J.sampletime_textbox,1,uW|I,10)
  J.sizer_sampletime.Add(J.button_update,0,E|I,10)
  J.vbox.Add(J.adc_box,0,E|I,5)
  J.vbox.Add(J.sizer_sampletime,0,E|I,5)
  J.hbox.Add(J.vbox,1,E|I,1)
  J.SetSizer(J.hbox)
  J.Layout()
 def __init_adc_values(J,values):
  for o in values.values():
   k=uU(J,label="CH"+uf(o.channel)+": "+o.label,style=ue,)
   t1=B(J,value=uf(o.value),style=ut)
   c1=uo(J)
   c1.SetValue(o.IsEnabled)
   J.enable_widgets[o.label]=c1
   J.values_widgets[o.label]=t1
   J.grid_register.Add(k,1,E|uk|uh,5)
   J.grid_register.Add(t1,1,uW|uD|ud|uh,5)
   J.grid_register.Add(c1,1,E|ud|uh,5)
  J.Fit()
  J.GetParent().Fit()
 def __inti_sampletime_value(J,ts):
  J.sampletime_textbox.SetValue(uf(ts))
 def Q(J,values,ts):
  if J.init_flag:
   for h in values.values():
    J.values_widgets[h.label].SetValue(uf(h.data_y[-1]))
  else:
   J.__init_adc_values(values)
   J.__inti_sampletime_value(ts)
   J.init_flag=uX
  J.g()
 def v(J,values):
  for h in values.values():
   h.IsEnabled=J.enable_widgets[h.label].GetValue()
 def M(J,D):
  D.SetBackgroundColour((128,255,0,50))
 def g(J):
  [D.SetBackgroundColour(G)for D in J.values_widgets.values()]
  J.Refresh()
class U(n):
 def __init__(J,u):
  n.__init__(J,u)
  J.__create_layout()
  J.init_flag=uL
 def __create_layout(J):
  J.SetBackgroundColour(G)
  J.hbox=w(H)
  J.vbox=w(R)
  J.hbox.Add(J.vbox,1,E|I,5)
  J.canvas_list={}
  J.SetSizer(J.hbox)
  J.Layout()
 def __init_subplots(J,values):
  for o in values.values():
   d=A(J)
   J.canvas_list[o.label]=d
   J.vbox.Add(d,1,E|I,5)
  J.Fit()
  J.GetParent().Fit()
 def i(J,values):
  for h in values.values(): 
   if h.IsEnabled:
    J.canvas_list[h.label].Show()
   else:
    J.canvas_list[h.label].Hide()
  J.Layout()
 def q(J,values):
  if J.init_flag:
   for h in values.values():
    J.canvas_list[h.label].update_plot(h)
  else:
   J.__init_subplots(values)
   J.init_flag=uX
class A(um):
 def __init__(J,u):
  um.__init__(J,u)
  J.SetMinSize(y(300,100))
  J.__create_layout()
  J.init_flag=uL
 def __create_layout(J):
  J.SetBackgroundColour(G)
  J.enableLegend=uX
 def s(J,h):
  if h.data_t[-1]<15:
   m=15
   c=0
  else:
   m=h.data_t[-1]
   c=m-15 
  O=up(uT(uK(h.data_t)),key=lambda i:ui(h.data_t[i]-c)) 
  x=h.data_t[O::].copy()
  y=h.data_y[O::].copy()
  if ua(y)==0:
   S=0.15
  elif ua(y)>0:
   S=1.15*ua(y)
  else:
   S=0.85*ua(y)
  if up(y)==0:
   L=-0.15
  elif up(y)>0:
   L=0.85*up(y)
  else:
   L=1.15*up(y)
  x=h.data_t
  y=h.data_y
  f=uV(uQ(x,y))
  X=uc(f,legend="CH"+uf(h.channel),colour="blue",width=1)
  p=uO([X],xLabel="Time (s)",yLabel=h.label)
  J.Draw(p,xAxis=(c,m),yAxis=(L,S))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
