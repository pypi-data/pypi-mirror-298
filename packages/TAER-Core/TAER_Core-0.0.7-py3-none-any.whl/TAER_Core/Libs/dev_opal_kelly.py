""" Opal Kelly device class """
iC=False
io=None
iS=property
iE=bool
iv=True
iQ=str
iM=dict
it=int
iT=bytearray
im=min
ig=len
iW=list
iq=pow
iB=super
import logging
import time
import ok
from threading import Lock
class z(ok.FrontPanelManager):
 def __init__(zN):
  ok.FrontPanelManager.__init__(zN)
  zN.__handler=ok.okCFrontPanel()
  zN.vendor_info=ok.okTDeviceInfo()
  zN.info=b()
  zN.lock=zl()
  zN.is_connected=iC
  zN.on_connection_change_callback=io
  zN.logger=logging.getLogger(__name__)
  zN.actions=i(zN,zN.logger)
 @iS
 def v(zN):
  return zN.__handler
 def __get_device_info(zN)->iE:
  zN.vendor_info=ok.okTDeviceInfo()
  if zN.__handler is not io:
   zN.__get_lock__()
   za=zN.__handler.GetDeviceInfo(zN.vendor_info)
   zN.__release_lock__()
   if zN.__handler.NoError!=za:
    zN.logger.info("Unable to retrieve device information.")
    return iC
  zN.info.set_values_from_OK(zN.vendor_info)
  return iv
 def Q(zN):
  zN.StartMonitoring()
 def M(zN):
  zN.StopMonitoring()
 def t(zN,bitstream:iQ):
  zN.config(bitstream)
  zN.initialize()
 def d(zN):
  pass
 def __get_lock__(zN):
  zN.lock.acquire(timeout=5)
 def __release_lock__(zN):
  zN.lock.release()
 def T(zN,bit_stream_path:iQ="")->iE:
  zN.__get_lock__()
  zN.__handler.LoadDefaultPLLConfiguration()
  za=zN.__handler.ConfigureFPGA(bit_stream_path)
  zN.__release_lock__()
  if zN.__handler.NoError!=za:
   zN.logger.error("FPGA configuration failed.")
   return iC
  zN.logger.info("Device %s configuration success.",zN.vendor_info.productName)
  zN.__get_lock__()
  zJ=zN.__handler.IsFrontPanelEnabled()
  zN.__release_lock__()
  if not zJ:
   zN.logger.error("Front Panel isn't enabled.")
   return iC
  time.sleep(1.5)
  if not zN.actions.check_calibration():
   zN.logger.error("Device RAM isn't calibrated.")
   return iC
  zN.actions.reset_device()
  return iv
 def m(zN,zC):
  zN.on_connection_change_callback=zC
 def g(zN):
  if zN.on_connection_change_callback is not io:
   zN.on_connection_change_callback()
 def W(zN,serial:iQ)->io:
  zN.logger.debug("On device %s connected.",serial)
  if zN.is_connected:
   return
  zN.__get_lock__()
  zN.__handler=zN.Open(serial)
  zN.__release_lock__()
  if not zN.__handler:
   zN.logger.error("A device could not be opened.")
  else:
   zo=zN.__get_device_info()
   if zo:
    zN.logger.info("Device %s connected.",zN.vendor_info.productName)
    zN.is_connected=iv
    zN.launch_on_connection_change_callback()
 def q(zN,serial:iQ)->io:
  zN.__get_lock__()
  zS=zN.__handler.IsOpen()
  zN.__release_lock__()
  if not zS:
   zN.logger.debug("On device %s disconnected.",zN.vendor_info.productName)
   del zN.__handler
   zN.__handler=io
   zN.is_connected=iC
   zN.logger.info("Device %s disconnected.",zN.vendor_info.productName)
   zN.launch_on_connection_change_callback()
  else:
   zN.logger.debug("On device %s disconnected.",serial)
class b:
 def __init__(zN)->io:
  zN.vendor=iQ()
  zN.product_name=iQ()
  zN.serial_number=iQ()
  zN.dev_version=iQ()
 def f(zN,zE:ok.okTDeviceInfo):
  zN.vendor="Opal Kelly"
  zN.product_name=iQ(zE.productName)
  zN.serial_number=iQ(zE.serialNumber)
  zN.dev_version=".".join([iQ(zE.deviceMajorVersion),iQ(zE.deviceMinorVersion)])
