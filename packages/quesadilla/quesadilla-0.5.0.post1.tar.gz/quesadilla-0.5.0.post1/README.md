<!-- `quesadilla` - an elegant background task queue for the more civilized age
Copyright (C) 2024 Artur Ciesielski <artur.ciesielski@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. -->

[![pipeline status](https://gitlab.com/arcanery/python/quesadilla/quesadilla/badges/main/pipeline.svg)](https://gitlab.com/arcanery/python/quesadilla/quesadilla/-/commits/main)
[![coverage report](https://gitlab.com/arcanery/python/quesadilla/quesadilla/badges/main/coverage.svg)](https://gitlab.com/arcanery/python/quesadilla/quesadilla/-/commits/main)
[![latest release](https://gitlab.com/arcanery/python/quesadilla/quesadilla/-/badges/release.svg)](https://gitlab.com/arcanery/python/quesadilla/quesadilla/-/releases)

# quesadilla

`quesadilla` is an elegant background task queue for the more civilized age.

## Example usage

First, install `quesadilla`: `pip install quesadilla==0.5.0`.

`tasks.py`:

```python
import logging
import random

from quesadilla.connectors.in_memory import ThreadSafeInMemoryConnector
from quesadilla.core import TaskNamespace, async_task, sync_task

logging.basicConfig(level=logging.INFO)

namespace = TaskNamespace("tasks", connector=ThreadSafeInMemoryConnector())
queue = namespace.queue("queue")


@sync_task(queue)
def simple_task(i: int) -> bool:
    return i == 0


@async_task(queue)
async def simple_atask(i: int) -> bool:
    return i == 0


# simulate someone adding jobs to the queue
# queue is preloaded with 200 tasks
for _ in range(100):
    simple_task.queue(random.choice((0, 1)))
    simple_atask.queue(random.choice((0, 1)))
```

Run with `python -m quesadilla runners listener tasks::queue`.

Exit with `SIGINT` (Ctrl + C) or `SIGTERM`.

## Roadmap

- support for retrying failed tasks
- support for cronjobs and heartbeat
- support for task priority
- support for delayed execution
- documentation
- a real-world connector! (most likely PostgreSQL with `psycopg` and `SQLAlchemy 2.0`)
