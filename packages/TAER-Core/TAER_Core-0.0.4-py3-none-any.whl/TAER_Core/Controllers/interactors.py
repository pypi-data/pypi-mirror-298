import wx
䛖=isinstance
𐠖=wx.CheckBox
ࢣ=wx.EVT_TEXT_ENTER
𐲓=wx.EVT_TEXT
ࢦ=wx.EVT_CHECKBOX
𐭯=wx.ID_FILE9
𰢗=wx.ID_FILE1
𡼬=wx.EVT_MENU_RANGE
ﷲ=wx.EVT_MENU
𐣭=wx.EVT_RADIOBOX
乧=wx.EVT_BUTTON
𩻽=wx.EVT_CLOSE
𢫃=wx.lib
import 𢫃.intctrl as wxInt
class 𐡢:
 def 𐦀(ﭢ,푨,𞠜):
  ﭢ.presenter=푨
  ﭢ.delegates=푨.delegates_main
  ﭢ.view=𞠜
  ﭢ.__config_delegates()
 def __config_delegates(ﭢ):
  ﭢ.view.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.edit_register_device_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.edit_register_chip_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.edit_dac_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.device_info_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.image_histogram_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.serial_control_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.view.adc_control_frame.Bind(𩻽,ﭢ.__on_close)
  ﭢ.__config_control_button_delegates()
  ﭢ.__config_menu_bar_delegates()
  ﭢ.__config_other_delegates()
  ﭢ.__config_adc_delegates()
 def __config_control_button_delegates(ﭢ):
  ﻴ=ﭢ.view.panel_control
  ﻴ.button_start_stop.Bind(乧,ﭢ.__on_start_stop)
  ﻴ.button_capture.Bind(乧,ﭢ.__on_capture)
  ﻴ.button_reset.Bind(乧,ﭢ.__on_reset)
  ﻴ.button_reset_periphery.Bind(乧,ﭢ.__on_reset_periphery)
  ﻴ.button_reset_chip.Bind(乧,ﭢ.__on_reset_chip)
  ﻴ.modes_box.Bind(𐣭,ﭢ.__on_mode_change)
 def __config_menu_bar_delegates(ﭢ):
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_edit,ﭢ.view.menu_bar.menu_edit.item_save_preset,)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_edit,ﭢ.view.menu_bar.menu_edit.item_load_preset,)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_edit,ﭢ.view.menu_bar.menu_edit.item_reg_dev)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_edit,ﭢ.view.menu_bar.menu_edit.item_reg_chip)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_edit,ﭢ.view.menu_bar.menu_edit.item_dac)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_device,ﭢ.view.menu_bar.menu_device.item_program,)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_device,ﭢ.view.menu_bar.menu_device.item_info)
  ﭢ.view.Bind(𡼬,ﭢ.__on_menu_device_file_history,id=𰢗,id2=𐭯,)
  ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_image,ﭢ.view.menu_bar.menu_image.item_histogram,)
  for ﺬ in ﭢ.view.menu_bar.menu_tools.items.values():
   ﭢ.view.Bind(ﷲ,ﭢ.__on_menu_tools,ﺬ)
 def __config_other_delegates(ﭢ):
  𞠜=ﭢ.view.image_histogram_frame
  𞠜.panel_histogram_plot.button_scale.Bind(乧,ﭢ.__on_image_histogram_scale)
  𞠜=ﭢ.view.serial_control_frame
  𞠜.panel_serial_control.btn_write.Bind(乧,ﭢ.__on_write_spi)
 def __config_adc_delegates(ﭢ):
  𞠜=ﭢ.view.adc_control_frame
  𞠜.panel_menu.button_update.Bind(乧,ﭢ.__on_update_adc_ts)
  𐂨=𞠜.panel_menu.enable_widgets
  for 동 in 𐂨.values():
   동.Bind(ࢦ,ﭢ.__on_update_adc_panels)
 def __on_close(ﭢ,evt):
  ﭢ.delegates.on_close(evt.GetEventObject())
 def __on_start_stop(ﭢ,evt):
  ﭢ.delegates.on_start_stop()
 def __on_capture(ﭢ,evt):
  ﭢ.delegates.on_capture()
 def __on_reset(ﭢ,evt):
  ﭢ.delegates.on_reset()
 def __on_reset_periphery(ﭢ,evt):
  ﭢ.delegates.on_reset_periphery()
 def __on_reset_chip(ﭢ,evt):
  ﭢ.delegates.on_reset_chip()
 def __on_mode_change(ﭢ,evt):
  동=evt.GetEventObject()
  𐺀=동.GetSelection()
  ﭢ.delegates.on_mode_change(동.GetItemLabel(𐺀))
 def __on_menu_edit(ﭢ,evt):
  ﺬ=ﭢ.view.menu_bar.menu_edit.item_save_preset
  if evt.GetId()==ﺬ.GetId():
   ﭢ.delegates.on_save_preset()
  ﺬ=ﭢ.view.menu_bar.menu_edit.item_load_preset
  if evt.GetId()==ﺬ.GetId():
   ﭢ.delegates.on_load_preset()
  ﺬ=ﭢ.view.menu_bar.menu_edit.item_reg_dev
  if evt.GetId()==ﺬ.GetId():
   ﭢ.delegates.on_show_registers_device()
  ﺬ=ﭢ.view.menu_bar.menu_edit.item_reg_chip
  if evt.GetId()==ﺬ.GetId():
   ﭢ.delegates.on_show_registers_chip()
  ﺬ=ﭢ.view.menu_bar.menu_edit.item_dac
  if evt.GetId()==ﺬ.GetId():
   ﭢ.delegates.on_show_dacs()
 def __on_menu_device(ﭢ,evt):
  ﺬ=ﭢ.view.menu_bar.menu_device.item_program
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_program()
  ﺬ=ﭢ.view.menu_bar.menu_device.item_info
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_show_device_info()
 def __on_menu_device_file_history(ﭢ,evt):
  𠑰=evt.GetId()-𰢗
  ﭢ.delegates.on_program_recent_file(𠑰)
 def __on_menu_image(ﭢ,evt):
  ﺬ=ﭢ.view.menu_bar.menu_image.item_histogram
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_show_histogram()
 def __on_menu_tools(ﭢ,evt):
  ﺬ=ﭢ.view.menu_bar.menu_tools.items["Write SPI"]
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_show_write_spi()
   return
  ﺬ=ﭢ.view.menu_bar.menu_tools.items["ADCs"]
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_show_adcs()
   return
  ﺬ=ﭢ.view.menu_bar.menu_tools.items["Execute test"]
  if evt.Id==ﺬ.GetId():
   ﭢ.delegates.on_test()
   return
  for 㮷,tool in ﭢ.presenter.tools.items():
   ﺬ=ﭢ.view.menu_bar.menu_tools.items[㮷]
   if evt.Id==ﺬ.GetId():
    ﭢ.delegates.on_show_tools(tool)
 def __on_image_histogram_scale(ﭢ,evt):
  ﭢ.delegates.on_scale_histogram()
 def __on_write_spi(ﭢ,evt):
  ﭢ.delegates.on_write_spi()
 def __on_update_adc_ts(ﭢ,evt):
  ﭢ.delegates.on_update_adc_ts()
 def __on_update_adc_panels(ﭢ,evt):
  ﭢ.delegates.on_update_adc_panels()
