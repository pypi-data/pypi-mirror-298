from os import path
g=None
Oi=max
OC=min
OB=super
ON=int
E=path.exists
import wx
R=wx.ID_CANCEL
x=wx.FD_CHANGE_DIR
q=wx.FD_FILE_MUST_EXIST
l=wx.FD_OPEN
M=wx.FileDialog
from TAER_Core.main_model import MainModel
class W:
 def __init__(O,i,C,B:MainModel)->g:
  O.presenter=i
  O.view=C
  O.model=B
 def J(O):
  O.presenter.logger.debug("On start or stop")
  O.presenter.toggle_main_img_thread()
 def t(O):
  O.presenter.capture()
  O.presenter.logger.info("Start capture.")
 def d(O):
  O.model.device.actions.reset_device()
  O.model.device.actions.reset_fifo()
  O.model.device.actions.reset_ram()
  O.presenter.logger.debug("Reset device.")
 def j(O):
  O.presenter.logger.debug("Reset periphery.")
  O.model.device.actions.reset_aer()
 def e(O):
  O.presenter.logger.info("Reset chip.")
  O.model.device.actions.reset_chip()
 def c(O,mode):
  O.presenter.set_mode(mode)
 def n(O):
  if not O.model.device.is_connected:
   O.presenter.logger.info("Device disconnected")
   O.model.binary_file=""
   O.presenter.stop_main_img_thread()
   O.model.reset_image()
   O.presenter.update_image()
  else:
   O.presenter.logger.info("On connection")
  O.presenter.update_view()
 def F(O):
  with M(O.view,"Open bitstream file",wildcard="Bitstream files (*.bit)|*.bit",style=l|q|x,)as U:
   if U.ShowModal()!=R:
    O.model.binary_file=U.GetPath()
    O.model.device.program(O.model.binary_file)
    O.model.read_dev_registers()
    Y=O.view.menu_bar.menu_device.program_history
    Y.AddFileToHistory(O.model.binary_file)
    Y.Save(O.view.menu_bar.menu_device.program_history_config)
    O.view.menu_bar.menu_device.program_history_config.Flush()
 def k(O,idx):
  Y=O.view.menu_bar.menu_device.program_history
  V=Y.GetHistoryFile(idx)
  if E(V):
   Y.AddFileToHistory(V)
   O.model.binary_file=V
   O.model.device.program(V)
   O.model.read_dev_registers()
  else:
   O.presenter.logger.error("The file %s doesn't exist.",V)
   Y.RemoveFileFromHistory(idx)
  Y.Save(O.view.menu_bar.menu_device.program_history_config)
  O.view.menu_bar.menu_device.program_history_config.Flush()
 def o(O):
  C=O.view.device_info_frame
  C.update_info(O.model.device.info)
  C.open()
 def f(O):
  O.presenter.save_preset()
 def u(O):
  O.presenter.load_preset()
 def D(O):
  C=O.view.edit_register_device_frame
  O.model.read_dev_registers()
  C.open()
 def v(O):
  C=O.view.edit_register_chip_frame
  O.model.read_signals()
  C.open()
 def A(O):
  C=O.view.edit_dac_frame
  O.presenter.update_view(C.GetId())
  C.open()
 def p(O):
  C=O.view.image_histogram_frame
  C.open()
 def Q(O):
  C=O.view.image_histogram_frame
  Oi,OC,H=C.get_bin_settings()
  O.model.img_histogram.set_settings(Oi,OC,H)
  C.scale()
  O.presenter.process_img()
  O.presenter.update_image()
 def z(O):
  C=O.view.serial_control_frame
  C.open()
 def s(O):
  C=O.view.adc_control_frame
  O.presenter.run_adc()
  C.open()
 def y(O):
  O.presenter.send_serial_data()
 def I(O):
  O.presenter.update_adc_ts()
 def r(O):
  O.presenter.update_adc_panels()
 def X(O,m):
  if m.chip_reg_update:
   O.model.read_signals()
  if m.dev_reg_update:
   O.model.read_dev_registers()
  if not m.is_shown():
   m.open()
 def h(O):
  O.presenter.initializer.on_test()
 def a(O,C):
  if C.GetId()==O.view.adc_control_frame.GetId():
   O.presenter.stop_adc()
  if C.GetId()==O.view.GetId():
   O.presenter.close()
   C.close()
  else:
   C.close()
class S:
 def __init__(O,i,C,B)->g:
  O.presenter=i
  O.view=C
  O.model=B
 def K(O,widget):
  O.view.panel_values.on_text_change(widget)
 def P(O):
  O.presenter.update_model(O.view.GetId())
  O.view.panel_values.to_default_color()
 def a(O):
  O.view.close()
class T(S):
 def __init__(O,i,C,B)->g:
  OB().__init__(i,C,B)
 def b(O,evt_widget):
  G=ON(evt_widget.GetValue())
  w=O.view.panel_values.values_widgets
  for L,widget in w.items():
   if evt_widget.GetId()==widget.GetId():
    O.model.write_signal(L,G)
    break
# Created by pyminifier (https://github.com/liftoff/pyminifier)
