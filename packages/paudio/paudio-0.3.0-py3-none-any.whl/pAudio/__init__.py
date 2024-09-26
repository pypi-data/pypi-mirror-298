import os
import subprocess
from . import paplay,parecord


#Check if host is android
if [os.environ.get('ANDROID_ROOT')]:
    print("Android detected, so using termux")
    subprocess.run(["pactl" ,"load-module","module-sles-source"])



try:
    check_pulseaudio_running = subprocess.run(['pulseaudio', '--check'], stdout=subprocess.PIPE,check=True)
except:
    print("Pulseaudio is not running, So starting it")
    subprocess.run(['pulseaudio', '--start',"--exit-idle-time=-1"])

__version__ = "0.3.0"
