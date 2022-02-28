# pylint: disable=unused-import,missing-docstring
import os
from os.path import dirname, abspath

from .__version__ import __title__, __description__, __url__, __version__

ROOT_PATH = dirname(dirname(abspath(__file__)))
DEFAULT_DATA_ROOT_PATH = os.path.join(os.environ["HOME"], "data")
