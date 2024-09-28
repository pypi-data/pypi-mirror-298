# -*- coding: utf-8 -*-
import inspect
import logging
import sys


class PoppyLogger:
    @property
    def logger(self):
        calling_module = inspect.currentframe().f_back
        calling_module_name = calling_module.f_globals["__name__"]
        return logging.getLogger(calling_module_name)


sys.modules[__name__] = PoppyLogger()
