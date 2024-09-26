# qt Worker

A generic worker class for QThreadpool use.


The following snippet shows the basic usecase
```
from qtworker import Worker

self.pool = QThreadpool()

worker = Worker(function, *args, **kwargs)
worker.signals.started.connect(self.handle_start)
worker.signals.result.connect(self.handle_result)
worker.signals.error.connect(self.handle_error)
worker.signals.finished.connect(self.handle_cleanup)
self.pool.start(worker)
```

> Todo: with full context



## setup

install the package via pip:
```
pip install qtworker
```

The full documentation can be found under 
[configwidgets documentation](https://qtworker.readthedocs.io/en/latest/)
The source code can be found under
[configwidgets repository](https://github.com/kolja-wagner/qtworker)