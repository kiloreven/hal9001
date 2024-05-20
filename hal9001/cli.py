#!/usr/bin/env python3
import sys
import time

from .conf import settings
from .service.pygame import start_loop, stop_loop
from .service.thread import start_thread


def main() -> None:
    start_thread()
    start_loop(settings.LOOP_FILENAME)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    stop_loop()
    sys.exit()


if __name__ == "__main__":
    main()
