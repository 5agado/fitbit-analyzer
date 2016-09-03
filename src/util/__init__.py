import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Console handler
#formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s - %(message)s", "%H:%M:%S")
#ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
#ch.setFormatter(formatter)
#logger.addHandler(ch)