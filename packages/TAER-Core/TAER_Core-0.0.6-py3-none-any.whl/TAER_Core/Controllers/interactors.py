import wx
b=isinstance
f=wx.CheckBox
x=wx.EVT_TEXT_ENTER
u=wx.EVT_TEXT
V=wx.EVT_CHECKBOX
C=wx.ID_FILE9
D=wx.ID_FILE1
H=wx.EVT_MENU_RANGE
m=wx.EVT_MENU
M=wx.EVT_RADIOBOX
L=wx.EVT_BUTTON
K=wx.EVT_CLOSE
t=wx.lib
import t.intctrl as wxInt
class y:
 def P(S,r,o):
  S.presenter=r
  S.delegates=r.delegates_main
  S.view=o
  S.__config_delegates()
 def __config_delegates(S):
  S.view.Bind(K,S.__on_close)
  S.view.edit_register_device_frame.Bind(K,S.__on_close)
  S.view.edit_register_chip_frame.Bind(K,S.__on_close)
  S.view.edit_dac_frame.Bind(K,S.__on_close)
  S.view.device_info_frame.Bind(K,S.__on_close)
  S.view.image_histogram_frame.Bind(K,S.__on_close)
  S.view.serial_control_frame.Bind(K,S.__on_close)
  S.view.adc_control_frame.Bind(K,S.__on_close)
  S.__config_control_button_delegates()
  S.__config_menu_bar_delegates()
  S.__config_other_delegates()
  S.__config_adc_delegates()
 def __config_control_button_delegates(S):
  Y=S.view.panel_control
  Y.button_start_stop.Bind(L,S.__on_start_stop)
  Y.button_capture.Bind(L,S.__on_capture)
  Y.button_reset.Bind(L,S.__on_reset)
  Y.button_reset_periphery.Bind(L,S.__on_reset_periphery)
  Y.button_reset_chip.Bind(L,S.__on_reset_chip)
  Y.modes_box.Bind(M,S.__on_mode_change)
 def __config_menu_bar_delegates(S):
  S.view.Bind(m,S.__on_menu_edit,S.view.menu_bar.menu_edit.item_save_preset,)
  S.view.Bind(m,S.__on_menu_edit,S.view.menu_bar.menu_edit.item_load_preset,)
  S.view.Bind(m,S.__on_menu_edit,S.view.menu_bar.menu_edit.item_reg_dev)
  S.view.Bind(m,S.__on_menu_edit,S.view.menu_bar.menu_edit.item_reg_chip)
  S.view.Bind(m,S.__on_menu_edit,S.view.menu_bar.menu_edit.item_dac)
  S.view.Bind(m,S.__on_menu_device,S.view.menu_bar.menu_device.item_program,)
  S.view.Bind(m,S.__on_menu_device,S.view.menu_bar.menu_device.item_info)
  S.view.Bind(H,S.__on_menu_device_file_history,id=D,id2=C,)
  S.view.Bind(m,S.__on_menu_image,S.view.menu_bar.menu_image.item_histogram,)
  for d in S.view.menu_bar.menu_tools.items.values():
   S.view.Bind(m,S.__on_menu_tools,d)
 def __config_other_delegates(S):
  o=S.view.image_histogram_frame
  o.panel_histogram_plot.button_scale.Bind(L,S.__on_image_histogram_scale)
  o=S.view.serial_control_frame
  o.panel_serial_control.btn_write.Bind(L,S.__on_write_spi)
 def __config_adc_delegates(S):
  o=S.view.adc_control_frame
  o.panel_menu.button_update.Bind(L,S.__on_update_adc_ts)
  U=o.panel_menu.enable_widgets
  for h in U.values():
   h.Bind(V,S.__on_update_adc_panels)
 def __on_close(S,evt):
  S.delegates.on_close(evt.GetEventObject())
 def __on_start_stop(S,evt):
  S.delegates.on_start_stop()
 def __on_capture(S,evt):
  S.delegates.on_capture()
 def __on_reset(S,evt):
  S.delegates.on_reset()
 def __on_reset_periphery(S,evt):
  S.delegates.on_reset_periphery()
 def __on_reset_chip(S,evt):
  S.delegates.on_reset_chip()
 def __on_mode_change(S,evt):
  h=evt.GetEventObject()
  c=h.GetSelection()
  S.delegates.on_mode_change(h.GetItemLabel(c))
 def __on_menu_edit(S,evt):
  d=S.view.menu_bar.menu_edit.item_save_preset
  if evt.GetId()==d.GetId():
   S.delegates.on_save_preset()
  d=S.view.menu_bar.menu_edit.item_load_preset
  if evt.GetId()==d.GetId():
   S.delegates.on_load_preset()
  d=S.view.menu_bar.menu_edit.item_reg_dev
  if evt.GetId()==d.GetId():
   S.delegates.on_show_registers_device()
  d=S.view.menu_bar.menu_edit.item_reg_chip
  if evt.GetId()==d.GetId():
   S.delegates.on_show_registers_chip()
  d=S.view.menu_bar.menu_edit.item_dac
  if evt.GetId()==d.GetId():
   S.delegates.on_show_dacs()
 def __on_menu_device(S,evt):
  d=S.view.menu_bar.menu_device.item_program
  if evt.Id==d.GetId():
   S.delegates.on_program()
  d=S.view.menu_bar.menu_device.item_info
  if evt.Id==d.GetId():
   S.delegates.on_show_device_info()
 def __on_menu_device_file_history(S,evt):
  a=evt.GetId()-D
  S.delegates.on_program_recent_file(a)
 def __on_menu_image(S,evt):
  d=S.view.menu_bar.menu_image.item_histogram
  if evt.Id==d.GetId():
   S.delegates.on_show_histogram()
 def __on_menu_tools(S,evt):
  d=S.view.menu_bar.menu_tools.items["Write SPI"]
  if evt.Id==d.GetId():
   S.delegates.on_show_write_spi()
   return
  d=S.view.menu_bar.menu_tools.items["ADCs"]
  if evt.Id==d.GetId():
   S.delegates.on_show_adcs()
   return
  d=S.view.menu_bar.menu_tools.items["Execute test"]
  if evt.Id==d.GetId():
   S.delegates.on_test()
   return
  for I,tool in S.presenter.tools.items():
   d=S.view.menu_bar.menu_tools.items[I]
   if evt.Id==d.GetId():
    S.delegates.on_show_tools(tool)
 def __on_image_histogram_scale(S,evt):
  S.delegates.on_scale_histogram()
 def __on_write_spi(S,evt):
  S.delegates.on_write_spi()
 def __on_update_adc_ts(S,evt):
  S.delegates.on_update_adc_ts()
 def __on_update_adc_panels(S,evt):
  S.delegates.on_update_adc_panels()
class B:
 def P(S,N,o):
  S.delegates=N
  S.view=o
  S.i()
 def i(S):
  S.view.panel_values.button_apply.Bind(L,S.n)
  O=S.view.panel_values.values_widgets.values()
  for h in O:
   h.Bind(u,S.p)
   h.Bind(x,S.n)
 def p(S,evt):
  S.delegates.on_text_change(evt.GetEventObject())
 def n(S,evt):
  S.delegates.on_apply()
class X(B):
 def i(S):
  S.view.button_apply.Bind(L,S.n)
  O=S.view.panel_values.values_widgets.values()
  for h in O:
   if b(h,f):
    h.Bind(V,S.__on_check_box)
   elif b(h,wxInt.IntCtrl):
    h.Bind(u,S.p)
    h.Bind(x,S.n)
 def __on_check_box(S,evt):
  h=evt.GetEventObject()
  S.delegates.on_check_box_change(h)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
