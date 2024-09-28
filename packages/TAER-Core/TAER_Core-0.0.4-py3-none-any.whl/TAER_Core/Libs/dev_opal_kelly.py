""" Opal Kelly device class """
𐴖=False
셰=None
ࡁ=property
𞡇=bool
𤘞=True
䂉=str
𮂄=dict
ݒ=int
𰅾=bytearray
ﳝ=min
𫽮=len
𞸟=list
𘔏=pow
𐫜=super
import logging
錅=logging.getLogger
import time
𢻎=time.time
ﶕ=time.sleep
import ok
ﱼ=ok.okTRegisterEntry
𥖺=ok.okTRegisterEntries
漎=ok.okTDeviceInfo
𰍫=ok.okCFrontPanel
𫷎=ok.FrontPanelManager
from threading import Lock
class ﲟ(𫷎):
 def __init__(𞤯):
  𫷎.__init__(𞤯)
  𞤯.__handler=𰍫()
  𞤯.vendor_info=漎()
  𞤯.info=팢()
  𞤯.lock=𭅣()
  𞤯.is_connected=𐴖
  𞤯.on_connection_change_callback=셰
  𞤯.logger=錅(__name__)
  𞤯.actions=𐿵(𞤯,𞤯.logger)
 @ࡁ
 def 𗊾(𞤯):
  return 𞤯.__handler
 def __get_device_info(𞤯)->𞡇:
  𞤯.vendor_info=漎()
  if 𞤯.__handler is not 셰:
   𞤯.__get_lock__()
   𐴚=𞤯.__handler.GetDeviceInfo(𞤯.vendor_info)
   𞤯.__release_lock__()
   if 𞤯.__handler.NoError!=𐴚:
    𞤯.logger.info("Unable to retrieve device information.")
    return 𐴖
  𞤯.info.set_values_from_OK(𞤯.vendor_info)
  return 𤘞
 def 畕(𞤯):
  𞤯.StartMonitoring()
 def ᚤ(𞤯):
  𞤯.StopMonitoring()
 def 𱄿(𞤯,bitstream:䂉):
  𞤯.𤬴(bitstream)
  𞤯.ﰤ()
 def ﰤ(𞤯):
  pass
 def __get_lock__(𞤯):
  𞤯.lock.acquire(timeout=5)
 def __release_lock__(𞤯):
  𞤯.lock.release()
 def 𤬴(𞤯,bit_stream_path:䂉="")->𞡇:
  𞤯.__get_lock__()
  𞤯.__handler.LoadDefaultPLLConfiguration()
  𐴚=𞤯.__handler.ConfigureFPGA(bit_stream_path)
  𞤯.__release_lock__()
  if 𞤯.__handler.NoError!=𐴚:
   𞤯.logger.error("FPGA configuration failed.")
   return 𐴖
  𞤯.logger.info("Device %s configuration success.",𞤯.vendor_info.productName)
  𞤯.__get_lock__()
  䜹=𞤯.__handler.IsFrontPanelEnabled()
  𞤯.__release_lock__()
  if not 䜹:
   𞤯.logger.error("Front Panel isn't enabled.")
   return 𐴖
  ﶕ(1.5)
  if not 𞤯.actions.check_calibration():
   𞤯.logger.error("Device RAM isn't calibrated.")
   return 𐴖
  𞤯.actions.reset_device()
  return 𤘞
 def 𗝼(𞤯,ﴭ):
  𞤯.on_connection_change_callback=ﴭ
 def ޠ(𞤯):
  if 𞤯.on_connection_change_callback is not 셰:
   𞤯.on_connection_change_callback()
 def 𤂣(𞤯,serial:䂉)->셰:
  𞤯.logger.debug("On device %s connected.",serial)
  if 𞤯.is_connected:
   return
  𞤯.__get_lock__()
  𞤯.__handler=𞤯.Open(serial)
  𞤯.__release_lock__()
  if not 𞤯.__handler:
   𞤯.logger.error("A device could not be opened.")
  else:
   ﴗ=𞤯.__get_device_info()
   if ﴗ:
    𞤯.logger.info("Device %s connected.",𞤯.vendor_info.productName)
    𞤯.is_connected=𤘞
    𞤯.ޠ()
 def 𘢯(𞤯,serial:䂉)->셰:
  𞤯.__get_lock__()
  ﭨ=𞤯.__handler.IsOpen()
  𞤯.__release_lock__()
  if not ﭨ:
   𞤯.logger.debug("On device %s disconnected.",𞤯.vendor_info.productName)
   del 𞤯.__handler
   𞤯.__handler=셰
   𞤯.is_connected=𐴖
   𞤯.logger.info("Device %s disconnected.",𞤯.vendor_info.productName)
   𞤯.ޠ()
  else:
   𞤯.logger.debug("On device %s disconnected.",serial)
