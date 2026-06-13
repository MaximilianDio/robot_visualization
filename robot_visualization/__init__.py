"""robot_visualization - PyVista-based 3D visualization of URDF robots.

Provides the :class:`Robot` visualizer plus small visualization primitives
(coordinate frames, arrows, boxes) and shared video utilities.
"""

from .primitives import ArrowVisualizer, AxesVisualizer, BoxVisualizer
from .robot import Robot
from . import video_utils

__version__ = "0.2.0"

__all__ = [
    "Robot",
    "AxesVisualizer",
    "ArrowVisualizer",
    "BoxVisualizer",
    "video_utils",
]
