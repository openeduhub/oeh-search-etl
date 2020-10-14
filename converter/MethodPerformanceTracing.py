import logging
import time

class MethodPerformanceTracing():
    methodRuntimeWarning = 5
    methodRuntimeInfo = 2
    # intercept method and check if runtime is taking too long
    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if hasattr(attr, '__call__'):
            def newfunc(*args, **kwargs):
                start = time.time()
                result = attr(*args, **kwargs)
                diff = time.time() - start
                msg = 'calling ' + type(self).__name__ + '.' + attr.__name__ + ' took ' + str(diff) + 's'
                if diff > self.methodRuntimeWarning:
                    logging.warning(msg)
                elif diff > self.methodRuntimeInfo:
                    logging.info(msg)
                return result

            return newfunc
        else:
            return attr
