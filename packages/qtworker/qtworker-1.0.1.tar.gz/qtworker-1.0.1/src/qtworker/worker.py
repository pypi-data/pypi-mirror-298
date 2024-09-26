# -*- coding: utf-8 -*-
"""
@author: kolja
"""

import sys
import traceback

from qtpy.QtCore import QObject, QRunnable, Signal

class WorkerSignals(QObject):
    started = Signal()
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)


class Worker(QRunnable):
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.signals = WorkerSignals()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.signals.started.emit()
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception:
            # traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
