import yaml
K=type
f=dict
q=setattr
A=None
x=str
F=open
v=yaml.safe_load
from os import path
O=path.exists
class V:
 def __init__(S,my_dict:"dict[str, object]"):
  for z in my_dict:
   if K(my_dict[z])is f:
    q(S,z,V(my_dict[z]))
   else:
    q(S,z,my_dict[z])
class J:
 D=""
 def __init__(S,config_path=A):
  if y is A:
   if O(S.CONFIG_PATH):
    S.value=S.__load_config(S.CONFIG_PATH)
  else:
   if O(y):
    S.value=S.__load_config(y)
 def __load_config(S,file_path:x):
  with F(file_path,"r")as f:
   return v(f)
class h:
 def __init__(S):
  R=J()
  V.__init__(S,R.value["VIEW"])
class t:
 def __init__(S):
  R=J()
  V.__init__(S,R.value["MODEL"])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