class 팢:
 def __init__(𞤯)->셰:
  𞤯.vendor=䂉()
  𞤯.product_name=䂉()
  𞤯.serial_number=䂉()
  𞤯.dev_version=䂉()
 def 𡌶(𞤯,ﲾ:漎):
  𞤯.vendor="Opal Kelly"
  𞤯.product_name=䂉(ﲾ.productName)
  𞤯.serial_number=䂉(ﲾ.serialNumber)
  𞤯.dev_version=".".join([䂉(ﲾ.deviceMajorVersion),䂉(ﲾ.deviceMinorVersion)])
class 𐿵:
 𐼒=0x01
 賑=32 
 ﳨ=1024*1024
 def __init__(𞤯,𞹋:ﲟ,logger=錅(__name__))->셰:
  𞤯.device=𞹋
  𞤯.links=ﶧ()
  𞤯.logger=𐮐
 def 𐡂(𞤯,address,穿):
  𞤯.device.__get_lock__()
  𞤯.device.interface.WriteRegister(address,穿)
  𞤯.device.__release_lock__()
 def 𥁌(𞤯,address):
  𞤯.device.__get_lock__()
  穿=𞤯.device.interface.ReadRegister(address)
  𞤯.device.__release_lock__()
  𐴚=𞤯.device.interface.NoError
  𞤯.__check_err_code(𐴚,f"Reading register address {address} -> value {value}")
  return 穿
 def 𞢱(𞤯,registers):
  𨍰=𥖺()
  for ﴭ in registers.values():
   𐺈=ﱼ()
   𐺈.address=ﴭ.address
   𐺈.data=ﴭ.value
   𨍰.append(𐺈)
  𞤯.device.__get_lock__()
  𪨀=𞤯.device.interface.WriteRegisters(𨍰)
  𞤯.device.__release_lock__()
  if 𞤯.device.interface.NoError==𪨀:
   𞤯.logger.info("Device register write success.")
  else:
   𞤯.logger.error("Device register write failed with code %s.",𪨀)
 def ﴇ(𞤯,registers)->𮂄:
  𨍰=𥖺()
  for ﴭ in registers.values():
   𐺈=ﱼ()
   𐺈.address=ﴭ.address
   𨍰.append(𐺈)
  𞤯.device.__get_lock__()
  𪨀=𞤯.device.interface.ReadRegisters(𨍰)
  𞤯.device.__release_lock__()
  if 𞤯.device.interface.NoError==𪨀:
   𞤯.logger.info("Device register read success.")
   𐳥={}
   for 𐺈 in 𨍰:
    𐳥[𐺈.address]=𐺈.data
   return 𐳥
  else:
   𞤯.logger.error("Device register read failed with code %s.",𪨀)
   return{}
 def 𐲫(𞤯,address,channel,穿):
  𞤯.__set_wire__(𞤯.links.win_dac,address,𣈵.DAC_SEL)
  𞤯.__set_wire__(𞤯.links.win_dac,𞤯.DAC_WRITE_MODE,𣈵.DAC_MODE)
  𞤯.__set_wire__(𞤯.links.win_dac,channel,𣈵.DAC_CHANNEL)
  𞤯.__set_wire__(𞤯.links.win_dac,穿,𣈵.DAC_VALUE)
  𞤯.__update_wires__()
  𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.TRIG_DAC)
 def 𐦡(𞤯,dacs):
  for 흣 in dacs.values():
   𞤯.𐲫(흣.address,흣.channel,흣.value)
 def 𤄪(𞤯,address,channel)->ݒ:
  𞤯.__set_wire__(𞤯.links.win_adc,address,ﶨ.ADC_ID)
  𞤯.__set_wire__(𞤯.links.win_adc,channel,ﶨ.ADC_CHANNEL)
  𞤯.__update_wires__()
  𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.TRIG_ADC)
  朌=𞤯.__wait_until(𞤯.𧰯,1)
  if 朌:
   𐬉=𞤯.__read_wire__(𞤯.links.wout_adc,𣓤.ADC_DATA)
  else:
   𐬉=0
  return 𐬉
 def 𧰯(𞤯)->𞡇:
  𐳣=𞤯.__read_trigger__(𞤯.links.trig_out,𬩱.ADC_DATA_VALID)
  return 𐳣
 def 𦚄(𞤯):
  𞤯.𡎟()
  𞤯.𑠚()
  𞤯.__set_wire__(𞤯.links.win0,1,𞹋.WRITE_EN_RAM)
  𞤯.__update_wires__()
  𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.START)
 def ﰠ(𞤯):
  𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.STOP)
 def ힳ(𞤯)->𞡇:
  𐳣=𞤯.__read_trigger__(𞤯.links.trig_out,𬩱.VIDEO_DONE)
  return 𐳣
 def בֿ(𞤯)->𞡇:
  𐳣=𞤯.__read_trigger__(𞤯.links.trig_out,𬩱.EVENTS_DONE)
  return 𐳣
 def 𐪖(𞤯):
  𞤯.__set_wire_as_trigger__(𞤯.links.win0,𞹋.RESET_CHIP)
  𞤯.__update_wires__()
 def 𞢠(𞤯):
  𞤯.__set_wire_as_trigger__(𞤯.links.win0,𞹋.RESET_PERIPH)
  𞤯.__update_wires__()
 def 𞺄(𞤯):
  𞤯.__set_wire_as_trigger__(𞤯.links.win0,𞹋.RESET)
  𞤯.__update_wires__()
 def 𡎟(𞤯):
  𞤯.__set_wire__(𞤯.links.win0,0,𞹋.READ_EN_RAM)
  𞤯.__set_wire__(𞤯.links.win0,0,𞹋.WRITE_EN_RAM)
  𞤯.__set_wire_as_trigger__(𞤯.links.win0,𞹋.RESET_FIFO)
  𞤯.__update_wires__()
 def 𑠚(𞤯):
  𞤯.__set_wire_as_trigger__(𞤯.links.win0,𞹋.RESET_RAM)
  𞤯.__update_wires__()
 def 𐤧(𞤯):
  穿=𞤯.__read_wire__(𞤯.links.wout_calib,化.CALIB)
  if 穿==0:
   return 𐴖
  else:
   return 𤘞
 def 鐞(𞤯,is_enabled):
  if is_enabled:
   𞤯.__set_wire__(𞤯.links.win0,1,𞹋.CLK_20M_EN)
  else:
   𞤯.__set_wire__(𞤯.links.win0,0,𞹋.CLK_20M_EN)
  𞤯.__update_wires__()
 def 𐦩(𞤯):
  쑸=𞤯.__read_wire__(𞤯.links.wout_xy,ৱ.X)
  刃=𞤯.__read_wire__(𞤯.links.wout_xy,ৱ.Y)
  return 쑸,刃
 def 䤫(𞤯,ﶦ):
  𞤯.𡎟()
  𞤯.𑠚()
  ﴽ=𞤯.__read_ram_block(ﶦ)
  𞤯.__set_wire__(𞤯.links.win0,0,𞹋.READ_EN_RAM)
  𞤯.__update_wires__()
  return ﴽ
 def 𠯿(𞤯,ﶦ):
  ﴽ=𞤯.__read_ram_block(ﶦ)
  𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.EVENTS_READ)
  return ﴽ
 def __read_ram_block(𞤯,ﶦ):
  𞤯.__set_wire__(𞤯.links.win0,1,𞹋.READ_EN_RAM)
  𞤯.__update_wires__()
  ﶦ=(ﶦ//16)*16
  땼=0
  ﴽ=𰅾()
  while 땼<ﶦ:
   𐢂=ﳝ([𞤯.RAM_READBUF_SIZE,ﶦ])
   𐦢=𞤯.__read_block_pipe_out__(𞤯.links.pipe_out0,𐢂)
   ﴽ.extend(𐦢)
   땼=땼+𐢂
  return ﴽ
 def ر(𞤯):
  ڼ=𞤯.__read_wire__(𞤯.links.wout_ram_read,ﯰ.ADDR_RD)
  𮧶=𞤯.__read_wire__(𞤯.links.wout_ram_write,𠜗.ADDR_WR)
  return ڼ,𮧶
 def 秲(𞤯,data_tx):
  𞤯.__write_serial_fifo(data_tx)
 def 𣪖(𞤯):
  𣖚=𞤯.__read_serial_fifo()
  return 𣖚
 def 쇣(𞤯,is_enabled):
  if is_enabled:
   𞤯.__set_wire__(𞤯.links.win0,1,𞹋.TEST_TFS_EN)
   𞤯.__set_wire__(𞤯.links.win0,1,𞹋.CLK_TFS_EN)
   𞤯.__update_wires__()
  else:
   𞤯.__set_wire__(𞤯.links.win0,0,𞹋.TEST_TFS_EN)
   𞤯.__set_wire__(𞤯.links.win0,0,𞹋.CLK_TFS_EN)
   𞤯.__update_wires__()
 def 𨌰(𞤯,mode):
  𞤯.__set_wire__(𞤯.links.win0,mode,𞹋.MODES)
  𞤯.__update_wires__()
 def 𪡬(𞤯,signal,穿):
  if signal==0:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX0)
  elif signal==1:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX1)
  elif signal==2:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX2)
  elif signal==3:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX3)
  elif signal==4:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX4)
  elif signal==5:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞹋.AUX5)
  𞤯.__update_wires__()
 def ၑ(𞤯,switch_bit,穿):
  if switch_bit==0:
   𞤯.__set_wire__(𞤯.links.win_pcb,穿,𞤟.BIT0)
  elif switch_bit==1:
   𞤯.__set_wire__(𞤯.links.win_pcb,穿,𞤟.BIT1)
  elif switch_bit==2:
   𞤯.__set_wire__(𞤯.links.win_pcb,穿,𞤟.BIT2)
  elif switch_bit==3:
   𞤯.__set_wire__(𞤯.links.win_pcb,穿,𞤟.BIT3)
  elif switch_bit==4:
   𞤯.__set_wire__(𞤯.links.win_pcb,穿,𞤟.BIT4)
  elif switch_bit==5:
   𞤯.__set_wire__(𞤯.links.win0,穿,𞤟.BIT5)
  𞤯.__update_wires__()
 def 𐣨(𞤯)->ݒ:
  馳=𞤯.__read_wire__(𞤯.links.wout_evt_count,ﯞ.EVT_COUNT)
  return 馳
 def __write_serial_fifo(𞤯,ﴽ):
  if ﴽ is not 셰:
   綩=𫽮(ﴽ) 
   ﴽ.reverse()
   𞤯.__set_register__(𞤯.links.reg_spi,綩)
   𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.SERIAL_RX_RST_FIFO)
   while 綩>0:
    ᚯ=𞤯.__read_wire__(𞤯.links.wout0,𐺏.SERIAL_TX_FULL)
    while ᚯ:
     ᚯ=𞤯.__read_wire__(𞤯.links.wout0,𐺏.SERIAL_TX_FULL)
     ﶕ(0.01)
    if 綩>0:
     𞤯.__set_wire__(𞤯.links.win_spi,ﴽ[綩-1],𞸕.BYTE3)
    if 綩>1:
     𞤯.__set_wire__(𞤯.links.win_spi,ﴽ[綩-2],𞸕.BYTE2)
    if 綩>2:
     𞤯.__set_wire__(𞤯.links.win_spi,ﴽ[綩-3],𞸕.BYTE1)
    if 綩>3:
     𞤯.__set_wire__(𞤯.links.win_spi,ﴽ[綩-4],𞸕.BYTE0)
    𞤯.__update_wires__()
    𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.SERIAL_TX_WEN)
    綩=綩-4
   𞤯.logger.debug(f"{len(data)} bytes sent to the serial driver.")
   ﶕ(0.0005) 
  else:
   𞤯.logger.error("Serial TX data is None.")
 def __read_serial_fifo(𞤯):
  ﲕ=𞸟()
  ﲲ=𞤯.__read_wire__(𞤯.links.wout0,𐺏.SERIAL_RX_EMPTY)
  if ﲲ:
   𞤯.logger.error("No RX data found in serial fifo. Make sure the device is answering or delay is long enough.")
   return 셰
  else:
   while not ﲲ:
    𞤯.__set_trigger__(𞤯.links.trig_in,ﺍ.SERIAL_RX_REN)
    곟=𞤯.__read_wire__(𞤯.links.wout0,𐺏.SERIAL_RX_BYTE)
    ﲕ.append(곟)
    ﲲ=𞤯.__read_wire__(𞤯.links.wout0,𐺏.SERIAL_RX_EMPTY)
   𞤯.logger.debug(f"{len(data_read)} bytes read from the serial driver.")
   return ﲕ
 def __set_trigger__(𞤯,address,trigger):
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.ActivateTriggerIn(address,trigger.offset)
  𞤯.device.__release_lock__()
  𞤯.__check_err_code(𐴚,f"Activate trigger address {address} bit {trigger.offset}")
 def __read_trigger__(𞤯,address,trigger):
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.UpdateTriggerOuts()
  𞤯.__check_err_code(𐴚,"Update trigger out")
  𐳣=𞤯.device.interface.IsTriggered(address,trigger.mask)
  𞤯.device.__release_lock__()
  return 𐳣
 def __set_wire_as_trigger__(𞤯,address,wire):
  𞤯.__set_wire__(address,1,wire)
  𞤯.__update_wires__()
  𞤯.__set_wire__(address,0,wire)
  𞤯.__update_wires__()
 def __read_wire__(𞤯,address,wire):
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.UpdateWireOuts()
  𞤯.__check_err_code(𐴚,f"Read wire out {address}")
  𐿥=𞤯.device.interface.GetWireOutValue(address)
  𞤯.device.__release_lock__()
  return(𐿥&wire.mask)>>wire.offset
 def __set_wire__(𞤯,address,穿,wire):
  𞤯.device.__get_lock__()
  𐨠=穿<<wire.offset
  𐴚=𞤯.device.interface.SetWireInValue(address,𐨠,wire.mask)
  𞤯.device.__release_lock__()
  𞤯.__check_err_code(𐴚,f"Set wire -> bits {format(to_write_value, '#032b')} -> mask {format(wire.mask,'#032b')} in address {address}",)
 def __update_wires__(𞤯):
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.UpdateWireIns()
  𞤯.device.__release_lock__()
  𞤯.__check_err_code(𐴚,"Update wire in")
 def __read_block_pipe_out__(𞤯,address,length):
  ࢣ=𰅾(length)
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.ReadFromBlockPipeOut(address,𞤯.RAM_BLOCK_SIZE,ࢣ)
  𞤯.device.__release_lock__()
  if 𐴚<0:
   𞤯.__check_err_code(𐴚,f"Read pipe block with address {address}")
  else:
   𞤯.logger.debug(f"Query {length} bytes \t Read {err_code} bytes")
  return ࢣ
 def __set_register__(𞤯,address,穿):
  𞤯.device.__get_lock__()
  𐴚=𞤯.device.interface.WriteRegister(address,穿)
  𞤯.device.__release_lock__()
  𞤯.__check_err_code(𐴚,f"Writing register address {address} value {value}")
 def __check_err_code(𞤯,𐴚,msg=""):
  if 𐴚!=𞤯.device.interface.NoError:
   𞤯.logger.error(msg+f" failed with code({err_code}).")
   𞤯.logger.error(f"Opal kelly error message: {self.device.interface.GetLastErrorMessage()}")
  else:
   𞤯.logger.debug(msg+" OK.")
 def __wait_until(𞤯,somepredicate,ݡ,period=0.01,*args,**kwargs):
  𭴯=𢻎()+ݡ
  while 𢻎()<𭴯:
   if somepredicate(*args,**kwargs):
    return 𤘞
   ﶕ(period)
  return 𐴖
