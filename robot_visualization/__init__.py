"""
robot_visualization - A Python package for robot visualization using URDF files and PyVista

This package provides tools for visualizing robots defined by URDF files,
including support for forward kinematics, end-effector visualization, and
trajectory plotting.
"""

__version__ = '0.1.0'

# Import main classes from submodules
from robot_visualization.robot import Robot
from robot_visualization.primitives import AxesVisualizer, ArrowVisualizer

# Re-export urdfpy classes for convenience
try:
    from urdfpy import URDF
    __all__ = ['Robot', 'AxesVisualizer', 'ArrowVisualizer', 'URDF']
except ImportError:
    # urdfpy not available, only export our classes
    __all__ = ['Robot', 'AxesVisualizer', 'ArrowVisualizer']
