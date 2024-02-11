
import logging
import logconf

logger = logging.getLogger(__name__)

def main():
    logconf.init()
    logger.info("An info")
    logger.warning("A warning")

if __name__ == "__main__":
    main()