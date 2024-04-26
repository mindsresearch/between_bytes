""" SsiLogger - A simple logging wrapper.

This module provides a simple interface for logging in Python. It is a wrapper around
Python's built-in logging module, providing a more user-friendly interface that
consolidates debug and audit logs into a single object.

The module provides two concrete classes: RootLogger and ChildLogger. RootLogger is a
singleton class that provides the main logging interface. ChildLogger is a class
that provides a child logger of the RootLogger, allowing for more descriptive naming.

One base class, SsiLogger, is provided for type hinting. It should not be used directly.

When run as a script, this module runs the series of tests that were used to develop the module.
"""
import logging
import sys
from pathlib import Path
import argparse
from time import sleep

class SsiLogger:
    """ Base class for logging wrapper.

    Do not call this class directly - use RootLogger or ChildLogger instead.

    This class is a wrapper around Python's logging module,
    consolidating debug and audit logs into a single simple interface.
    """

    def crit(self, message:str, throw:Exception=None) -> None:
        """ Log a critical message.

        This should be used for unrecoverable errors that will crash the program.

        Args:
            message (str): The message to log.
            throw (Exception, optional): An exception to raise with the message. Defaults to None.

        Raises:
            Exception: If `throw` is provided, raise it with the message.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def err(self, message:str) -> None:
        """ Log an error message.

        This should be used for recoverable errors that will not
        crash the program but may impede functionality.

        Args:
            message (str): The message to log.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def warn(self, message:str) -> None:
        """ Log a warning message.

        This should be used for non-critical issues that may
        become a bigger issue later. Program continues to run normally.

        Args:
            message (str): The message to log.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def info(self, message:str) -> None:
        """ Log an informational message.

        This should be used for general runtime information and 'all is well' confirmations.

        Args:
            message (str): The message to log.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def debug(self, message:str) -> None:
        """ Log a debug message.

        This should be used for detailed information about program state and execution.

        Args:
            message (str): The message to log.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def use_inet(self, url:str) -> None:
        """ Log internet access.

        This should be used for reporting URLs accessed by the program.

        Args:
            url (str): The URL accessed.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def use_file(self, path:Path, message:str) -> None:
        """ Log file access.

        This should be used for reporting any time a file are accessed by the program.

        Args:
            path (Path): The path to the file accessed.
            message (str): The type of access (e.g. 'contents', 'metadata').
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def wrote_file(self, path:Path) -> None:
        """ Log file writing.

        This should be used for reporting any time a file is written to by the program.

        Args:
            path (Path): The path to the file written.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

    def get_child(self, name:str) -> 'SsiLogger':
        """ Get a child logger with the given name.
        
        Create a new logger with a specific name if it does not already exist.

        Args:
            name (str): The name of the child logger.
        
        Returns:
            SsiLogger: The child logger.

        NOTE:
            If a child logger with the given name already exists,
            this method should return the existing logger.
        """
        raise NotImplementedError('Don\'t call me directly. Use RootLogger or ChildLogger instead.')

