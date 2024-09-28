import yaml
G=type
E=dict
b=setattr
V=None
v=str
A=open
C=yaml.safe_load
from os import path
u=path.exists
class f:
 def __init__(o,my_dict:"dict[str, object]"):
  for d in my_dict:
   if G(my_dict[d])is E:
    b(o,d,f(my_dict[d]))
   else:
    b(o,d,my_dict[d])
class e:
 N=""
 def __init__(o,config_path=V):
  if p is V:
   if u(o.CONFIG_PATH):
    o.value=o.__load_config(o.CONFIG_PATH)
  else:
   if u(p):
    o.value=o.__load_config(p)
 def __load_config(o,file_path:v):
  with A(file_path,"r")as f:
   return C(f)
class q:
 def __init__(o):
  M=e()
  f.__init__(o,M.value["VIEW"])
class H:
 def __init__(o):
  M=e()
  f.__init__(o,M.value["MODEL"])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