class ﶧ:
 def __init__(𞤯)->셰:
  𞤯.win0=0x00
  𞤯.win_spi=0x01
  𞤯.win_adc=0x02
  𞤯.win_pcb=0x03
  𞤯.win_dac=0x04
  𞤯.reg_spi=0x08
  𞤯.wout_calib=0x20
  𞤯.wout0=0x21
  𞤯.wout_xy=0x22
  𞤯.wout_adc=0x23
  𞤯.wout_evt_count=0x27
  𞤯.wout_ram_read=0x28
  𞤯.wout_ram_write=0x29
  𞤯.trig_in=0x41
  𞤯.trig_out=0x60
  𞤯.pipe_out0=0xA0
class ﮮ:
 def __init__(𞤯,𧝧,end=0)->셰:
  if 𐦋!=0:
   𞤯.size=𐦋-𧝧+1
  else:
   𞤯.size=1
  𞤯.offset=𧝧
  𞤯.mask=(𘔏(2,𞤯.size)-1)<<𧝧
class 𣕑(ﮮ):
 def __init__(𞤯,𧝧)->셰:
  𐫜().__init__(𧝧)
class 𞹋:
 ﲻ=ﮮ(0)
 𦷶=ﮮ(1)
 𭌪=ﮮ(2)
 שׂ=ﮮ(3)
 𐤮=ﮮ(4)
 𠵜=ﮮ(5)
 喬=ﮮ(7)
 𬑱=ﮮ(8)
 𖡹=ﮮ(9)
 蓀=ﮮ(10)
 ﵧ=ﮮ(20)
 儧=ﮮ(21)
 ﵑ=ﮮ(22)
 𘱟=ﮮ(23)
 检=ﮮ(24)
 𐤳=ﮮ(25)
 쎋=ﮮ(26)
 𣷋=ﮮ(27)
 ࢦ=ﮮ(29,31)
