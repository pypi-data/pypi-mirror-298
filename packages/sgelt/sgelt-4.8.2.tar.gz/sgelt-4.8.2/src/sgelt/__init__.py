"""Set logging, locale and package_dir"""

from pathlib import Path
from .__version__ import __version__

__all__ = ['__version__', 'package_dir']

package_dir = Path(__file__).parent
