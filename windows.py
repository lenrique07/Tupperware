
from configparser import ConfigParser
import os
import re
import platform
import psutil


def main():   
    pid = ""
    if platform.system() == "Windows":
        config = ConfigParser()
        config.read('settings.ini')
        puerto = config['Server']['port']
        output_command = os.popen("netstat -noa").readlines()
        for line in output_command:
            if len(re.findall(puerto, line)) > 0:
                print(line)
                pid = (list(line.split(" "))).pop()
                break
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                try:
                    if processID == int(pid) and processName == "python.exe":
                        print(processName , ' ::: ', processID)
                        endProcess = "taskkill /F /PID " + pid
                        os.system(endProcess)
                        break
                except:
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass