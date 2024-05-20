import threading
from logging import getLogger

from .speech import start_mqtt_listen

logger = getLogger()


def start_thread() -> threading.Thread:
    """ """
    logger.info("Starting thread...")
    thread = threading.Thread(target=start_mqtt_listen)
    thread.daemon = True
    thread.start()
    return thread
