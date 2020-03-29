#region imports
import functools
import os
import shutil
import stat
import subprocess
import sys
import time

import psutil
from psutil import MACOS
from psutil import POSIX
from psutil import WINDOWS

from psutil._compat import which
#endregion


__all__ = [
    # constants
    'DEVNULL' , 'PYTHON_EXE', 'TESTFILE_PREFIX' , 'TESTFN',
    # subprocesses
    'get_test_subprocess',
    # test utils
    'unittest' ,
    # fs utils
    'safe_rmpath' ,
    # sync primitives
    'wait_for_pid', 'wait_for_file',
]


TESTFILE_PREFIX = '$testfn'
if os.name == 'java':
    # Jython disallows @ in module names
    TESTFILE_PREFIX = '$psutil-test-'
else:
    TESTFILE_PREFIX = '@psutil-test-'
TESTFN = os.path.join(os.path.realpath(os.getcwd()), TESTFILE_PREFIX)
TESTFN = TESTFN + str(os.getpid())

_TESTFN = TESTFN + '-internal'


def _get_py_exe():
    def attempt(exe):
        try:
            subprocess.check_call(
                [exe, "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception:
            return None
        else:
            return exe

    if MACOS:
        exe = \
            attempt(sys.executable) or \
            attempt(os.path.realpath(sys.executable)) or \
            attempt(which("python%s.%s" % sys.version_info[:2])) or \
            attempt(psutil.Process().exe())
        if not exe:
            raise ValueError("can't find python exe real abspath")
        return exe
    else:
        exe = os.path.realpath(sys.executable)
        assert os.path.exists(exe), exe
        return exe


PYTHON_EXE = _get_py_exe()
DEVNULL = open(os.devnull, 'r+')

_subprocesses_started = set()


def get_test_subprocess(cmd=None, **kwds):
    """Creates a python subprocess which does nothing for 30 secs and
    return it as subprocess.Popen instance.
    If "cmd" is specified that is used instead of python.
    By default stdin and stdout are redirected to /dev/null.
    It also attemps to make sure the process is in a reasonably
    initialized state.
    The process is registered for cleanup on reap_children().
    """
    kwds.setdefault("stdin", DEVNULL)
    kwds.setdefault("stdout", DEVNULL)
    kwds.setdefault("cwd", os.getcwd())
    kwds.setdefault("env", os.environ)
    if WINDOWS:
        # Prevents the subprocess to open error dialogs. This will also
        # cause stderr to be suppressed, which is suboptimal in order
        # to debug broken tests.
        CREATE_NO_WINDOW = 0x8000000
        kwds.setdefault("creationflags", CREATE_NO_WINDOW)
    if cmd is None:
        safe_rmpath(_TESTFN)
        pyline = "from time import sleep;" \
                 "open(r'%s', 'w').close();" \
                 "sleep(30);" % _TESTFN
        cmd = [PYTHON_EXE, "-c", pyline]
        sproc = subprocess.Popen(cmd, **kwds)
        _subprocesses_started.add(sproc)
        #wait_for_file(_TESTFN, delete=True, empty=True)
    else:
        sproc = subprocess.Popen(cmd, **kwds)
        _subprocesses_started.add(sproc)
        wait_for_pid(sproc.pid)
    return sproc


def wait_for_pid(pid):
    """Wait for pid to show up in the process list then return.
    Used in the test suite to give time the sub process to initialize.
    """
    psutil.Process(pid)
    if WINDOWS:
        # give it some more time to allow better initialization
        time.sleep(0.01)


def wait_for_file(fname, delete=True, empty=False):
    """Wait for a file to be written on disk with some content."""
    with open(fname, "rb") as f:
        data = f.read()
    if not empty:
        assert data
    if delete:
        safe_rmpath(fname)
    return data


def safe_rmpath(path):
    "Convenience function for removing temporary test files or dirs"
    def retry_fun(fun):
        # On Windows it could happen that the file or directory has
        # open handles or references preventing the delete operation
        # to succeed immediately, so we retry for a while. See:
        # https://bugs.python.org/issue33240
        stop_at = time.time() + 1
        while time.time() < stop_at:
            try:
                return fun()
            except FileNotFoundError:
                pass

    try:
        st = os.stat(path)
        if stat.S_ISDIR(st.st_mode):
            fun = functools.partial(shutil.rmtree, path)
        else:
            fun = functools.partial(os.remove, path)
        if POSIX:
            fun()
        else:
            retry_fun(fun)
    except FileNotFoundError:
        pass