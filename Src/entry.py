import os
import sys
import threading
import subprocess

try:
    subprocess.Popen([sys.executable, "main.py"], creationflags=subprocess.CREATE_NO_WINDOW)
except:
    os.system("python main.py")