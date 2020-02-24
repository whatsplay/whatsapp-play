import signal
import psutil


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    print('Process Killed!')
    for process in children:
        process.send_signal(sig)
