import time
from .scriptexceptions import ScriptUserAbortException
class ScriptControl:
    def __init__(self):
        self.m_stop_script = False
        self._is_busy = False
        self._script_runner = None
    def set_script_runner(self, runner):
        self._script_runner = runner
    def set_busy(self, is_busy):
        self._is_busy = is_busy
        self.m_stop_script = False
    def is_busy(self):
        return self._is_busy
    def stop(self):
        if self._is_busy:
            print("'stop' flag is set.  Scripts may stop soon.")
        else:
            print("Normally no script is active, but I'll set the 'stop' flag anyway.")
        self.m_stop_script = True
    def ok(self):
        return not self.m_stop_script
    def check(self):
        if self.m_stop_script:
            raise ScriptUserAbortException( "Script stopping on user request" )
    def sleep(self, time_in_seconds):
        t = time_in_seconds
        while t>0:
            if t > 0.5:
                time.sleep(0.5)
            else:
                time.sleep(t)
            t = t-0.5
            if self.m_stop_script:
                raise ScriptUserAbortException( "Script stopping on user request" )
    def run(self, script_name, **argv):
        assert self._script_runner is not None, "Internal error: scriptrunner is not set"
        return self._script_runner.run_script(script_name, **argv)
    def run_parallel(self, func, parname, parvalues, **extra_params):
        return self._script_runner.run_parallel(func, parname, parvalues, **extra_params)
