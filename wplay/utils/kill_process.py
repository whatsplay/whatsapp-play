#These lines import signal library for asynchronous event handling along with psutil for process and system utility.

import signal
import psutil

# Checks for the event handler by using exception handling with try and except if still not working then prints process killed.
def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    print('Process Killed!')
    for process in children:
        process.send_signal(sig)
