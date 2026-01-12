# Robot Visualization

A Python package for visualizing robots using URDF files and PyVista. This package provides an easy-to-use interface for rendering robots, updating joint configurations, and visualizing end-effector positions and trajectories.

## Features

- Load and visualize robots from URDF files
- Update robot configurations in real-time
- Visualize end-effector positions and paths
- Coordinate axes and arrow visualization primitives
- Built on PyVista for interactive 3D rendering
- Includes urdfpy submodule for URDF parsing

## Installation

### Standard Installation

```bash
# Clone the repository with submodules
git clone --recursive https://github.com/MaximilianDio/robot_visualization.git
cd robot_visualization

# Install the package
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Basic Robot Visualization

```python
from robot_visualization import Robot
import pyvista as pv

# Create a plotter
plotter = pv.Plotter()

# Load a robot from URDF
robot = Robot("path/to/robot.urdf", plotter=plotter, color='lightgray', opacity=1.0)

# Set initial robot mesh
robot.set_robot_mesh()

# Show the visualization
plotter.show()
```

### Update Robot Configuration

```python
import numpy as np
from robot_visualization import Robot
import pyvista as pv

plotter = pv.Plotter()
robot = Robot("path/to/robot.urdf", plotter=plotter)

# Define joint configuration (adjust size based on your robot's DOF)
q = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

# Update robot to new configuration
robot.update(q)

plotter.show()
```

### Visualize End-Effector

```python
import numpy as np
from robot_visualization import Robot
import pyvista as pv

plotter = pv.Plotter()
robot = Robot("path/to/robot.urdf", plotter=plotter)

q = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
robot.update(q)

# Plot end-effector position
robot.plot_ee(q, ee_link_name="end_effector_link", color="red", size=0.02, type="sphere")

plotter.show()
```

### Plot End-Effector Path

```python
import numpy as np
from robot_visualization import Robot
import pyvista as pv

plotter = pv.Plotter()
robot = Robot("path/to/robot.urdf", plotter=plotter)

# Two different configurations
q1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
q2 = np.array([0.5, 0.4, 0.3, 0.2, 0.1, 0.0])

robot.update(q1)

# Plot path between two configurations
robot.plot_ee_path(q1, q2, ee_link_name="end_effector_link", color="blue", line_width=4)

plotter.show()
```

### Using Visualization Primitives

```python
from robot_visualization import AxesVisualizer, ArrowVisualizer
import pyvista as pv
import numpy as np

plotter = pv.Plotter()

# Create coordinate axes
axes = AxesVisualizer(plotter, origin=[0, 0, 0], scale=1.0)

# Update axes position and rotation
axes.update(position=[1, 1, 1], rotation=np.array([0.1, 0.2, 0.3]))

# Create an arrow
arrow = ArrowVisualizer(plotter, origin=[0, 0, 0], direction=[1, 0, 0], scale=0.5, color='red')

# Update arrow
arrow.update(origin=[0.5, 0.5, 0.5], direction=[0, 1, 0])

plotter.show()
```

## API Reference

### Robot Class

Main class for robot visualization.

**Constructor:**
```python
Robot(urdf_file, plotter=None, **kwargs)
```
- `urdf_file` (str): Path to the URDF file
- `plotter` (pv.Plotter, optional): PyVista plotter instance
- `color` (str, optional): Robot mesh color (default: 'lightgray')
- `opacity` (float, optional): Robot mesh opacity (default: 1.0)

**Methods:**
- `set_robot_mesh()`: Initialize and render the robot mesh
- `update(q)`: Update robot configuration with joint angles
- `plot_ee(q, ee_link_name, color, **kwargs)`: Plot end-effector position
  - `type`: 'sphere', 'cube', or 'cross'
  - `size`: Size of the marker
- `plot_ee_path(q1, q2, ee_link_name, color, opacity, line_width)`: Plot path between configurations

### AxesVisualizer Class

Visualize 3D coordinate axes.

**Constructor:**
```python
AxesVisualizer(plotter, origin=None, scale=1.0)
```

**Methods:**
- `update(position, rotation)`: Update axes position and orientation
- `plot_path(p1, p2, color, line_width)`: Plot a line between two points

### ArrowVisualizer Class

Visualize 3D arrows.

**Constructor:**
```python
ArrowVisualizer(plotter, origin=None, direction=None, scale=1.0, color='white')
```

**Methods:**
- `update(origin, direction)`: Update arrow position and direction

## Dependencies

This package requires:
- Python >= 3.7
- numpy
- pyvista
- scipy
- lxml
- networkx
- pillow
- pycollada
- pyrender
- trimesh
- six

All dependencies are automatically installed via pip.

## URDF Submodule

This package includes the [urdfpy](https://github.com/MaximilianDio/urdfpy) library as a git submodule. When installing with pip, all urdfpy dependencies are automatically included.

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Examples

See the examples directory for more usage examples (if available).

## Troubleshooting

### ImportError: No module named 'urdfpy'

Make sure you cloned the repository with submodules:
```bash
git submodule update --init --recursive
```

### Visualization window not showing

Make sure you call `plotter.show()` at the end of your script.

### Robot not updating

Make sure to call `robot.update(q)` after changing joint configurations.
