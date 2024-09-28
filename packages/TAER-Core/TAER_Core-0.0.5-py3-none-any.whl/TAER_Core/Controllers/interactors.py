import wx
F=isinstance
G=wx.CheckBox
K=wx.EVT_TEXT_ENTER
u=wx.EVT_TEXT
a=wx.EVT_CHECKBOX
T=wx.ID_FILE9
U=wx.ID_FILE1
t=wx.EVT_MENU_RANGE
B=wx.EVT_MENU
S=wx.EVT_RADIOBOX
N=wx.EVT_BUTTON
A=wx.EVT_CLOSE
n=wx.lib
import n.intctrl as wxInt
class k:
 def s(P,X,z):
  P.presenter=X
  P.delegates=X.delegates_main
  P.view=z
  P.__config_delegates()
 def __config_delegates(P):
  P.view.Bind(A,P.__on_close)
  P.view.edit_register_device_frame.Bind(A,P.__on_close)
  P.view.edit_register_chip_frame.Bind(A,P.__on_close)
  P.view.edit_dac_frame.Bind(A,P.__on_close)
  P.view.device_info_frame.Bind(A,P.__on_close)
  P.view.image_histogram_frame.Bind(A,P.__on_close)
  P.view.serial_control_frame.Bind(A,P.__on_close)
  P.view.adc_control_frame.Bind(A,P.__on_close)
  P.__config_control_button_delegates()
  P.__config_menu_bar_delegates()
  P.__config_other_delegates()
  P.__config_adc_delegates()
 def __config_control_button_delegates(P):
  e=P.view.panel_control
  e.button_start_stop.Bind(N,P.__on_start_stop)
  e.button_capture.Bind(N,P.__on_capture)
  e.button_reset.Bind(N,P.__on_reset)
  e.button_reset_periphery.Bind(N,P.__on_reset_periphery)
  e.button_reset_chip.Bind(N,P.__on_reset_chip)
  e.modes_box.Bind(S,P.__on_mode_change)
 def __config_menu_bar_delegates(P):
  P.view.Bind(B,P.__on_menu_edit,P.view.menu_bar.menu_edit.item_save_preset,)
  P.view.Bind(B,P.__on_menu_edit,P.view.menu_bar.menu_edit.item_load_preset,)
  P.view.Bind(B,P.__on_menu_edit,P.view.menu_bar.menu_edit.item_reg_dev)
  P.view.Bind(B,P.__on_menu_edit,P.view.menu_bar.menu_edit.item_reg_chip)
  P.view.Bind(B,P.__on_menu_edit,P.view.menu_bar.menu_edit.item_dac)
  P.view.Bind(B,P.__on_menu_device,P.view.menu_bar.menu_device.item_program,)
  P.view.Bind(B,P.__on_menu_device,P.view.menu_bar.menu_device.item_info)
  P.view.Bind(t,P.__on_menu_device_file_history,id=U,id2=T,)
  P.view.Bind(B,P.__on_menu_image,P.view.menu_bar.menu_image.item_histogram,)
  for l in P.view.menu_bar.menu_tools.items.values():
   P.view.Bind(B,P.__on_menu_tools,l)
 def __config_other_delegates(P):
  z=P.view.image_histogram_frame
  z.panel_histogram_plot.button_scale.Bind(N,P.__on_image_histogram_scale)
  z=P.view.serial_control_frame
  z.panel_serial_control.btn_write.Bind(N,P.__on_write_spi)
 def __config_adc_delegates(P):
  z=P.view.adc_control_frame
  z.panel_menu.button_update.Bind(N,P.__on_update_adc_ts)
  v=z.panel_menu.enable_widgets
  for L in v.values():
   L.Bind(a,P.__on_update_adc_panels)
 def __on_close(P,evt):
  P.delegates.on_close(evt.GetEventObject())
 def __on_start_stop(P,evt):
  P.delegates.on_start_stop()
 def __on_capture(P,evt):
  P.delegates.on_capture()
 def __on_reset(P,evt):
  P.delegates.on_reset()
 def __on_reset_periphery(P,evt):
  P.delegates.on_reset_periphery()
 def __on_reset_chip(P,evt):
  P.delegates.on_reset_chip()
 def __on_mode_change(P,evt):
  L=evt.GetEventObject()
  r=L.GetSelection()
  P.delegates.on_mode_change(L.GetItemLabel(r))
 def __on_menu_edit(P,evt):
  l=P.view.menu_bar.menu_edit.item_save_preset
  if evt.GetId()==l.GetId():
   P.delegates.on_save_preset()
  l=P.view.menu_bar.menu_edit.item_load_preset
  if evt.GetId()==l.GetId():
   P.delegates.on_load_preset()
  l=P.view.menu_bar.menu_edit.item_reg_dev
  if evt.GetId()==l.GetId():
   P.delegates.on_show_registers_device()
  l=P.view.menu_bar.menu_edit.item_reg_chip
  if evt.GetId()==l.GetId():
   P.delegates.on_show_registers_chip()
  l=P.view.menu_bar.menu_edit.item_dac
  if evt.GetId()==l.GetId():
   P.delegates.on_show_dacs()
 def __on_menu_device(P,evt):
  l=P.view.menu_bar.menu_device.item_program
  if evt.Id==l.GetId():
   P.delegates.on_program()
  l=P.view.menu_bar.menu_device.item_info
  if evt.Id==l.GetId():
   P.delegates.on_show_device_info()
 def __on_menu_device_file_history(P,evt):
  d=evt.GetId()-U
  P.delegates.on_program_recent_file(d)
 def __on_menu_image(P,evt):
  l=P.view.menu_bar.menu_image.item_histogram
  if evt.Id==l.GetId():
   P.delegates.on_show_histogram()
 def __on_menu_tools(P,evt):
  l=P.view.menu_bar.menu_tools.items["Write SPI"]
  if evt.Id==l.GetId():
   P.delegates.on_show_write_spi()
   return
  l=P.view.menu_bar.menu_tools.items["ADCs"]
  if evt.Id==l.GetId():
   P.delegates.on_show_adcs()
   return
  l=P.view.menu_bar.menu_tools.items["Execute test"]
  if evt.Id==l.GetId():
   P.delegates.on_test()
   return
  for x,tool in P.presenter.tools.items():
   l=P.view.menu_bar.menu_tools.items[x]
   if evt.Id==l.GetId():
    P.delegates.on_show_tools(tool)
 def __on_image_histogram_scale(P,evt):
  P.delegates.on_scale_histogram()
 def __on_write_spi(P,evt):
  P.delegates.on_write_spi()
 def __on_update_adc_ts(P,evt):
  P.delegates.on_update_adc_ts()
 def __on_update_adc_panels(P,evt):
  P.delegates.on_update_adc_panels()
class y:
 def s(P,q,z):
  P.delegates=q
  P.view=z
  P.H()
 def H(P):
  P.view.panel_values.button_apply.Bind(N,P.m)
  V=P.view.panel_values.values_widgets.values()
  for L in V:
   L.Bind(u,P.O)
   L.Bind(K,P.m)
 def O(P,evt):
  P.delegates.on_text_change(evt.GetEventObject())
 def m(P,evt):
  P.delegates.on_apply()
class f(y):
 def H(P):
  P.view.button_apply.Bind(N,P.m)
  V=P.view.panel_values.values_widgets.values()
  for L in V:
   if F(L,G):
    L.Bind(a,P.__on_check_box)
   elif F(L,wxInt.IntCtrl):
    L.Bind(u,P.O)
    L.Bind(K,P.m)
 def __on_check_box(P,evt):
  L=evt.GetEventObject()
  P.delegates.on_check_box_change(L)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
