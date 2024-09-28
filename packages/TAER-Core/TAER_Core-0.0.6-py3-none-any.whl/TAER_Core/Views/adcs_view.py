import wx
Gr=super
Gx=False
GJ=str
GA=True
Gy=min
GS=range
GH=len
GN=abs
Gl=max
Gp=list
Gv=zip
GF=wx.LEFT
Ga=wx.ALIGN_RIGHT
Gq=wx.TOP
GU=wx.ALIGN_LEFT
GX=wx.CheckBox
GI=wx.TE_READONLY
Gj=wx.CENTER
Gn=wx.StaticText
Gh=wx.ALIGN_CENTER_VERTICAL
GE=wx.ID_APPLY
B=wx.Button
s=wx.TE_CENTRE
o=wx.TextCtrl
C=wx.FlexGridSizer
f=wx.StaticBoxSizer
k=wx.Panel
K=wx.ALL
e=wx.EXPAND
g=wx.HORIZONTAL
u=wx.VERTICAL
Q=wx.BoxSizer
b=wx.NullColour
D=wx.Size
t=wx.MAXIMIZE_BOX
L=wx.DEFAULT_FRAME_STYLE
Y=wx.NewId
R=wx.lib
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
from R import plot as wxplot
Gm=wxplot.PlotGraphics
Gw=wxplot.PolySpline
Gi=wxplot.PlotCanvas
class z(AuxViewBase):
 def __init__(E,G):
  Gr().__init__(parent=G,id=Y(),title="ADC signals",style=L^t,)
  E.SetMinSize(D(1000,300))
  E.__create_layout()
 def __create_layout(E):
  E.SetBackgroundColour(b)
  E.panel_menu=h(E)
  E.panel_plot=n(E)
  E.vbox=Q(u)
  E.hbox=Q(g)
  E.vbox.Add(E.hbox,1,e|K,5)
  E.hbox.Add(E.panel_menu,0,e)
  E.hbox.Add(E.panel_plot,1,e|K,10)
  E.SetSizerAndFit(E.vbox)
  E.Layout()
 def H(E,values,ts):
  E.panel_menu.update_channels(values,ts)
  E.panel_plot.update_subplots(values)
 def N(E,values):
  E.panel_menu.update_isenabled(values)
  E.panel_plot.update_panels(values)
 def l(E):
  E.panel_menu.to_default_color()
 def p(E,state):
  E.panel_menu.Enable(state)
class h(k):
 def __init__(E,G):
  Gr().__init__(G)
  E.__create_layout()
  E.values_widgets={}
  E.enable_widgets={}
  E.init_flag=Gx
 def __create_layout(E):
  E.SetBackgroundColour(b)
  E.hbox=Q(g)
  E.vbox=Q(u)
  E.adc_box=f(g,E,"ADC channels")
  E.grid_register=C(cols=3,hgap=0,vgap=0)
  E.adc_box.Add(E.grid_register,0,e|K,10)
  E.sizer_sampletime=f(g,E,"Sample time")
  E.sampletime_textbox=o(E,style=s)
  E.button_update=B(E,GE,"Update")
  E.sizer_sampletime.Add(E.sampletime_textbox,1,Gh|K,10)
  E.sizer_sampletime.Add(E.button_update,0,e|K,10)
  E.vbox.Add(E.adc_box,0,e|K,5)
  E.vbox.Add(E.sizer_sampletime,0,e|K,5)
  E.hbox.Add(E.vbox,1,e|K,1)
  E.SetSizer(E.hbox)
  E.Layout()
 def __init_adc_values(E,values):
  for X in values.values():
   U=Gn(E,label="CH"+GJ(X.channel)+": "+X.label,style=Gj,)
   t1=o(E,value=GJ(X.value),style=GI)
   c1=GX(E)
   c1.SetValue(X.IsEnabled)
   E.enable_widgets[X.label]=c1
   E.values_widgets[X.label]=t1
   E.grid_register.Add(U,1,e|GU|Gq,5)
   E.grid_register.Add(t1,1,Gh|Ga|GF|Gq,5)
   E.grid_register.Add(c1,1,e|GF|Gq,5)
  E.Fit()
  E.GetParent().Fit()
 def __inti_sampletime_value(E,ts):
  E.sampletime_textbox.SetValue(GJ(ts))
 def v(E,values,ts):
  if E.init_flag:
   for q in values.values():
    E.values_widgets[q.label].SetValue(GJ(q.data_y[-1]))
  else:
   E.__init_adc_values(values)
   E.__inti_sampletime_value(ts)
   E.init_flag=GA
  E.T()
 def V(E,values):
  for q in values.values():
   q.IsEnabled=E.enable_widgets[q.label].GetValue()
 def M(E,a):
  a.SetBackgroundColour((128,255,0,50))
 def T(E):
  [a.SetBackgroundColour(b)for a in E.values_widgets.values()]
  E.Refresh()
class n(k):
 def __init__(E,G):
  k.__init__(E,G)
  E.__create_layout()
  E.init_flag=Gx
 def __create_layout(E):
  E.SetBackgroundColour(b)
  E.hbox=Q(g)
  E.vbox=Q(u)
  E.hbox.Add(E.vbox,1,e|K,5)
  E.canvas_list={}
  E.SetSizer(E.hbox)
  E.Layout()
 def __init_subplots(E,values):
  for X in values.values():
   F=O(E)
   E.canvas_list[X.label]=F
   E.vbox.Add(F,1,e|K,5)
  E.Fit()
  E.GetParent().Fit()
 def N(E,values):
  for q in values.values(): 
   if q.IsEnabled:
    E.canvas_list[q.label].Show()
   else:
    E.canvas_list[q.label].Hide()
  E.Layout()
 def c(E,values):
  if E.init_flag:
   for q in values.values():
    E.canvas_list[q.label].update_plot(q)
  else:
   E.__init_subplots(values)
   E.init_flag=GA
class O(Gi):
 def __init__(E,G):
  Gi.__init__(E,G)
  E.SetMinSize(D(300,100))
  E.__create_layout()
  E.init_flag=Gx
 def __create_layout(E):
  E.SetBackgroundColour(b)
  E.enableLegend=GA
 def P(E,q):
  if q.data_t[-1]<15:
   i=15
   w=0
  else:
   i=q.data_t[-1]
   w=i-15 
  m=Gy(GS(GH(q.data_t)),key=lambda i:GN(q.data_t[i]-w)) 
  x=q.data_t[m::].copy()
  y=q.data_y[m::].copy()
  if Gl(y)==0:
   r=0.15
  elif Gl(y)>0:
   r=1.15*Gl(y)
  else:
   r=0.85*Gl(y)
  if Gy(y)==0:
   x=-0.15
  elif Gy(y)>0:
   x=0.85*Gy(y)
  else:
   x=1.15*Gy(y)
  x=q.data_t
  y=q.data_y
  J=Gp(Gv(x,y))
  A=Gw(J,legend="CH"+GJ(q.channel),colour="blue",width=1)
  y=Gm([A],xLabel="Time (s)",yLabel=q.label)
  E.Draw(y,xAxis=(w,i),yAxis=(x,r))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
