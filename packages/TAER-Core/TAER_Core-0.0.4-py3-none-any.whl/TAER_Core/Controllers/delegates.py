from os import path
ﯧ=None
𨡰=max
𐂃=min
ﲘ=super
櫞=int
𘞢=path.exists
import wx
𞸖=wx.ID_CANCEL
ﳈ=wx.FD_CHANGE_DIR
𐬚=wx.FD_FILE_MUST_EXIST
𢣠=wx.FD_OPEN
𨶮=wx.FileDialog
from TAER_Core.main_model import MainModel
class 𣐃:
 def __init__(𰸛,𬸸,ﷲ,𐀚:MainModel)->ﯧ:
  𰸛.presenter=𬸸
  𰸛.view=ﷲ
  𰸛.model=𐀚
 def 𡛣(𰸛):
  𰸛.presenter.logger.debug("On start or stop")
  𰸛.presenter.toggle_main_img_thread()
 def ࡦ(𰸛):
  𰸛.presenter.capture()
  𰸛.presenter.logger.info("Start capture.")
 def ߙ(𰸛):
  𰸛.model.device.actions.reset_device()
  𰸛.model.device.actions.reset_fifo()
  𰸛.model.device.actions.reset_ram()
  𰸛.presenter.logger.debug("Reset device.")
 def 𞡤(𰸛):
  𰸛.presenter.logger.debug("Reset periphery.")
  𰸛.model.device.actions.reset_aer()
 def 𐲑(𰸛):
  𰸛.presenter.logger.info("Reset chip.")
  𰸛.model.device.actions.reset_chip()
 def ہ(𰸛,mode):
  𰸛.presenter.set_mode(mode)
 def 𐺰(𰸛):
  if not 𰸛.model.device.is_connected:
   𰸛.presenter.logger.info("Device disconnected")
   𰸛.model.binary_file=""
   𰸛.presenter.stop_main_img_thread()
   𰸛.model.reset_image()
   𰸛.presenter.update_image()
  else:
   𰸛.presenter.logger.info("On connection")
  𰸛.presenter.update_view()
 def 𑐅(𰸛):
  with 𨶮(𰸛.view,"Open bitstream file",wildcard="Bitstream files (*.bit)|*.bit",style=𢣠|𐬚|ﳈ,)as 𞠥:
   if 𞠥.ShowModal()!=𞸖:
    𰸛.model.binary_file=𞠥.GetPath()
    𰸛.model.device.program(𰸛.model.binary_file)
    𰸛.model.read_dev_registers()
    𩡺=𰸛.view.menu_bar.menu_device.program_history
    𩡺.AddFileToHistory(𰸛.model.binary_file)
    𩡺.Save(𰸛.view.menu_bar.menu_device.program_history_config)
    𰸛.view.menu_bar.menu_device.program_history_config.Flush()
 def 𪃸(𰸛,idx):
  𩡺=𰸛.view.menu_bar.menu_device.program_history
  𞠂=𩡺.GetHistoryFile(idx)
  if 𘞢(𞠂):
   𩡺.AddFileToHistory(𞠂)
   𰸛.model.binary_file=𞠂
   𰸛.model.device.program(𞠂)
   𰸛.model.read_dev_registers()
  else:
   𰸛.presenter.logger.error("The file %s doesn't exist.",𞠂)
   𩡺.RemoveFileFromHistory(idx)
  𩡺.Save(𰸛.view.menu_bar.menu_device.program_history_config)
  𰸛.view.menu_bar.menu_device.program_history_config.Flush()
 def 𐡓(𰸛):
  ﷲ=𰸛.view.device_info_frame
  ﷲ.update_info(𰸛.model.device.info)
  ﷲ.open()
 def 𘧯(𰸛):
  𰸛.presenter.save_preset()
 def 𩠘(𰸛):
  𰸛.presenter.load_preset()
 def 봯(𰸛):
  ﷲ=𰸛.view.edit_register_device_frame
  𰸛.model.read_dev_registers()
  ﷲ.open()
 def ﻞ(𰸛):
  ﷲ=𰸛.view.edit_register_chip_frame
  𰸛.model.read_signals()
  ﷲ.open()
 def ﺃ(𰸛):
  ﷲ=𰸛.view.edit_dac_frame
  𰸛.presenter.update_view(ﷲ.GetId())
  ﷲ.open()
 def 坾(𰸛):
  ﷲ=𰸛.view.image_histogram_frame
  ﷲ.open()
 def 𢘠(𰸛):
  ﷲ=𰸛.view.image_histogram_frame
  𨡰,𐂃,𐣭=ﷲ.get_bin_settings()
  𰸛.model.img_histogram.set_settings(𨡰,𐂃,𐣭)
  ﷲ.scale()
  𰸛.presenter.process_img()
  𰸛.presenter.update_image()
 def תּ(𰸛):
  ﷲ=𰸛.view.serial_control_frame
  ﷲ.open()
 def 롟(𰸛):
  ﷲ=𰸛.view.adc_control_frame
  𰸛.presenter.run_adc()
  ﷲ.open()
 def 𐴖(𰸛):
  𰸛.presenter.send_serial_data()
 def 붙(𰸛):
  𰸛.presenter.update_adc_ts()
 def 𤠳(𰸛):
  𰸛.presenter.update_adc_panels()
 def 寺(𰸛,쥍):
  if 쥍.chip_reg_update:
   𰸛.model.read_signals()
  if 쥍.dev_reg_update:
   𰸛.model.read_dev_registers()
  if not 쥍.is_shown():
   쥍.open()
 def 𰋞(𰸛):
  𰸛.presenter.initializer.on_test()
 def 𐳌(𰸛,ﷲ):
  if ﷲ.GetId()==𰸛.view.adc_control_frame.GetId():
   𰸛.presenter.stop_adc()
  if ﷲ.GetId()==𰸛.view.GetId():
   𰸛.presenter.close()
   ﷲ.close()
  else:
   ﷲ.close()
class 𐠅:
 def __init__(𰸛,𬸸,ﷲ,𐀚)->ﯧ:
  𰸛.presenter=𬸸
  𰸛.view=ﷲ
  𰸛.model=𐀚
 def 岰(𰸛,widget):
  𰸛.view.panel_values.on_text_change(widget)
 def ﲤ(𰸛):
  𰸛.presenter.update_model(𰸛.view.GetId())
  𰸛.view.panel_values.to_default_color()
 def 𐳌(𰸛):
  𰸛.view.close()
class ﻂ(𐠅):
 def __init__(𰸛,𬸸,ﷲ,𐀚)->ﯧ:
  ﲘ().__init__(𬸸,ﷲ,𐀚)
 def 𐰥(𰸛,evt_widget):
  𐤀=櫞(evt_widget.GetValue())
  𧎕=𰸛.view.panel_values.values_widgets
  for 𐦯,widget in 𧎕.items():
   if evt_widget.GetId()==widget.GetId():
    𰸛.model.write_signal(𐦯,𐤀)
    break
# Created by pyminifier (https://github.com/liftoff/pyminifier)