class 觃:
 def 𐦀(ﭢ,ﱸ,𞠜):
  ﭢ.delegates=ﱸ
  ﭢ.view=𞠜
  ﭢ.𤩌()
 def 𤩌(ﭢ):
  ﭢ.view.panel_values.button_apply.Bind(乧,ﭢ.𐭑)
  𐿡=ﭢ.view.panel_values.values_widgets.values()
  for 동 in 𐿡:
   동.Bind(𐲓,ﭢ.ﰇ)
   동.Bind(ࢣ,ﭢ.𐭑)
 def ﰇ(ﭢ,evt):
  ﭢ.delegates.on_text_change(evt.GetEventObject())
 def 𐭑(ﭢ,evt):
  ﭢ.delegates.on_apply()
class ڕ(觃):
 def 𤩌(ﭢ):
  ﭢ.view.button_apply.Bind(乧,ﭢ.𐭑)
  𐿡=ﭢ.view.panel_values.values_widgets.values()
  for 동 in 𐿡:
   if 䛖(동,𐠖):
    동.Bind(ࢦ,ﭢ.__on_check_box)
   elif 䛖(동,wxInt.IntCtrl):
    동.Bind(𐲓,ﭢ.ﰇ)
    동.Bind(ࢣ,ﭢ.𐭑)
 def __on_check_box(ﭢ,evt):
  동=evt.GetEventObject()
  ﭢ.delegates.on_check_box_change(동)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
