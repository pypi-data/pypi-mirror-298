from xnippet import XnippetManager as XfistManager
from xnippet import setup_logging

__version__ = '0.0.0.dev0'

config = XfistManager(package_name='xfist',
                       package_version=__version__,
                       package__file__=__file__,
                       config_path=None,
                       config_filename='config.yaml')

__all__ = ['XfistManager', 'setup_logging']