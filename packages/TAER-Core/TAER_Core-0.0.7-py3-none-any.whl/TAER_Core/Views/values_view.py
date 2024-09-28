import wx
m=super
P=False
v=str
f=True
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class k(AuxViewBase):
 def __init__(L,x,title):
  m().__init__(parent=x,id=wx.NewId(),title=title,style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX,)
  L.SetMinSize(wx.Size(0,0))
  L.__create_layout()
 def __create_layout(L):
  L.SetBackgroundColour(wx.NullColour)
  L.vsizer=wx.BoxSizer(wx.VERTICAL)
  L.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  L.vsizer.Add(L.hsizer,0,wx.ALL,5)
  L.panel_values=t(L)
  L.hsizer.Add(L.panel_values,0,wx.EXPAND)
  L.SetSizerAndFit(L.vsizer)
  L.Layout()
 def N(L,values):
  L.panel_values.update_values(values)
  L.Fit()
 def U(L):
  L.panel_values.to_default_color()
 def H(L,state):
  L.panel_values.Enable(state)
class t(wx.Panel):
 def __init__(L,x):
  wx.Panel.__init__(L,x)
  L.__create_layout()
  L.values_widgets={}
  L.init_flag=P
 def __create_layout(L):
  L.SetBackgroundColour(wx.NullColour)
  L.hbox=wx.BoxSizer(wx.HORIZONTAL)
  L.vbox=wx.BoxSizer(wx.VERTICAL)
  L.hbox.Add(L.vbox,0,wx.ALL,1)
  L.grid_register=wx.GridSizer(2,0,0)
  L.vbox.Add(L.grid_register,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
  L.sizer_buttons=wx.BoxSizer(wx.HORIZONTAL)
  L.vbox.Add(L.sizer_buttons,0,wx.ALIGN_RIGHT|wx.ALL,5)
  L.button_apply=wx.Button(L,wx.ID_APPLY,"Apply")
  L.sizer_buttons.Add(L.button_apply,0,wx.ALL,5)
  L.SetSizer(L.hbox)
  L.Layout()
 def __init_values(L,values):
  for p in values.values():
   R=wx.StaticText(L,label=p.label,style=wx.CENTER)
   t1=wx.TextCtrl(L,value=v(p.value),style=wx.TE_CENTRE|wx.TE_PROCESS_ENTER)
   L.values_widgets[p.label]=t1
   L.grid_register.Add(R,0,wx.ALIGN_CENTER|wx.TOP,5)
   L.grid_register.Add(t1,0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.TOP,5)
 def N(L,values):
  if L.init_flag:
   for y in values.values():
    L.values_widgets[y.label].SetValue(v(y.value))
  else:
   L.__init_values(values)
   L.init_flag=f
  L.to_default_color()
 def K(L,w):
  w.SetBackgroundColour((128,255,0,50))
 def F(L):
  [w.SetBackgroundColour(wx.NullColour)for w in L.values_widgets.values()]
  L.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