class RootLogger(SsiLogger):
    """ Singleton class for logging. Use this class to access
    the root logger and create child loggers.

    This class is a singleton, meaning that only one instance of it can exist at a time.
    This is to ensure that all loggers are using the same configuration and handlers.

    Attributes:
        logger (logging.Logger): The logger object for debug messages.
        auditor (logging.Logger): The logger object for audit messages.
        children (dict): A dictionary of child loggers, indexed by name.
        log_fmt (str): The format string for debug messages.
        aud_fmt (str): The format string for audit messages.

    Methods:
        crit(message:str, throw:Exception=None): Log a critical message.
            If an exception is provided, raise it with the message.
        err(message:str): Log an error message.
        warn(message:str): Log a warning message.
        info(message:str): Log an informational message.
        debug(message:str): Log a debug message.
        use_inet(url:str): Log internet access.
        use_file(path:Path, message:str='contents'): Log file access.
        wrote_file(path:Path): Log file write.
        get_child(name:str): Get a child logger with the given name.
        setup(verb:int, output:str): Set up the logger with the given verbosity level and output.
        set_verb(verb:int): Set the verbosity level of the logger.
        set_output(file:str=None, stream:str=None): Set the output for logging.

    WARNING:
        Do not modify any attributes directly.
        Use only the provided methods to interact with the logger.
    """
    def __new__(cls):
        """ Singleton enforcement and constructor."""
        if not hasattr(cls, 'instance'):
            cls.instance = super(RootLogger, cls).__new__(cls)
            cls.instance.logger  = logging.getLogger('root_debug')
            cls.instance.auditor = logging.getLogger('root_audit')
            cls.instance.children = {}
            cls.instance.log_fmt = 'T+ {relativeCreated:03.0f}ms - {name} - {levelname} - {message}'
            cls.instance.aud_fmt = 'T+ {relativeCreated:03.0f}ms - {name} - {message}'
        return cls.instance
    def crit(self, message:str, throw:Exception=None) -> None:
        self.logger.critical(message)
        if throw:
            raise throw(message)
    def err(self, message:str) -> None:
        self.logger.error(message)
    def warn(self, message:str) -> None:
        self.logger.warning(message)
    def info(self, message:str) -> None:
        self.logger.info(message)
    def debug(self, message:str) -> None:
        self.logger.debug(message)
    def use_inet(self, url:str) -> None:
        self.auditor.warning('[INET] - Accessed URL: %s', url)
    def use_file(self, path:Path, message:str='contents') -> None:
        self.auditor.info("[FILE I/O] - Accessed %s of file: %s", message, path.name)
        self.auditor.debug("[FILE I/O] - Full path: %s", path.absolute())
    def wrote_file(self, path:Path) -> None:
        self.auditor.info("[FILE I/O] - Wrote file: %s", path.name)
        self.auditor.debug("[FILE I/O] - Full path: %s", path.absolute())

    def get_child(self, name) -> 'ChildLogger':
        if name not in self.children:
            self.children[name] = ChildLogger(name)
        return self.children[name]

    def setup(self, verb:int, output:Path=None):
        """ Set up the logger with the given verbosity level and output.

        Args:
            verb (int): The verbosity level. 0 is PROD, 1 is DEV, 2 is DEBUG, 3 is SUPER.
            output (str): The output file path. If None, output will be sent to stdout.
        """
        self.set_verb(verb)
        self.set_output(output)

    def set_verb(self, verb:int):
        """ Set the verbosity level of the logger.

        Sets the verbosity of the ENTIRE logger system to one of the four pre-defined levels.

        These levels are:
            0 - PROD: Only logs internet usage and messages that may affect program execution.
            1 - DEV: Above plus file accesses and 'all is well' messages.
            2 - DEBUG: Above plus detailed execution information.
            3 - SUPER: Above plus full paths of file accesses.
                       Can create massive logs, so confirmation is required.

        Args:
            verb (int): The verbosity level. 0 is PROD, 1 is DEV, 2 is DEBUG, 3 is SUPER.

        Raises:
            ValueError: If an invalid verbosity level is provided.
        """
        print('Setting verbosity level to:', verb)
        match verb:
            case 0:
                self.logger.setLevel(logging.WARNING)
                self.auditor.setLevel(logging.WARNING)
            case 1:
                self.logger.setLevel(logging.INFO)
                self.auditor.setLevel(logging.INFO)
            case 2:
                self.logger.setLevel(logging.DEBUG)
                self.auditor.setLevel(logging.INFO)
            case 3:
                ver = input('WARNING: Enable SUPER level logging? (y/n)')
                if ver == 'y':
                    self.logger.setLevel(logging.DEBUG)
                    self.auditor.setLevel(logging.DEBUG)
                else:
                    print('Falling back to DEBUG...')
                    self.logger.setLevel(logging.DEBUG)
                    self.auditor.setLevel(logging.INFO)
            case _:
                raise ValueError('Invalid logging level! Valid levels are: 0, 1, 2, 3.')

    def set_output(self, file:str=None, stream:str=None):
        """
        Sets the output for logging.

        Args:
            file (str, optional): The file path to log to. Defaults to None.
            stream (str, optional): The stream to log to. Defaults to None.

        Raises:
            TypeError: If both `file` and `stream` are provided.

        """
        lf = logging.Formatter(self.log_fmt, style='{')
        af = logging.Formatter(self.aud_fmt, style='{')
        if file and stream:
            raise TypeError('You can only set one output at a time.')
        if file:
            print('Logging to file: ', file)
            log_hand = logging.FileHandler(file)
            aud_hand = logging.FileHandler(file)
        else:
            print('Logging to stream:', stream or 'stdout')
            log_hand = logging.StreamHandler(stream or sys.stderr)
            aud_hand = logging.StreamHandler(stream or sys.stdout)
        log_hand.setFormatter(lf)
        aud_hand.setFormatter(af)
        self.logger.addHandler(log_hand)
        self.auditor.addHandler(aud_hand)

