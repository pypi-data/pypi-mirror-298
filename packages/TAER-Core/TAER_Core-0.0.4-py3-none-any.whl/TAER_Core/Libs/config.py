import yaml
ﷻ=type
𐳢=dict
ﮯ=setattr
𥴓=None
𮭙=str
𞠜=open
𑈔=yaml.safe_load
from os import path
ގ=path.exists
class 𐼆:
 def __init__(ࢥ,my_dict:"dict[str, object]"):
  for 𐭁 in my_dict:
   if ﷻ(my_dict[𐭁])is 𐳢:
    ﮯ(ࢥ,𐭁,𐼆(my_dict[𐭁]))
   else:
    ﮯ(ࢥ,𐭁,my_dict[𐭁])
class ࠅ:
 𱂪=""
 def __init__(ࢥ,config_path=𥴓):
  if 𤳦 is 𥴓:
   if ގ(ࢥ.CONFIG_PATH):
    ࢥ.value=ࢥ.__load_config(ࢥ.CONFIG_PATH)
  else:
   if ގ(𤳦):
    ࢥ.value=ࢥ.__load_config(𤳦)
 def __load_config(ࢥ,file_path:𮭙):
  with 𞠜(file_path,"r")as f:
   return 𑈔(f)
class ﭡ:
 def __init__(ࢥ):
  燛=ࠅ()
  𐼆.__init__(ࢥ,燛.value["VIEW"])
class 𰼄:
 def __init__(ࢥ):
  燛=ࠅ()
  𐼆.__init__(ࢥ,燛.value["MODEL"])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
