import os
import json
import logging.config

#SET MODE:
def setup_logging(
    default_path='logs/logging.json',
    default_level=logging.INFO):
    """Setup logging configuration
    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        print 'loded'
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger(__name__)

# logger.info('Logger Info')
# logger.error('Logger Error')
# logger.debug('Logger Debug')

# logger.setLevel(logging.INFO)
# logger.info('Logger Info')
# logger.error('Logger Error')
# logger.debug('Logger Debug')
