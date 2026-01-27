"""
robot_visualization - A Python package for robot visualization using URDF files and PyVista

This package provides tools for visualizing robots defined by URDF files,
including support for forward kinematics, end-effector visualization, and
trajectory plotting.
"""

__version__ = '0.1.0'

# Import main classes from submodules using relative imports
from .robot import Robot
from .primitives import AxesVisualizer, ArrowVisualizer
from . import video_utils

# Re-export urdfpy classes for convenience
try:
    from urdfpy import URDF
    __all__ = ['Robot', 'AxesVisualizer', 'ArrowVisualizer', 'video_utils', 'URDF']
except ImportError:
    # urdfpy not available, only export our classes
    __all__ = ['Robot', 'AxesVisualizer', 'ArrowVisualizer', 'video_utils']
