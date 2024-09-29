"""
handle Synfig animations

Sangfroid allows you to load, change, and save Synfig animations
using Python.
"""
import sangfroid.layer
import sangfroid.value

from sangfroid.keyframe import *
from sangfroid.animation import *
from sangfroid.t import *

def open(filename):
    """
    Loads the Synfig file with the given filename.

    Args:
        filename (str): the name of the source file. Can be .sfg, .sif,
            or .sifz.

    Returns:
        Animation
    """
    result = Animation(filename)
    return result

__version__ = '0.2'

__all__ = [
        'layer',
        'Canvas',
        'Keyframe',
        'Animation',
        'T',

        'open',
        ]
