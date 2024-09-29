# loggext-py
logging extensions for pythons logging library

<!-- TOC -->
* [loggext-py](#loggext-py)
  * [Installation](#installation)
  * [Features](#features)
  * [Usage](#usage)
<!-- TOC -->

## Installation

```shell
pip install loggext
```

## Features

- function-decorators for logging
  - with support for asnyc-functions
- additional logging-handlers
  - ColoredConsoleHandler

## Usage

```python
import logging
import loggext
from loggext.decorators import add_logging

# only configures if not already configured
if not loggext.logging_is_configured():
    logging.basicConfig(
        level=logging.NOTSET,
        handlers=[
            # adds colored output based on the level of each message
            loggext.handlers.ColoredConsoleHandler()
        ],
    )

@add_logging(
  call=True,  # logs when the function is called
  call_args=True,  # logs passed arguments of call
  timeit=True,   # measure performance of the function
  timeit_precision=2,  # number of units when formatting timing
  result=True,  # log the result
)  # note: exception-logging is always
def myfn(arg):
    ...  # stuff

myfn("value")
# DEBUG:root:<function myfn at 0x7f06a6cc3400> was called with ('value')
# DEBUG:root:<function myfn at 0x7f06a6cc3400> returned None after 65μs+614ns
```
