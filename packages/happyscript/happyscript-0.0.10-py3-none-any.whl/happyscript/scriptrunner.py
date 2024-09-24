import datetime, logging, threading
from .scriptexceptions import ScriptUserAbortException
from .scriptexceptions import ScriptRecursiveAbortException
class ScriptThreadRunner:
    logger = logging.getLogger("happyscript.scriptrunner")
    MARKER_LEVEL = 25
    def __init__(self, ctrl):
        self._ctrl = ctrl
        self._recurse_count = 0
        self.top_script_name = ''
        self.last_result = False
        self.busy = False
    def execute_script(self, script_name, script_func, argvalues):
        self.last_result = False
        self.busy = True
        if threading.currentThread().getName()=="ScriptThread":
            self.execute_threadfunc(script_name, script_func, argvalues)
        elif self._recurse_count>0:
            self.logger.error( "Script '%s' already running.  Wait until it completed." % self.top_script_name )
        else:
            self.top_script_name = script_name
            thread = threading.Thread(name = "ScriptThread", target=self.execute_threadfunc, args=(script_name, script_func, argvalues) )
            thread.start()
    def execute_threadfunc(self, script_name, script_func, argvalues):
        if self._recurse_count<0:
            self._recurse_count = 0
        tstamp = datetime.datetime.now().strftime("%m/%d_%H:%M")
        self.logger.log(self.MARKER_LEVEL, "__________%s__________%s__" % (script_name, tstamp) )
        test_passed = False
        all_tests_done = False
        try:
            self._recurse_count += 1
            self._ctrl.set_busy(True)
            script_func( *argvalues )
            test_passed = True
        except ScriptUserAbortException as _:
            self.logger.error("Script stopped by user")
        except Exception as e:
            if self._ctrl.m_stop_script:
                self.logger.error("Script stopped by user")
            else:
                logging.error(str(e), exc_info = e)
        finally:
            self._recurse_count -= 1
            if self._recurse_count<=0:
                all_tests_done = True
            if test_passed:
                self.logger.log(self.MARKER_LEVEL, "\\_________%s__________ PASS ______/" % script_name )
            else:
                self.logger.log(self.MARKER_LEVEL, "\\_________%s__________ FAIL ______/" % script_name )
        if self._recurse_count>0 and test_passed==False:
            raise ScriptRecursiveAbortException("Stopping parent script...")
        if all_tests_done:
            self._recurse_count = 0
            self.top_script_name=''
            self.last_result = test_passed
            self._ctrl.set_busy(False)
            self.busy = False
class ScriptParallelThread(threading.Thread):
    thread_counter = 0
    def __init__(self, ctrl, func, arg_list):
        thread_name = "Parallel" + str(ScriptParallelThread.thread_counter)
        threading.Thread.__init__(self, name=thread_name)
        ScriptParallelThread.thread_counter += 1
        self._ctrl = ctrl
        self.the_func = func
        self.arg_list = arg_list
        self.success = False
        self.stopped_by_user = False
        self.start()
    def run(self):
        try:
            self.the_func( *self.arg_list )
            self.success = True
        except ScriptUserAbortException as _:
            pass
        except Exception as e:
            if self._ctrl.m_stop_script:
                self.stopped_by_user = True
            else:
                logging.error(str(e), exc_info = e)
class ScriptRunner:
    logger = logging.getLogger("happyscript.runner")
    def __init__(self, script_params, script_readers, script_control):
        self.script_params = script_params
        self._readers = script_readers
        self._recurse_count = 0
        self.start_ok = False
        self._ctrl = script_control
        self.thread_runner = ScriptThreadRunner(script_control)
    @property
    def test_passed(self):
        return self.start_ok and self.thread_runner.last_result
    @property
    def busy(self):
        return self.thread_runner.busy
    def find_scriptfunct(self, script_name):
        parts = script_name.split(".")
        if len(parts) != 3:
            self.logger.error("Must provide script name as dirname.filename.scriptname")
            return None
        if not parts[0] in self._readers:
            self.logger.error("Cannot start %s : group %s not found",  script_name, parts[0])
            return  None
        func = self._readers[parts[0]].get_func(parts[1], parts[2])
        if func is None:
            self.logger.error("Cannot start %s : function not found", script_name)
        return func
    def run_script(self, script_name, **extra_params):
        self.start_ok = False
        if threading.currentThread().getName().startswith("Parallel"):
            self.logger.error("You cannot start other scripts in a parallel thread.")
            return
        func = self.find_scriptfunct(script_name)
        if func is None: return
        (argvalues, missing) = self.script_params.get_parameters(func, extra_params)
        if len(missing)>0:
            self.logger.error( "Error : missing value for parameter(s) %s" % ("".join(missing) ) )
            return
        self.thread_runner.execute_script(script_name, func, argvalues)
        self.start_ok = True
    def run_parallel(self, func, parname, parvalues, **extra_params):
        assert threading.currentThread().getName()=="ScriptThread", "run_parallel() can only be executed from within a (non-parallel) script function"
        if not callable(func):
            func = self.find_scriptfunct(func)
            assert func is not None, f"Parameter 'func' of run_parallel is no function or script name."
        threads = list()
        for val in parvalues:
            extra_params[parname] = val
            (argvalues, missing) = self.script_params.get_parameters(func, extra_params)
            if len(missing)>0:
                self.logger.error( "Error : missing value for parameter(s) %s" % ("".join(missing) ) )
                return
            threads.append( ScriptParallelThread(self._ctrl, func, argvalues) )
        fail_count = 0
        stopped_by_user = 0
        for thread in threads:
            thread.join()
            if not thread.success:
                fail_count += 1
            if thread.stopped_by_user:
                stopped_by_user += 1
        if stopped_by_user>0:
            self.logger.error(f"{stopped_by_user} scripts stopped by user")
        assert fail_count==0, f"Parallel executiong failed on {fail_count} threads"