class 𞤟:
 𫵼=ﮮ(0)
 鑛=ﮮ(1)
 㪟=ﮮ(2)
 𤇀=ﮮ(3)
 北=ﮮ(4)
 榅=ﮮ(5)
 ﹷ=ﮮ(6)
class 𞸕:
 𞤾=ﮮ(0,7)
 ﳻ=ﮮ(8,15)
 𐢝=ﮮ(16,23)
 廘=ﮮ(24,31)
 𓈭=ﮮ(0,31)
class ﶨ:
 ۈ=ﮮ(0,1)
 쉀=ﮮ(2,3)
class 𣈵:
 𡇱=ﮮ(0,11)
 ޚ=ﮮ(12,13)
 𥵻=ﮮ(14,15)
 ﻀ=ﮮ(16,17)
class 化:
 ﶼ=ﮮ(0)
class 𐺏:
 𐬖=ﮮ(0,7)
 𘁏=ﮮ(8)
 𐽅=ﮮ(10)
 𩞤=ﮮ(9)
class 𣓤:
 𞤕=ﮮ(0,11)
class ﯞ:
 ﹸ=ﮮ(0,31)
class ﯰ:
 獸=ﮮ(0,31)
class 𠜗:
 ﱮ=ﮮ(0,31)
class ৱ:
 𐺅=ﮮ(0,15)
 ﶒ=ﮮ(16,31)
class ﺍ:
 𞠫=𣕑(0)
 ؽ=𣕑(1)
 ﮚ=𣕑(2)
 𰼿=𣕑(3)
 ﳅ=𣕑(4)
 𠄣=𣕑(5)
 ﴳ=𣕑(6)
 塗=𣕑(7)
class 𬩱:
 𐳣=𣕑(0)
 ۅ=𣕑(1)
 𞸭=𣕑(2)
 킚=𣕑(3)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
