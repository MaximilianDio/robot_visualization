"""
robot_visualization package

This wrapper exposes the robot_visualization subpackage functionality.
"""
import importlib.util
import sys
import os
from pathlib import Path

# Get paths to the actual module files
_base_dir = Path(__file__).parent
_robot_module_path = _base_dir / 'robot_visualization' / 'robot.py'
_primitives_module_path = _base_dir / 'robot_visualization' / 'primitives.py'
_video_utils_module_path = _base_dir / 'robot_visualization' / 'video_utils.py'

# Manually load the modules
def _load_module(name, file_path):
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Load robot, primitives, and video_utils modules
_robot_mod = _load_module('robot_visualization.robot', _robot_module_path)
_primitives_mod = _load_module('robot_visualization.primitives', _primitives_module_path)
video_utils = _load_module('robot_visualization.video_utils', _video_utils_module_path)

# Export the classes
Robot = _robot_mod.Robot
AxesVisualizer = _primitives_mod.AxesVisualizer
ArrowVisualizer = _primitives_mod.ArrowVisualizer

__version__ = '0.1.0'
__all__ = ['Robot', 'AxesVisualizer', 'ArrowVisualizer', 'video_utils']

# Try to also expose URDF from urdfpy
try:
    from urdfpy import URDF
    __all__.append('URDF')
except ImportError:
    pass
