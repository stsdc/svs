import socket
import locale
import subprocess
import os
import signal
import psutil

locale.setlocale(locale.LC_ALL, 'C.UTF-8')


def run_system():
    if socket.gethostname() == 'main_unit':
        from server import UI
        UI()
    else:
        from client import Client
        client = Client()
        client.run()


def kill_another_instances():
    print 'Instance already running...'
    child = subprocess.Popen(['pgrep', '-f', "svs.py"], stdout=subprocess.PIPE, shell=False)
    pids = child.communicate()[0].split()
    print "PID, PPID:", os.getpid(), os.getppid()
    for pid in pids:
        try:
            if int(pid) != os.getppid():
                print "Killing...", int(pid)
                parent = psutil.Process(int(pid))
                children = parent.children(recursive=True)
                for process in children:
                    process.send_signal(signal.SIGKILL)
        except psutil.NoSuchProcess:
            return

    run_system()


kill_another_instances()
