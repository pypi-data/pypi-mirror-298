import wx
v=isinstance
import wx.lib.intctrl as wxInt
class y:
 def d(Y,a,x):
  Y.presenter=a
  Y.delegates=a.delegates_main
  Y.view=x
  Y.__config_delegates()
 def __config_delegates(Y):
  Y.view.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.edit_register_device_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.edit_register_chip_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.edit_dac_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.device_info_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.image_histogram_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.serial_control_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.view.adc_control_frame.Bind(wx.EVT_CLOSE,Y.__on_close)
  Y.__config_control_button_delegates()
  Y.__config_menu_bar_delegates()
  Y.__config_other_delegates()
  Y.__config_adc_delegates()
 def __config_control_button_delegates(Y):
  M=Y.view.panel_control
  M.button_start_stop.Bind(wx.EVT_BUTTON,Y.__on_start_stop)
  M.button_capture.Bind(wx.EVT_BUTTON,Y.__on_capture)
  M.button_reset.Bind(wx.EVT_BUTTON,Y.__on_reset)
  M.button_reset_periphery.Bind(wx.EVT_BUTTON,Y.__on_reset_periphery)
  M.button_reset_chip.Bind(wx.EVT_BUTTON,Y.__on_reset_chip)
  M.modes_box.Bind(wx.EVT_RADIOBOX,Y.__on_mode_change)
 def __config_menu_bar_delegates(Y):
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_edit,Y.view.menu_bar.menu_edit.item_save_preset,)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_edit,Y.view.menu_bar.menu_edit.item_load_preset,)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_edit,Y.view.menu_bar.menu_edit.item_reg_dev)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_edit,Y.view.menu_bar.menu_edit.item_reg_chip)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_edit,Y.view.menu_bar.menu_edit.item_dac)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_device,Y.view.menu_bar.menu_device.item_program,)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_device,Y.view.menu_bar.menu_device.item_info)
  Y.view.Bind(wx.EVT_MENU_RANGE,Y.__on_menu_device_file_history,id=wx.ID_FILE1,id2=wx.ID_FILE9,)
  Y.view.Bind(wx.EVT_MENU,Y.__on_menu_image,Y.view.menu_bar.menu_image.item_histogram,)
  for J in Y.view.menu_bar.menu_tools.items.values():
   Y.view.Bind(wx.EVT_MENU,Y.__on_menu_tools,J)
 def __config_other_delegates(Y):
  x=Y.view.image_histogram_frame
  x.panel_histogram_plot.button_scale.Bind(wx.EVT_BUTTON,Y.__on_image_histogram_scale)
  x=Y.view.serial_control_frame
  x.panel_serial_control.btn_write.Bind(wx.EVT_BUTTON,Y.__on_write_spi)
 def __config_adc_delegates(Y):
  x=Y.view.adc_control_frame
  x.panel_menu.button_update.Bind(wx.EVT_BUTTON,Y.__on_update_adc_ts)
  s=x.panel_menu.enable_widgets
  for D in s.values():
   D.Bind(wx.EVT_CHECKBOX,Y.__on_update_adc_panels)
 def __on_close(Y,evt):
  Y.delegates.on_close(evt.GetEventObject())
 def __on_start_stop(Y,evt):
  Y.delegates.on_start_stop()
 def __on_capture(Y,evt):
  Y.delegates.on_capture()
 def __on_reset(Y,evt):
  Y.delegates.on_reset()
 def __on_reset_periphery(Y,evt):
  Y.delegates.on_reset_periphery()
 def __on_reset_chip(Y,evt):
  Y.delegates.on_reset_chip()
 def __on_mode_change(Y,evt):
  D=evt.GetEventObject()
  S=D.GetSelection()
  Y.delegates.on_mode_change(D.GetItemLabel(S))
 def __on_menu_edit(Y,evt):
  J=Y.view.menu_bar.menu_edit.item_save_preset
  if evt.GetId()==J.GetId():
   Y.delegates.on_save_preset()
  J=Y.view.menu_bar.menu_edit.item_load_preset
  if evt.GetId()==J.GetId():
   Y.delegates.on_load_preset()
  J=Y.view.menu_bar.menu_edit.item_reg_dev
  if evt.GetId()==J.GetId():
   Y.delegates.on_show_registers_device()
  J=Y.view.menu_bar.menu_edit.item_reg_chip
  if evt.GetId()==J.GetId():
   Y.delegates.on_show_registers_chip()
  J=Y.view.menu_bar.menu_edit.item_dac
  if evt.GetId()==J.GetId():
   Y.delegates.on_show_dacs()
 def __on_menu_device(Y,evt):
  J=Y.view.menu_bar.menu_device.item_program
  if evt.Id==J.GetId():
   Y.delegates.on_program()
  J=Y.view.menu_bar.menu_device.item_info
  if evt.Id==J.GetId():
   Y.delegates.on_show_device_info()
 def __on_menu_device_file_history(Y,evt):
  b=evt.GetId()-wx.ID_FILE1
  Y.delegates.on_program_recent_file(b)
 def __on_menu_image(Y,evt):
  J=Y.view.menu_bar.menu_image.item_histogram
  if evt.Id==J.GetId():
   Y.delegates.on_show_histogram()
 def __on_menu_tools(Y,evt):
  J=Y.view.menu_bar.menu_tools.items["Write SPI"]
  if evt.Id==J.GetId():
   Y.delegates.on_show_write_spi()
   return
  J=Y.view.menu_bar.menu_tools.items["ADCs"]
  if evt.Id==J.GetId():
   Y.delegates.on_show_adcs()
   return
  J=Y.view.menu_bar.menu_tools.items["Execute test"]
  if evt.Id==J.GetId():
   Y.delegates.on_test()
   return
  for k,tool in Y.presenter.tools.items():
   J=Y.view.menu_bar.menu_tools.items[k]
   if evt.Id==J.GetId():
    Y.delegates.on_show_tools(tool)
 def __on_image_histogram_scale(Y,evt):
  Y.delegates.on_scale_histogram()
 def __on_write_spi(Y,evt):
  Y.delegates.on_write_spi()
 def __on_update_adc_ts(Y,evt):
  Y.delegates.on_update_adc_ts()
 def __on_update_adc_panels(Y,evt):
  Y.delegates.on_update_adc_panels()
class T:
 def d(Y,E,x):
  Y.delegates=E
  Y.view=x
  Y.config_delegates()
 def l(Y):
  Y.view.panel_values.button_apply.Bind(wx.EVT_BUTTON,Y.on_apply)
  z=Y.view.panel_values.values_widgets.values()
  for D in z:
   D.Bind(wx.EVT_TEXT,Y.on_text_change)
   D.Bind(wx.EVT_TEXT_ENTER,Y.on_apply)
 def o(Y,evt):
  Y.delegates.on_text_change(evt.GetEventObject())
 def I(Y,evt):
  Y.delegates.on_apply()
class B(T):
 def l(Y):
  Y.view.button_apply.Bind(wx.EVT_BUTTON,Y.on_apply)
  z=Y.view.panel_values.values_widgets.values()
  for D in z:
   if v(D,wx.CheckBox):
    D.Bind(wx.EVT_CHECKBOX,Y.__on_check_box)
   elif v(D,wxInt.IntCtrl):
    D.Bind(wx.EVT_TEXT,Y.on_text_change)
    D.Bind(wx.EVT_TEXT_ENTER,Y.on_apply)
 def __on_check_box(Y,evt):
  D=evt.GetEventObject()
  Y.delegates.on_check_box_change(D)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
