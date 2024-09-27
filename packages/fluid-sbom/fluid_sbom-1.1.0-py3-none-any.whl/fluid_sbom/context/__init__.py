import logging
import os

LOGGER = logging.getLogger(__name__)

try:
    CI_COMMIT_REF_NAME = os.environ["CI_COMMIT_REF_NAME"]
    CI_COMMIT_SHA = os.environ["CI_COMMIT_SHA"]
    CI_COMMIT_SHORT_SHA = CI_COMMIT_SHA[0:8]
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except KeyError as ex:
    LOGGER.exception("Environment variable %s doesn't exist", ex.args[0])
    raise
