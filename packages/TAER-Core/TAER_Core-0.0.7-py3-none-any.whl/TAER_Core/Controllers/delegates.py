from os import path
f=None
m=max
B=min
n=super
b=int
import wx
from TAER_Core.main_model import MainModel
class z:
 def __init__(D,c,N,o:MainModel)->f:
  D.presenter=c
  D.view=N
  D.model=o
 def l(D):
  D.presenter.logger.debug("On start or stop")
  D.presenter.toggle_main_img_thread()
 def M(D):
  D.presenter.capture()
  D.presenter.logger.info("Start capture.")
 def U(D):
  D.model.device.actions.reset_device()
  D.model.device.actions.reset_fifo()
  D.model.device.actions.reset_ram()
  D.presenter.logger.debug("Reset device.")
 def K(D):
  D.presenter.logger.debug("Reset periphery.")
  D.model.device.actions.reset_aer()
 def F(D):
  D.presenter.logger.info("Reset chip.")
  D.model.device.actions.reset_chip()
 def P(D,mode):
  D.presenter.set_mode(mode)
 def H(D):
  if not D.model.device.is_connected:
   D.presenter.logger.info("Device disconnected")
   D.model.binary_file=""
   D.presenter.stop_main_img_thread()
   D.model.reset_image()
   D.presenter.update_image()
  else:
   D.presenter.logger.info("On connection")
  D.presenter.update_view()
 def X(D):
  with wx.FileDialog(D.view,"Open bitstream file",wildcard="Bitstream files (*.bit)|*.bit",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST|wx.FD_CHANGE_DIR,)as v:
   if v.ShowModal()!=wx.ID_CANCEL:
    D.model.binary_file=v.GetPath()
    D.model.device.program(D.model.binary_file)
    D.model.read_dev_registers()
    I=D.view.menu_bar.menu_device.program_history
    I.AddFileToHistory(D.model.binary_file)
    I.Save(D.view.menu_bar.menu_device.program_history_config)
    D.view.menu_bar.menu_device.program_history_config.Flush()
 def r(D,idx):
  I=D.view.menu_bar.menu_device.program_history
  A=I.GetHistoryFile(idx)
  if path.exists(A):
   I.AddFileToHistory(A)
   D.model.binary_file=A
   D.model.device.program(A)
   D.model.read_dev_registers()
  else:
   D.presenter.logger.error("The file %s doesn't exist.",A)
   I.RemoveFileFromHistory(idx)
  I.Save(D.view.menu_bar.menu_device.program_history_config)
  D.view.menu_bar.menu_device.program_history_config.Flush()
 def p(D):
  N=D.view.device_info_frame
  N.update_info(D.model.device.info)
  N.open()
 def R(D):
  D.presenter.save_preset()
 def x(D):
  D.presenter.load_preset()
 def G(D):
  N=D.view.edit_register_device_frame
  D.model.read_dev_registers()
  N.open()
 def T(D):
  N=D.view.edit_register_chip_frame
  D.model.read_signals()
  N.open()
 def s(D):
  N=D.view.edit_dac_frame
  D.presenter.update_view(N.GetId())
  N.open()
 def O(D):
  N=D.view.image_histogram_frame
  N.open()
 def C(D):
  N=D.view.image_histogram_frame
  m,B,q=N.get_bin_settings()
  D.model.img_histogram.set_settings(m,B,q)
  N.scale()
  D.presenter.process_img()
  D.presenter.update_image()
 def V(D):
  N=D.view.serial_control_frame
  N.open()
 def E(D):
  N=D.view.adc_control_frame
  D.presenter.run_adc()
  N.open()
 def Y(D):
  D.presenter.send_serial_data()
 def J(D):
  D.presenter.update_adc_ts()
 def g(D):
  D.presenter.update_adc_panels()
 def L(D,h):
  if h.chip_reg_update:
   D.model.read_signals()
  if h.dev_reg_update:
   D.model.read_dev_registers()
  if not h.is_shown():
   h.open()
 def u(D):
  D.presenter.initializer.on_test()
 def t(D,N):
  if N.GetId()==D.view.adc_control_frame.GetId():
   D.presenter.stop_adc()
  if N.GetId()==D.view.GetId():
   D.presenter.close()
   N.close()
  else:
   N.close()
class j:
 def __init__(D,c,N,o)->f:
  D.presenter=c
  D.view=N
  D.model=o
 def i(D,widget):
  D.view.panel_values.on_text_change(widget)
 def e(D):
  D.presenter.update_model(D.view.GetId())
  D.view.panel_values.to_default_color()
 def t(D):
  D.view.close()
class a(j):
 def __init__(D,c,N,o)->f:
  n().__init__(c,N,o)
 def S(D,evt_widget):
  w=b(evt_widget.GetValue())
  d=D.view.panel_values.values_widgets
  for k,widget in d.items():
   if evt_widget.GetId()==widget.GetId():
    D.model.write_signal(k,w)
    break
# Created by pyminifier (https://github.com/liftoff/pyminifier)
