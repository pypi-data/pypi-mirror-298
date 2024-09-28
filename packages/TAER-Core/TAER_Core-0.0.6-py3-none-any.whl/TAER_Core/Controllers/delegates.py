from os import path
d=None
NW=max
NG=min
NJ=super
NH=int
V=path.exists
import wx
b=wx.ID_CANCEL
a=wx.FD_CHANGE_DIR
t=wx.FD_FILE_MUST_EXIST
j=wx.FD_OPEN
s=wx.FileDialog
from TAER_Core.main_model import MainModel
class k:
 def __init__(N,W,G,J:MainModel)->d:
  N.presenter=W
  N.view=G
  N.model=J
 def U(N):
  N.presenter.logger.debug("On start or stop")
  N.presenter.toggle_main_img_thread()
 def r(N):
  N.presenter.capture()
  N.presenter.logger.info("Start capture.")
 def B(N):
  N.model.device.actions.reset_device()
  N.model.device.actions.reset_fifo()
  N.model.device.actions.reset_ram()
  N.presenter.logger.debug("Reset device.")
 def c(N):
  N.presenter.logger.debug("Reset periphery.")
  N.model.device.actions.reset_aer()
 def m(N):
  N.presenter.logger.info("Reset chip.")
  N.model.device.actions.reset_chip()
 def I(N,mode):
  N.presenter.set_mode(mode)
 def M(N):
  if not N.model.device.is_connected:
   N.presenter.logger.info("Device disconnected")
   N.model.binary_file=""
   N.presenter.stop_main_img_thread()
   N.model.reset_image()
   N.presenter.update_image()
  else:
   N.presenter.logger.info("On connection")
  N.presenter.update_view()
 def p(N):
  with s(N.view,"Open bitstream file",wildcard="Bitstream files (*.bit)|*.bit",style=j|t|a,)as y:
   if y.ShowModal()!=b:
    N.model.binary_file=y.GetPath()
    N.model.device.program(N.model.binary_file)
    N.model.read_dev_registers()
    u=N.view.menu_bar.menu_device.program_history
    u.AddFileToHistory(N.model.binary_file)
    u.Save(N.view.menu_bar.menu_device.program_history_config)
    N.view.menu_bar.menu_device.program_history_config.Flush()
 def z(N,idx):
  u=N.view.menu_bar.menu_device.program_history
  v=u.GetHistoryFile(idx)
  if V(v):
   u.AddFileToHistory(v)
   N.model.binary_file=v
   N.model.device.program(v)
   N.model.read_dev_registers()
  else:
   N.presenter.logger.error("The file %s doesn't exist.",v)
   u.RemoveFileFromHistory(idx)
  u.Save(N.view.menu_bar.menu_device.program_history_config)
  N.view.menu_bar.menu_device.program_history_config.Flush()
 def O(N):
  G=N.view.device_info_frame
  G.update_info(N.model.device.info)
  G.open()
 def C(N):
  N.presenter.save_preset()
 def w(N):
  N.presenter.load_preset()
 def h(N):
  G=N.view.edit_register_device_frame
  N.model.read_dev_registers()
  G.open()
 def Y(N):
  G=N.view.edit_register_chip_frame
  N.model.read_signals()
  G.open()
 def q(N):
  G=N.view.edit_dac_frame
  N.presenter.update_view(G.GetId())
  G.open()
 def S(N):
  G=N.view.image_histogram_frame
  G.open()
 def g(N):
  G=N.view.image_histogram_frame
  NW,NG,n=G.get_bin_settings()
  N.model.img_histogram.set_settings(NW,NG,n)
  G.scale()
  N.presenter.process_img()
  N.presenter.update_image()
 def T(N):
  G=N.view.serial_control_frame
  G.open()
 def R(N):
  G=N.view.adc_control_frame
  N.presenter.run_adc()
  G.open()
 def X(N):
  N.presenter.send_serial_data()
 def Q(N):
  N.presenter.update_adc_ts()
 def f(N):
  N.presenter.update_adc_panels()
 def A(N,F):
  if F.chip_reg_update:
   N.model.read_signals()
  if F.dev_reg_update:
   N.model.read_dev_registers()
  if not F.is_shown():
   F.open()
 def o(N):
  N.presenter.initializer.on_test()
 def e(N,G):
  if G.GetId()==N.view.adc_control_frame.GetId():
   N.presenter.stop_adc()
  if G.GetId()==N.view.GetId():
   N.presenter.close()
   G.close()
  else:
   G.close()
class x:
 def __init__(N,W,G,J)->d:
  N.presenter=W
  N.view=G
  N.model=J
 def P(N,widget):
  N.view.panel_values.on_text_change(widget)
 def D(N):
  N.presenter.update_model(N.view.GetId())
  N.view.panel_values.to_default_color()
 def e(N):
  N.view.close()
class K(x):
 def __init__(N,W,G,J)->d:
  NJ().__init__(W,G,J)
 def l(N,evt_widget):
  E=NH(evt_widget.GetValue())
  L=N.view.panel_values.values_widgets
  for i,widget in L.items():
   if evt_widget.GetId()==widget.GetId():
    N.model.write_signal(i,E)
    break
# Created by pyminifier (https://github.com/liftoff/pyminifier)
