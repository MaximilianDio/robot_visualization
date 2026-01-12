import pyvista as pv
import numpy as np
from scipy.spatial.transform import Rotation

# Example usage:

# plotter = pv.Plotter()
# axes_viz = AxesVisualizer(plotter, origin=[0, 0, 0], scale=1.0)
# axes_viz.update(position=[1, 1, 1], rodrigues=[0.1, 0.2, 0.3])
# plotter.show()

class AxesVisualizer:
    """A class to visualize coordinate axes in PyVista."""
    
    def __init__(self, plotter, origin=None, scale=1.0):
        """
        Initialize the axes visualizer.
        
        Args:
            plotter: PyVista plotter instance
            origin: Origin position [x, y, z], defaults to [0, 0, 0]
            scale: Scale factor for axis length
        """
        self.plotter = plotter
        self.origin = np.array(origin if origin is not None else [0, 0, 0])
        self.scale = scale
        self.actors = []
        self._create_axes()
    
    def _create_axes(self):
        """Create the initial axes actors."""
        self.actors = []
        
        # X axis (red)
        x_axis = pv.Line(self.origin, self.origin + np.array([self.scale, 0, 0]))
        self.actors.append(self.plotter.add_mesh(x_axis, color='red', line_width=2))
        
        # Y axis (green)
        y_axis = pv.Line(self.origin, self.origin + np.array([0, self.scale, 0]))
        self.actors.append(self.plotter.add_mesh(y_axis, color='green', line_width=2))
        
        # Z axis (blue)
        z_axis = pv.Line(self.origin, self.origin + np.array([0, 0, self.scale]))
        self.actors.append(self.plotter.add_mesh(z_axis, color='blue', line_width=2))
    
    def update(self, position=None, rotation=None):
        """
        Update the axes position and orientation using position and Rodrigues vector.
        
        Args:
            position: New origin position [x, y, z]
            rotation: Rotation object or Rodrigues rotation vector [rx, ry, rz]
        """
        if position is not None:
            self.origin = np.array(position)
        
        # Default axis directions
        axes_directions = [
            np.array([self.scale, 0, 0]),  # X axis
            np.array([0, self.scale, 0]),  # Y axis
            np.array([0, 0, self.scale]),  # Z axis
        ]
        
        # Apply Rodrigues rotation if provided
        if rotation is not None:
            if isinstance(rotation, np.ndarray) and rotation.shape == (3,):
                rotation = Rotation.from_rotvec(rotation)
            else:
                rotation = Rotation.from_matrix(rotation)
            axes_directions = [rotation.apply(direction) for direction in axes_directions]
        
        # Update axis endpoints
        for direction, idx in zip(axes_directions, range(3)):
            self.actors[idx].mapper.dataset.points = np.array([
                self.origin,
                self.origin + direction
            ])
    
    def plot_path(self, p1, p2, color='yellow', line_width=2):
        """
        Plot a path defined by a series of points.
        
        Args:
            points: Array of points defining the path [[x1, y1, z1], [x2, y2, z2], ...]
            color: Color of the path
            line_width: Width of the path line
        """
        path = pv.Line(p1, p2)
        actor = self.plotter.add_mesh(path, color=color, line_width=line_width)
        return actor

class ArrowVisualizer:
    """A class to visualize an arrow in PyVista."""
        
    def __init__(self, plotter, origin=None, direction=None, scale=1.0, color='white'):
        """
        Initialize the arrow visualizer.
        
        Args:
            plotter: PyVista plotter instance
            origin: Origin position [x, y, z], defaults to [0, 0, 0]
            direction: Direction vector [x, y, z], defaults to [1, 0, 0]
            scale: Scale factor for arrow length
            color: Color of the arrow
        """
        self.plotter = plotter
        self.origin = np.array(origin if origin is not None else [0, 0, 0])
        self.direction = np.array(direction if direction is not None else [1, 0, 0])
        self.scale = scale
        self.color = color
        self.actor = None
        self._create_arrow()
    
    def _create_arrow(self):
        """Create the initial arrow actor."""
        arrow = pv.Arrow(start=self.origin, direction=self.direction, scale=self.scale)
        self.actor = self.plotter.add_mesh(arrow, color=self.color)
    
    def update(self, origin=None, direction=None):
        """
        Update the arrow origin and direction.
        
        Args:
            origin: New origin position [x, y, z]
            direction: New direction vector [x, y, z]
        """
        if origin is not None:
            self.origin = np.array(origin)
        if direction is not None:
            self.direction = np.array(direction)
        
        arrow = pv.Arrow(start=self.origin, direction=self.direction,scale= self.scale * np.linalg.norm(self.direction))
        self.actor.mapper.dataset = arrow
