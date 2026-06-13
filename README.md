# robot_visualization

PyVista-based 3D visualization of URDF robots: render robots, update joint
configurations and plot end-effector markers, frames, and paths, etc.
Uses fork of [urdfpy](https://github.com/mmatl/urdfpy) (git
submodule) for URDF parsing — installing this package also installs `urdfpy`.

> **Note:** this repository is usually consumed as a submodule of
> [robot_tools](https://github.com/MaximilianDio/robot_tools), whose single
> `pip install` already includes it. Install standalone only if you need just
> the visualization.

## Installation (standalone)

```bash
git clone --recursive https://github.com/MaximilianDio/robot_visualization.git
pip install ./robot_visualization
```

Requires Python ≥ 3.10 and pip ≥ 23. If you cloned without `--recursive`, run
`git submodule update --init --recursive` first.

## Quickstart

```python
import numpy as np
import pyvista as pv
from robot_visualization import Robot

plotter = pv.Plotter()
robot = Robot("path/to/robot.urdf", plotter, color="lightblue", opacity=1.0)
robot.set_robot_mesh(id=0)

q0 = np.zeros(7)
q1 = np.array([1.0, 0.5, 0.0, -1.0, 0.0, 1.0, 0.0])
robot.update(q0, id=0)

# End-effector marker, frame, and path
path = np.linspace(q0, q1, 20)
robot.plot_ee(q1, ee_link_name="ee_link", color="red", size=0.02, type="sphere")
robot.plot_ee_frame(q1, ee_link_name="ee_link", scale=0.1)
robot.plot_ee_path(path, ee_link_name="ee_link", color="blue", line_width=4)

plotter.show()
```

Multiple instances of the same robot (e.g. start and goal configuration) are
handled via mesh ids:

```python
robot.set_robot_mesh(id=1)
robot.update(q1, id=1, opacity=0.4)
```

### Primitives

```python
from robot_visualization import AxesVisualizer, ArrowVisualizer, BoxVisualizer

axes = AxesVisualizer(plotter, origin=[0, 0, 0], scale=1.0)
axes.update(position=[1, 1, 1], rotation=np.array([0.1, 0.2, 0.3]))  # Rodrigues

arrow = ArrowVisualizer(plotter, origin=[0, 0, 0], direction=[1, 0, 0], color="red")
arrow.update(origin=[0.5, 0.5, 0.5], direction=[0, 1, 0])

box = BoxVisualizer(plotter, x_size=0.2, y_size=0.2, z_size=0.2, color="orange")
box.update(0, np.eye(4))
```

## API overview

| Object | Purpose |
|---|---|
| `Robot` | URDF robot mesh: `set_robot_mesh`, `update`, `fk`, `toggle_mesh_type`, `plot_ee`, `plot_ee_frame`, `plot_ee_path` |
| `AxesVisualizer` | RGB coordinate frame with `update(position, rotation)` |
| `ArrowVisualizer` | Single arrow with `update(origin, direction)` |
| `BoxVisualizer` | Pose-tracked boxes by id with `update(id, T)` |
| `video_utils` | FPS/timestamp/video-writer helpers used by robot_video_tools |

The full reference lives in the parent repository's
[API.md](https://github.com/MaximilianDio/robot_tools/blob/main/API.md).

## Troubleshooting

- **`ModuleNotFoundError: urdfpy`** — clone submodules
  (`git submodule update --init --recursive`) and reinstall. Do not install
  urdfpy from PyPI alongside this package.
- **Window not showing** — call `plotter.show()`; for headless use create the
  plotter with `off_screen=True` and use `plotter.screenshot(...)`.

## License

MIT
