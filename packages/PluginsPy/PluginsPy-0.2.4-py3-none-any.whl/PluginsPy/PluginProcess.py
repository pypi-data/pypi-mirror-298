import threading
import multiprocessing
import importlib
import inspect
import re
import traceback

def getClazzWithRun(moduleString, **args):
    ret = None
    module = None

    try:
        if moduleString == "VisualLogPlot":
            # import file
            module = importlib.import_module("PluginsPy." + moduleString)
        else:
            # import file
            module = importlib.import_module("Plugins." + moduleString)

        matchObj     = re.match(r'\d{4}[_]?', moduleString)
        if matchObj:
            moduleString = moduleString.replace(matchObj.group(0), "")

        # get class
        clazz  = getattr(module, moduleString)
        # new class
        obj = clazz(args)

        invert_op = getattr(obj, "start", None)
        if callable(invert_op):
            print(">>> enter plugin start method")
            if len(inspect.signature(invert_op).parameters) > 0:
                ret = invert_op(args)
            else:
                ret = invert_op()
            print("<<< end plugin start method")
    except Exception as e:
        print(e)
        traceback.print_exc()

    if ret == None:
        return ""
    elif isinstance(ret, list):
        return "\n".join(ret)
    elif isinstance(ret, int) or isinstance(ret, float):
        return str(ret)
    else:
        return ret

class PluginProcess(threading.Thread):

    def __init__(self, moduleString, kwargs):
        super().__init__()
        self.moduleString = moduleString
        self.kwargs = kwargs

    def run(self):
        print("PluginProcess running")

        p = multiprocessing.Process(target=getClazzWithRun, args=(self.moduleString,), kwargs=self.kwargs)
        p.start()
        p.join()
