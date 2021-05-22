__version__ = '0.1'

from os.path import join, dirname

this_directory = dirname(__file__)
QUASAR_GUI_INDEX_PATH = join(this_directory, 'assets', 'index.html')

from .main import run, set_main_component
from ._base import Model