class ChildLogger(SsiLogger):
    """ Class for child loggers. Use this class to create child loggers of the root logger.

    Attributes:
        logger (logging.Logger): The logger object for debug messages.
        auditor (logging.Logger): The logger object for audit messages.
        children (dict): A dictionary of child loggers, indexed by name.
        name (str): The name of the instance.

    Methods:
        crit(message:str, throw:Exception=None): Log a critical message.
            If an exception is provided, raise it with the message.
        err(message:str): Log an error message.
        warn(message:str): Log a warning message.
        info(message:str): Log an informational message.
        debug(message:str): Log a debug message.
        use_inet(url:str): Log internet access.
        use_file(path:Path, message:str='contents'): Log file access.
        wrote_file(path:Path): Log file write.
        get_child(name:str): Get a child logger with the given name.
    """

    def __init__(self, name, parent=None):
        self.name = name
        if parent is None:
            parent = RootLogger()
        self.logger = parent.logger.getChild(name)
        self.auditor = parent.auditor.getChild(name)
        self.children = {}

    def crit(self, message:str, throw:Exception=None):
        self.logger.critical(message)
        if throw:
            raise throw(message)
    def err(self, message:str):
        self.logger.error(message)
    def warn(self, message:str):
        self.logger.warning(message)
    def info(self, message:str):
        self.logger.info(message)
    def debug(self, message:str):
        self.logger.debug(message)
    def use_inet(self, url:str):
        self.auditor.warning('[INET] - Accessed URL %s', url)
    def use_file(self, path:Path, message:str='contents'):
        self.auditor.info("[FILE I/O] - Accessed %s of file %s", message, path.name)
        self.auditor.debug("[FILE I/O] - Full path: %s", path.absolute())
    def wrote_file(self, path:Path):
        self.auditor.info("[FILE I/O] - Wrote file %s", path.name)
        self.auditor.debug("[FILE I/O] - Full path: %s", path.absolute())

    def get_child(self, name):
        if name not in self.children:
            self.children[name] = ChildLogger(name, self)
        return self.children[name]

def demo_function(log:SsiLogger):
    """ A simple function for testing the logger."""
    log.debug('This is a debug message on demo')
    log.info('This is an info message on demo')
    log.warn('This is a warn message on demo')
    log.err('This is an err message on demo')
    log.crit('This is a crit message on demo')
    log.use_inet('demo.com')
    log.use_file(Path('path/to/demo.txt'))
    log.wrote_file(Path('path/to/demo.txt'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SsiLogger tests')
    parser.add_argument('-v', '--verb', action='count',
                        default=0, help='Verbosity level (-v, -vv, -vvv)')
    parser.add_argument('-l', '--log', help='Log file path (default: stdout)')
    args = parser.parse_args()
    r_log = RootLogger()
    r_log.setup(args.verb, args.log)

    print('====== TEST 1: RootLogger singleton ======')
    r_log_2 = RootLogger()
    if r_log is not r_log_2:
        raise AssertionError('RootLogger is not a singleton!')
    print('RootLogger is a singleton!')

    print('====== TEST 2: RootLogger basics ======')
    r_log.debug('This is a debug message on root')
    r_log.info('This is an info message on root')
    r_log.warn('This is a warn message on root')
    r_log.err('This is an err message on root')
    r_log.crit('This is a crit message on root')
    r_log.use_inet('root.com')
    r_log.use_file(Path('path/to/root.txt'))
    r_log.wrote_file(Path('path/to/root.txt'))

    print('====== TEST 3: ChildLogger basics ======')
    c_log = r_log.get_child('test')
    c_log.debug('This is a debug message on test')
    c_log.info('This is an info message on test')
    c_log.warn('This is a warn message on test')
    c_log.err('This is an err message on test')
    c_log.crit('This is a crit message on test')
    c_log.use_inet('test.com')
    c_log.use_file(Path('path/to/test.txt'))
    c_log.wrote_file(Path('path/to/test.txt'))

    print('====== TEST 4: ChildLogger singleton ======')
    c_log_2 = r_log.get_child('test')
    if c_log is not c_log_2:
        raise AssertionError('ChildLoggers are not singletons!')
    print('ChildLoggers are singletons!')

    print('====== TEST 5: Demo function ======')
    demo_function(r_log.get_child('demo'))

    print('====== TEST 6: Child of Child ======')
    demo_function(c_log.get_child('demo'))

    print('====== TEST 7: Sleepy boi ======')
    c_log = r_log.get_child('sleepy')
    c_log.debug('This is a debug message on test')
    sleep(0.1)
    c_log.info('This is an info message on test')
    sleep(0.1)
    c_log.warn('This is a warn message on test')
    sleep(0.1)
    c_log.err('This is an err message on test')
    sleep(0.05)
    c_log.crit('This is a crit message on test')
    sleep(0.05)
    c_log.use_inet('test.com')
    sleep(0.05)
    c_log.use_file(Path('path/to/test.txt'))
    sleep(0.002)
    c_log.wrote_file(Path('path/to/test.txt'))
