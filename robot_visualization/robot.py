from typing import List
from urdfpy import URDF
import pyvista as pv
import numpy as np


class Robot:

    def __init__(self, urdf_file : str, plotter=None, **kwargs):
        """
        Initialize the Robot class with a URDF file and a PyVista plotter.

        Args:
            urdf_file (str): Path to the URDF file of the robot.
            plotter (pv.Plotter, optional): Optional PyVista plotter instance. If None, a new plotter will be created.
            color (str, optional): Color of the robot mesh. Default is 'lightgray'.
            opacity (float, optional): Opacity of the robot mesh. Default is 1.0.
            **kwargs: Additional keyword arguments for future extensions.
        """

        # Get additional visualization arguments
        self.mesh_color = kwargs.get('color', 'lightgray')
        self.mesh_opacity = kwargs.get('opacity', 1.0)

        # Load the URDF file
        self.robot = URDF.load(urdf_file)

        if plotter is None:
            self.plotter = pv.Plotter()
        else:
            self.plotter = plotter

        self.mesh_actors = {}

    def set_robot_mesh(self):
        fk = self.robot.visual_trimesh_fk()

        for tm in fk:
            pose = fk[tm]
            # Convert trimesh to pyvista mesh
            pv_mesh = pv.wrap(tm)
            # Apply pose transformation
            transform = np.eye(4)
            transform[:3, :3] = pose[:3, :3]
            transform[:3, 3] = pose[:3, 3]
            pv_mesh.transform(transform, inplace=True)
            # Add mesh to plotter
            actor = self.plotter.add_mesh(pv_mesh, color=self.mesh_color, opacity=self.mesh_opacity)
            self.mesh_actors[tm] = (pv_mesh, actor)

    def update(self, q):
        if not self.mesh_actors:
            self.set_robot_mesh()

        fk = self.robot.visual_trimesh_fk(q)
        for tm in fk:
            pose = fk[tm]
            pv_mesh, actor = self.mesh_actors[tm]
            # Reset mesh to original and apply new pose
            pv_mesh.points = pv.wrap(tm).points
            transform = np.eye(4)
            transform[:3, :3] = pose[:3, :3]
            transform[:3, 3] = pose[:3, 3]  
            pv_mesh.transform(transform, inplace=True)
            # No need to update actor, as mesh is updated in-place

    def plot_ee(self, q, ee_link_name="CS_6", color="red", **kwargs):
        """
        Plot the end-effector position for a given joint configuration.

        Args:
            q (np.ndarray): Joint configuration of the robot.
            ee_link_name (str): Name of the end-effector link.
        """
        T_EE = self.robot.link_fk(q, ee_link_name)

        # Plot a low-res red sphere at the end-effector position
        ee_pos = T_EE[:3, 3]

        # if radius is provided in kwargs, use it; otherwise, default to 0.01
        size = kwargs.get("size", 0.01)
        type = kwargs.get("type", "sphere")

        if type == "sphere":
            sphere = pv.Sphere(radius=size / 2, center=ee_pos)
            self.plotter.add_mesh(sphere, color=color)
        elif type == "cube":
            cube = pv.Cube(center=ee_pos, x_length=size, y_length=size, z_length=size)
            self.plotter.add_mesh(cube, color=color)
        elif type == "cross":
            line1 = pv.Line(
                ee_pos - np.array([size / 2, 0, 0]), ee_pos + np.array([size / 2, 0, 0])
            )
            line2 = pv.Line(
                ee_pos - np.array([0, size / 2, 0]), ee_pos + np.array([0, size / 2, 0])
            )
            line3 = pv.Line(
                ee_pos - np.array([0, 0, size / 2]), ee_pos + np.array([0, 0, size / 2])
            )
            self.plotter.add_mesh(line1, color=color, line_width=4)
            self.plotter.add_mesh(line2, color=color, line_width=4)
            self.plotter.add_mesh(line3, color=color, line_width=4)

    def plot_ee_path(self, q1, q2, ee_link_name="CS_6", color=None, opacity=1.0, line_width=4):

        T_EE_1 = self.robot.link_fk(q1, ee_link_name)
        T_EE_2 = self.robot.link_fk(q2, ee_link_name)

        if color is None:
            color = self.mesh_color


        # Plot a low-res red sphere at the end-effector position
        ee_pos_1 = T_EE_1[:3, 3]
        ee_pos_2 = T_EE_2[:3, 3]
        # Draw a line between the two end-effector positions
        line = pv.Line(ee_pos_1, ee_pos_2)

        actor = self.plotter.add_mesh(line, color=color, opacity=opacity, line_width=line_width)
        return actor
        # self.plotter.add_lines(np.array([ee_pos_1, ee_pos_2]), color=color, width=4, opacity=opacity)  # Draw line between EE positions