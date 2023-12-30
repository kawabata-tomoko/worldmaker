import os
import logging
import pickle
from functools import wraps
from datetime import datetime
from worldmaker.configs.config_setting import CONFIGS

global LOGGER, REGISTER
REGISTER = {}

class LoggerManager(logging.Logger):
    def __init__(
        self,
        name: str,
        level=0,
        log_path=f"{CONFIGS.common.defaults()['log_path']}/{datetime.now().strftime('TESLA_%Y%m%d_%H_%M_logs')}",
        parent=None,
        format="%(asctime)s %(name)s - %(levelname)s  (%(pathname)s:%(funcName)s:%(lineno)d) \n%(message)s",
    ) -> None:
        super().__init__(name, level)
        if not isinstance(parent,LoggerManager)and parent:
            raise TypeError("Not valid type of parent")
        else:
            self.parent = parent 
        self.log_path = log_path
        self.format = format
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        REGISTER[self] = set()
        
    def run(self):
        """
        The function adds a file handler to a logger object and sets the formatter for the log messages.
        """
        handler = logging.FileHandler(f"{self.log_path}/{self.name}.log")
        formatter = logging.Formatter(self.format)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def add_child_logger(self, name, propagate=True):
        """
        The function `add_child_logger` creates a child logger with the specified name and settings,
        adds it to a register, and returns the child logger.
        
        :param name: The name of the child logger to be created
        :param propagate: The `propagate` parameter determines whether log messages from the child
            logger should be propagated to the parent logger. If `propagate` is set to `True`, log messages
            from the child logger will be passed to the parent logger and potentially to higher-level
            loggers in the logger hierarchy. If `, defaults to True (optional)
        :return: the child logger that was created.
        """
        self.info(f"Create a child logger :{name}")
        child = LoggerManager(
            name=name, level=self.level, log_path=self.log_path, parent=self
        )
        child.propagate=propagate
        REGISTER[self].add(child)
        child.run()
        return child
    def rebase(self, new_parent):
        """
        The `rebase` function updates the parent of a `LoggerManager` object and calls the `update`
        method.
        
        :param new_parent: The `new_parent` parameter is an instance of the `LoggerManager` class
        """
        if isinstance(new_parent, LoggerManager):
            self.parent = new_parent
            self.update()
    def update(self):
        """
        The update function updates the level and log_path attributes of an object and recursively calls
        the update function on its child objects.
        """
        self.level = self.parent.level if self.parent else logging.DEBUG
        self.log_path=self.parent.log_path
        for child in REGISTER[self]:
            child.update()
    def catch_error(self,func):
        """
        The `catch_error` function is a decorator that catches any exceptions that occur in the
        decorated function, logs the error message, saves the function arguments and keyword arguments
        to a pickle file, and re-raises the exception.
        
        :param func: The `func` parameter is a function that you want to wrap with error handling. It is
            the function that will be executed within the `wrapper` function
        :return: The function `catch_error` returns a decorated version of the input function `func`.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.error(f'Error occurred in {func.__name__} function.\nError message: {e}')
                with open(f"{self.log_path}/{func.__name__}_error.pickle", 'wb') as f:
                    pickle.dump((args,kwargs),f)
                raise e
        return wrapper
    def save_debugs(self,func_name,locals,globals):
        """
        The function `save_debugs` saves the local and global variables of a function into a pickle file
        for debugging purposes.
        
        :param func_name: The `func_name` parameter is a string that represents the name of the function
            where the debug variables are being saved
        :param locals: The `locals` parameter refers to the local variables within the scope of the
            function `save_debugs`. These variables are specific to the function and can only be accessed
            within the function
        :param globals: The `globals` parameter refers to the global namespace, which contains all the
            variables and functions that are defined outside of any function or class. It includes variables
            and functions that can be accessed from anywhere in the code
        """
        self.debug(f"Trying to save vars in {func_name}")
        with open(f"{self.log_path}/{self.name}_{func_name}_debug_{datetime.now().strftime('%H_%M')}.pickle", 'wb') as f:
            pickle.dump((locals,globals),f)
    def __hash__(self):
        return hash(f"{self.name}")
    def __repr__(self):
        return f"{self.name}:{self.level}"


LOGGER = LoggerManager(name="tesla.main_process", level=logging.DEBUG)
LOGGER.run()
# __all__ = ["LOGGER"]