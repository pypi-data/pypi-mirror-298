__all__ = ['config']

from ._imports import *
from sys import platform

config = configparser.ConfigParser()

def modify_local_folder_to_linux_path():
    #assume in linux platform, need to change ds_config file path
    config_path = r'/home/eds_ds/model/mlop/ds_config.txt'
    out_row = []
    with open (config_path, 'r') as f:
        for l in f.readlines():
            if 'local_folder' in l:
                l = r'local_folder = /home/eds_ds/model/temp'            
            out_row.append(l)        

    with open(config_path, 'w') as f:
        for line in out_row:
            if line.strip(): 
                f.write(f"{line}\n")
    return 

if platform == "linux" or platform == "linux2":
    modify_local_folder_to_linux_path()
    config.read(r'/home/eds_ds/model/mlop/ds_config.txt')
elif platform == "darwin":
    pass # OS X
elif platform == "win32":
    if os.environ.get("CONFIG") == None:
        config.read(f'C:\\Users\\{getpass.getuser()}\\ds_config.txt')
    else:
        config.read(os.environ.get("CONFIG"))

