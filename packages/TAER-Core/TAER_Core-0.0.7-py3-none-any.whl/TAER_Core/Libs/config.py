import yaml
z=type
A=dict
f=setattr
u=None
E=str
x=open
from os import path
class d:
 def __init__(R,my_dict:"dict[str, object]"):
  for a in my_dict:
   if z(my_dict[a])is A:
    f(R,a,d(my_dict[a]))
   else:
    f(R,a,my_dict[a])
class I:
 U=""
 def __init__(R,config_path=u):
  if M is u:
   if path.exists(R.CONFIG_PATH):
    R.value=R.__load_config(R.CONFIG_PATH)
  else:
   if path.exists(M):
    R.value=R.__load_config(M)
 def __load_config(R,file_path:E):
  with x(file_path,"r")as f:
   return yaml.safe_load(f)
class X:
 def __init__(R):
  B=I()
  d.__init__(R,B.value["VIEW"])
class S:
 def __init__(R):
  B=I()
  d.__init__(R,B.value["MODEL"])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
