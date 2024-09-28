import wx
L=super
R=True
g=False
Q=hasattr
v=pow
import wx.lib.scrolledpanel
import wx.lib.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class A(AuxViewBase):
 def __init__(q,P):
  L().__init__(parent=P,id=wx.NewId(),title="Chip registers",style=wx.DEFAULT_FRAME_STYLE^wx.MAXIMIZE_BOX,)
  q.SetMaxClientSize((600,800))
  q.__create_layout()
 def __create_layout(q):
  q.SetBackgroundColour(wx.NullColour)
  q.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  q.vsizer=wx.BoxSizer(wx.VERTICAL)
  q.hsizer.Add(q.vsizer,1,wx.EXPAND|wx.ALL,5)
  q.panel_values=E(q)
  q.vsizer.Add(q.panel_values,1,wx.EXPAND|wx.ALL)
  q.sizer_buttons=wx.BoxSizer(wx.HORIZONTAL)
  q.vsizer.Add(q.sizer_buttons,0,wx.ALIGN_RIGHT|wx.ALL,5)
  q.button_apply=wx.Button(q,wx.ID_APPLY,"Apply")
  q.sizer_buttons.Add(q.button_apply,0,wx.ALL,10)
  q.SetAutoLayout(R)
  q.SetSizerAndFit(q.hsizer)
  q.Layout()
 def c(q,values):
  q.panel_values.update_values(values)
  q.Fit()
class E(wx.lib.scrolledpanel.ScrolledPanel):
 def __init__(q,*args,**kw):
  L().__init__(*args,**kw)
  q.SetMinClientSize((400,400))
  q.SetMaxClientSize((600,1000))
  q.SetAutoLayout(R)
  q.SetupScrolling()
  q.__create_layout()
  q.init_flag=g
  q.values_widgets={}
 def __create_layout(q):
  q.SetBackgroundColour(wx.NullColour)
  q.hbox=wx.BoxSizer(wx.HORIZONTAL)
  q.vbox=wx.BoxSizer(wx.VERTICAL)
  q.hbox.Add(q.vbox,1,wx.EXPAND|wx.ALL,1)
  q.SetSizer(q.hbox)
  q.Layout()
 def __init_values(q,values):
  for O in values.values():
   D=wx.StaticBoxSizer(wx.HORIZONTAL,q,O.label)
   x=wx.FlexGridSizer(cols=2,vgap=3,hgap=10)
   x.SetFlexibleDirection(wx.BOTH)
   D.Add(x,1,wx.ALL|wx.EXPAND,5)
   if Q(O,"signals"):
    for T in O.signals.values():
     h=wx.StaticText(q,label=T.label,style=wx.CENTER)
     x.Add(h,1,wx.ALL|wx.EXPAND|wx.LEFT|wx.ALIGN_CENTRE_VERTICAL,5,)
     if T.nbits==1:
      t1=wx.CheckBox(q)
      x.Add(t1,1,wx.ALL|wx.LEFT|wx.ALIGN_CENTRE_VERTICAL,2)
     else:
      F=v(2,T.nbits)-1
      t1=wxInt.IntCtrl(q,style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER,min=0,max=F,limited=R,)
      x.Add(t1,1,wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL,1)
     q.values_widgets[T.label]=t1
   else:
    h=wx.StaticText(q,label="Value",style=wx.CENTER)
    x.Add(h,1,wx.ALL|wx.EXPAND|wx.LEFT|wx.ALIGN_CENTRE_VERTICAL,5)
    F=v(2,8)-1
    t1=wxInt.IntCtrl(q,style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER,min=0,max=F,limited=R,)
    x.Add(t1,1,wx.ALL|wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL,1)
    q.values_widgets[O.label]=t1
   q.vbox.Add(D,0,wx.EXPAND|wx.ALL,5)
  q.Fit()
 def c(q,values):
  if q.init_flag:
   for _,O in values.items():
    for _,T in O.signals.items():
     S=O.get_signal(T.label)
     q.values_widgets[T.label].SetValue(S)
  else:
   q.__init_values(values)
   q.init_flag=R
  q.to_default_color()
 def k(q,f):
  f.SetBackgroundColour((128,255,0,50))
 def n(q):
  [f.SetBackgroundColour(wx.NullColour)for f in q.values_widgets.values()]
  q.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
