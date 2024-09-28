class AbstractLogger:
    def __init__(self, log_dir=None):
        self.log_dir = log_dir
    def log(self, name, value):
        pass

loggers = {}
def register_logger(name, logger = None):
    if name in loggers:
        if logger is not None:
            loggers[name] = logger
        return loggers[name]
    else:
        loggers[name] = logger
    return logger

def remove_logger(name):
    if name in loggers:
        del loggers[name]

def get_logger(name):
    if name not in loggers:
        return AbstractLogger()
    return loggers[name]


class LoggerContext:
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.logger = get_logger(self.name)
        return self.logger
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def monitor(name):
    return LoggerContext(name)
