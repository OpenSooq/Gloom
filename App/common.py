import sys
import logging

# intentionally allow this so that one can use "from .common import something"
# pylint: disable=W0401
from .base_utils import *
from .config import app_config
# pylint: disable=W0401
from .utils import *

logging.basicConfig(stream=sys.stderr, level=getattr(logging, app_config.log_level))
logger = logging.getLogger(__name__)

logging.debug("logging started")
