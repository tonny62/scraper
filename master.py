import subprocess
import time
import os

if(__name__ == '__main__'):
    while(True):
        if('done' in os.listdir()):
            break
        else:
            subprocess.run(['python3', 'main.py', '-d'])
