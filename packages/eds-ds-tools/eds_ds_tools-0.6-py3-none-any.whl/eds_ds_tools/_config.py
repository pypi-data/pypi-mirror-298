__all__ = ['config']

from ._imports import *
from sys import platform

config = configparser.ConfigParser()

if platform == "linux" or platform == "linux2":
    config.read(r'/home/eds_ds/model/mlop/ds_config.txt')
elif platform == "darwin":
    pass # OS X
elif platform == "win32":
    if os.environ.get("CONFIG") == None:
        config.read(f'C:\\Users\\{getpass.getuser()}\\ds_config.txt')
    else:
        config.read(os.environ.get("CONFIG"))

