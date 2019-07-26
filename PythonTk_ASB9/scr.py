__author__ = 'AlexM'
#SOURCEs
from os.path import abspath, join, dirname, realpath
from platform import system

if system() == 'Windows':

    #SCR_PATH = abspath(join(dirname((realpath(__file__))),"library.zip", "scr"))
    SCR_PATH = abspath(join(dirname((realpath(__file__))), "scr"))
    # if 'library.zip' in SCR_PATH:
    #     SCR_PATH.remove('library.zip') #trick for py2exe
    ICON_PATH = join(SCR_PATH, "orad.ico")
    DB_PATH = join(SCR_PATH, "last_asb.txt")
    DSEARCH_PATH = join(SCR_PATH, "dsearch.exe")