class i:
 zv=0x01
 zQ=32 
 zM=1024*1024
 def __init__(zN,zt:z,logger=logging.getLogger(__name__))->io:
  zN.device=zt
  zN.links=D()
  zN.logger=zd
 def B(zN,address,zT):
  zN.device.__get_lock__()
  zN.device.interface.WriteRegister(address,zT)
  zN.device.__release_lock__()
 def U(zN,address):
  zN.device.__get_lock__()
  zT=zN.device.interface.ReadRegister(address)
  zN.device.__release_lock__()
  za=zN.device.interface.NoError
  zN.__check_err_code(za,f"Reading register address {address} -> value {value}")
  return zT
 def e(zN,registers):
  zm=ok.okTRegisterEntries()
  for zg in registers.values():
   zW=ok.okTRegisterEntry()
   zW.address=zg.address
   zW.data=zg.value
   zm.append(zW)
  zN.device.__get_lock__()
  zq=zN.device.interface.WriteRegisters(zm)
  zN.device.__release_lock__()
  if zN.device.interface.NoError==zq:
   zN.logger.info("Device register write success.")
  else:
   zN.logger.error("Device register write failed with code %s.",zq)
 def R(zN,registers)->iM:
  zm=ok.okTRegisterEntries()
  for zg in registers.values():
   zW=ok.okTRegisterEntry()
   zW.address=zg.address
   zm.append(zW)
  zN.device.__get_lock__()
  zq=zN.device.interface.ReadRegisters(zm)
  zN.device.__release_lock__()
  if zN.device.interface.NoError==zq:
   zN.logger.info("Device register read success.")
   zf={}
   for zW in zm:
    zf[zW.address]=zW.data
   return zf
  else:
   zN.logger.error("Device register read failed with code %s.",zq)
   return{}
 def I(zN,address,channel,zT):
  zN.__set_wire__(zN.links.win_dac,address,c.DAC_SEL)
  zN.__set_wire__(zN.links.win_dac,zN.DAC_WRITE_MODE,c.DAC_MODE)
  zN.__set_wire__(zN.links.win_dac,channel,c.DAC_CHANNEL)
  zN.__set_wire__(zN.links.win_dac,zT,c.DAC_VALUE)
  zN.__update_wires__()
  zN.__set_trigger__(zN.links.trig_in,S.TRIG_DAC)
 def H(zN,dacs):
  for zB in dacs.values():
   zN.write_dac(zB.address,zB.channel,zB.value)
 def A(zN,address,channel)->it:
  zN.__set_wire__(zN.links.win_adc,address,K.ADC_ID)
  zN.__set_wire__(zN.links.win_adc,channel,K.ADC_CHANNEL)
  zN.__update_wires__()
  zN.__set_trigger__(zN.links.trig_in,S.TRIG_ADC)
  zU=zN.__wait_until(zN.is_adc_done,1)
  if zU:
   ze=zN.__read_wire__(zN.links.wout_adc,a.ADC_DATA)
  else:
   ze=0
  return ze
 def L(zN)->iE:
  zR=zN.__read_trigger__(zN.links.trig_out,E.ADC_DATA_VALID)
  return zR
 def s(zN):
  zN.reset_fifo()
  zN.reset_ram()
  zN.__set_wire__(zN.links.win0,1,O.WRITE_EN_RAM)
  zN.__update_wires__()
  zN.__set_trigger__(zN.links.trig_in,S.START)
 def k(zN):
  zN.__set_trigger__(zN.links.trig_in,S.STOP)
 def x(zN)->iE:
  zR=zN.__read_trigger__(zN.links.trig_out,E.VIDEO_DONE)
  return zR
 def u(zN)->iE:
  zR=zN.__read_trigger__(zN.links.trig_out,E.EVENTS_DONE)
  return zR
 def G(zN):
  zN.__set_wire_as_trigger__(zN.links.win0,O.RESET_CHIP)
  zN.__update_wires__()
 def Y(zN):
  zN.__set_wire_as_trigger__(zN.links.win0,O.RESET_PERIPH)
  zN.__update_wires__()
 def p(zN):
  zN.__set_wire_as_trigger__(zN.links.win0,O.RESET)
  zN.__update_wires__()
 def j(zN):
  zN.__set_wire__(zN.links.win0,0,O.READ_EN_RAM)
  zN.__set_wire__(zN.links.win0,0,O.WRITE_EN_RAM)
  zN.__set_wire_as_trigger__(zN.links.win0,O.RESET_FIFO)
  zN.__update_wires__()
 def r(zN):
  zN.__set_wire_as_trigger__(zN.links.win0,O.RESET_RAM)
  zN.__update_wires__()
 def X(zN):
  zT=zN.__read_wire__(zN.links.wout_calib,N.CALIB)
  if zT==0:
   return iC
  else:
   return iv
 def F(zN,is_enabled):
  if is_enabled:
   zN.__set_wire__(zN.links.win0,1,O.CLK_20M_EN)
  else:
   zN.__set_wire__(zN.links.win0,0,O.CLK_20M_EN)
  zN.__update_wires__()
 def w(zN):
  zI=zN.__read_wire__(zN.links.wout_xy,o.X)
  zH=zN.__read_wire__(zN.links.wout_xy,o.Y)
  return zI,zH
 def zb(zN,zL):
  zN.reset_fifo()
  zN.reset_ram()
  zA=zN.__read_ram_block(zL)
  zN.__set_wire__(zN.links.win0,0,O.READ_EN_RAM)
  zN.__update_wires__()
  return zA
 def zi(zN,zL):
  zA=zN.__read_ram_block(zL)
  zN.__set_trigger__(zN.links.trig_in,S.EVENTS_READ)
  return zA
 def __read_ram_block(zN,zL):
  zN.__set_wire__(zN.links.win0,1,O.READ_EN_RAM)
  zN.__update_wires__()
  zL=(zL//16)*16
  zs=0
  zA=iT()
  while zs<zL:
   zk=im([zN.RAM_READBUF_SIZE,zL])
   zx=zN.__read_block_pipe_out__(zN.links.pipe_out0,zk)
   zA.extend(zx)
   zs=zs+zk
  return zA
 def zD(zN):
  zu=zN.__read_wire__(zN.links.wout_ram_read,J.ADDR_RD)
  zG=zN.__read_wire__(zN.links.wout_ram_write,C.ADDR_WR)
  return zu,zG
 def zP(zN,data_tx):
  zN.__write_serial_fifo(data_tx)
 def zV(zN):
  zY=zN.__read_serial_fifo()
  return zY
 def zO(zN,is_enabled):
  if is_enabled:
   zN.__set_wire__(zN.links.win0,1,O.TEST_TFS_EN)
   zN.__set_wire__(zN.links.win0,1,O.CLK_TFS_EN)
   zN.__update_wires__()
  else:
   zN.__set_wire__(zN.links.win0,0,O.TEST_TFS_EN)
   zN.__set_wire__(zN.links.win0,0,O.CLK_TFS_EN)
   zN.__update_wires__()
 def zh(zN,mode):
  zN.__set_wire__(zN.links.win0,mode,O.MODES)
  zN.__update_wires__()
 def zn(zN,signal,zT):
  if signal==0:
   zN.__set_wire__(zN.links.win0,zT,O.AUX0)
  elif signal==1:
   zN.__set_wire__(zN.links.win0,zT,O.AUX1)
  elif signal==2:
   zN.__set_wire__(zN.links.win0,zT,O.AUX2)
  elif signal==3:
   zN.__set_wire__(zN.links.win0,zT,O.AUX3)
  elif signal==4:
   zN.__set_wire__(zN.links.win0,zT,O.AUX4)
  elif signal==5:
   zN.__set_wire__(zN.links.win0,zT,O.AUX5)
  zN.__update_wires__()
 def zK(zN,switch_bit,zT):
  if switch_bit==0:
   zN.__set_wire__(zN.links.win_pcb,zT,h.BIT0)
  elif switch_bit==1:
   zN.__set_wire__(zN.links.win_pcb,zT,h.BIT1)
  elif switch_bit==2:
   zN.__set_wire__(zN.links.win_pcb,zT,h.BIT2)
  elif switch_bit==3:
   zN.__set_wire__(zN.links.win_pcb,zT,h.BIT3)
  elif switch_bit==4:
   zN.__set_wire__(zN.links.win_pcb,zT,h.BIT4)
  elif switch_bit==5:
   zN.__set_wire__(zN.links.win0,zT,h.BIT5)
  zN.__update_wires__()
 def zc(zN)->it:
  zp=zN.__read_wire__(zN.links.wout_evt_count,y.EVT_COUNT)
  return zp
 def __write_serial_fifo(zN,zA):
  if zA is not io:
   zj=ig(zA) 
   zA.reverse()
   zN.__set_register__(zN.links.reg_spi,zj)
   zN.__set_trigger__(zN.links.trig_in,S.SERIAL_RX_RST_FIFO)
   while zj>0:
    zr=zN.__read_wire__(zN.links.wout0,l.SERIAL_TX_FULL)
    while zr:
     zr=zN.__read_wire__(zN.links.wout0,l.SERIAL_TX_FULL)
     time.sleep(0.01)
    if zj>0:
     zN.__set_wire__(zN.links.win_spi,zA[zj-1],n.BYTE3)
    if zj>1:
     zN.__set_wire__(zN.links.win_spi,zA[zj-2],n.BYTE2)
    if zj>2:
     zN.__set_wire__(zN.links.win_spi,zA[zj-3],n.BYTE1)
    if zj>3:
     zN.__set_wire__(zN.links.win_spi,zA[zj-4],n.BYTE0)
    zN.__update_wires__()
    zN.__set_trigger__(zN.links.trig_in,S.SERIAL_TX_WEN)
    zj=zj-4
   zN.logger.debug(f"{len(data)} bytes sent to the serial driver.")
   time.sleep(0.0005) 
  else:
   zN.logger.error("Serial TX data is None.")
 def __read_serial_fifo(zN):
  zX=iW()
  zF=zN.__read_wire__(zN.links.wout0,l.SERIAL_RX_EMPTY)
  if zF:
   zN.logger.error("No RX data found in serial fifo. Make sure the device is answering or delay is long enough.")
   return io
  else:
   while not zF:
    zN.__set_trigger__(zN.links.trig_in,S.SERIAL_RX_REN)
    zw=zN.__read_wire__(zN.links.wout0,l.SERIAL_RX_BYTE)
    zX.append(zw)
    zF=zN.__read_wire__(zN.links.wout0,l.SERIAL_RX_EMPTY)
   zN.logger.debug(f"{len(data_read)} bytes read from the serial driver.")
   return zX
 def __set_trigger__(zN,address,trigger):
  zN.device.__get_lock__()
  za=zN.device.interface.ActivateTriggerIn(address,trigger.offset)
  zN.device.__release_lock__()
  zN.__check_err_code(za,f"Activate trigger address {address} bit {trigger.offset}")
 def __read_trigger__(zN,address,trigger):
  zN.device.__get_lock__()
  za=zN.device.interface.UpdateTriggerOuts()
  zN.__check_err_code(za,"Update trigger out")
  zR=zN.device.interface.IsTriggered(address,trigger.mask)
  zN.device.__release_lock__()
  return zR
 def __set_wire_as_trigger__(zN,address,wire):
  zN.__set_wire__(address,1,wire)
  zN.__update_wires__()
  zN.__set_wire__(address,0,wire)
  zN.__update_wires__()
 def __read_wire__(zN,address,wire):
  zN.device.__get_lock__()
  za=zN.device.interface.UpdateWireOuts()
  zN.__check_err_code(za,f"Read wire out {address}")
  bz=zN.device.interface.GetWireOutValue(address)
  zN.device.__release_lock__()
  return(bz&wire.mask)>>wire.offset
 def __set_wire__(zN,address,zT,wire):
  zN.device.__get_lock__()
  bi=zT<<wire.offset
  za=zN.device.interface.SetWireInValue(address,bi,wire.mask)
  zN.device.__release_lock__()
  zN.__check_err_code(za,f"Set wire -> bits {format(to_write_value, '#032b')} -> mask {format(wire.mask,'#032b')} in address {address}",)
 def __update_wires__(zN):
  zN.device.__get_lock__()
  za=zN.device.interface.UpdateWireIns()
  zN.device.__release_lock__()
  zN.__check_err_code(za,"Update wire in")
 def __read_block_pipe_out__(zN,address,length):
  bD=iT(length)
  zN.device.__get_lock__()
  za=zN.device.interface.ReadFromBlockPipeOut(address,zN.RAM_BLOCK_SIZE,bD)
  zN.device.__release_lock__()
  if za<0:
   zN.__check_err_code(za,f"Read pipe block with address {address}")
  else:
   zN.logger.debug(f"Query {length} bytes \t Read {err_code} bytes")
  return bD
 def __set_register__(zN,address,zT):
  zN.device.__get_lock__()
  za=zN.device.interface.WriteRegister(address,zT)
  zN.device.__release_lock__()
  zN.__check_err_code(za,f"Writing register address {address} value {value}")
 def __check_err_code(zN,za,msg=""):
  if za!=zN.device.interface.NoError:
   zN.logger.error(msg+f" failed with code({err_code}).")
   zN.logger.error(f"Opal kelly error message: {self.device.interface.GetLastErrorMessage()}")
  else:
   zN.logger.debug(msg+" OK.")
 def __wait_until(zN,somepredicate,zy,period=0.01,*args,**kwargs):
  bP=time.time()+zy
  while time.time()<bP:
   if somepredicate(*args,**kwargs):
    return iv
   time.sleep(period)
  return iC
class D:
 def __init__(zN)->io:
  zN.win0=0x00
  zN.win_spi=0x01
  zN.win_adc=0x02
  zN.win_pcb=0x03
  zN.win_dac=0x04
  zN.reg_spi=0x08
  zN.wout_calib=0x20
  zN.wout0=0x21
  zN.wout_xy=0x22
  zN.wout_adc=0x23
  zN.wout_evt_count=0x27
  zN.wout_ram_read=0x28
  zN.wout_ram_write=0x29
  zN.trig_in=0x41
  zN.trig_out=0x60
  zN.pipe_out0=0xA0
class P:
 def __init__(zN,bO,end=0)->io:
  if bV!=0:
   zN.size=bV-bO+1
  else:
   zN.size=1
  zN.offset=bO
  zN.mask=(iq(2,zN.size)-1)<<bO
class V(P):
 def __init__(zN,bO)->io:
  iB().__init__(bO)
class O:
 bh=P(0)
 bn=P(1)
 bK=P(2)
 bc=P(3)
 bN=P(4)
 bl=P(5)
 ba=P(7)
 by=P(8)
 bJ=P(9)
 bC=P(10)
 bo=P(20)
 bS=P(21)
 bE=P(22)
 bv=P(23)
 bQ=P(24)
 bM=P(25)
 bt=P(26)
 bd=P(27)
 bT=P(29,31)
class h:
 bm=P(0)
 bg=P(1)
 bW=P(2)
 bq=P(3)
 bf=P(4)
 bB=P(5)
 bU=P(6)
class n:
 be=P(0,7)
 bR=P(8,15)
 bI=P(16,23)
 bH=P(24,31)
 bA=P(0,31)
class K:
 bL=P(0,1)
 bs=P(2,3)
class c:
 bk=P(0,11)
 bx=P(12,13)
 bu=P(14,15)
 bG=P(16,17)
class N:
 bY=P(0)
class l:
 bp=P(0,7)
 bj=P(8)
 br=P(10)
 bX=P(9)
class a:
 bF=P(0,11)
class y:
 bw=P(0,31)
class J:
 iz=P(0,31)
class C:
 ib=P(0,31)
class o:
 X=P(0,15)
 Y=P(16,31)
class S:
 iD=V(0)
 iP=V(1)
 iV=V(2)
 iO=V(3)
 ih=V(4)
 iK=V(5)
 ic=V(6)
 iN=V(7)
class E:
 il=V(0)
 ia=V(1)
 iy=V(2)
 iJ=V(3)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
