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
        self.p0 = kwargs.get('p0', np.zeros(3))
        self.R0 = kwargs.get('R0', np.eye(3))
        
        self.T0 = np.eye(4)
        self.T0[:3, :3] = self.R0
        self.T0[:3, 3] = self.p0

        # Load the URDF file
        self.robot = URDF.load(urdf_file)

        if plotter is None:
            self.plotter = pv.Plotter()
        else:
            self.plotter = plotter

        self.mesh_actors = {}
        self.id_list = []

    def set_robot_mesh(self, id = 0, color= None, opacity=None):
        
        self.id_list.append(id)
        
        if color is None:
            color = self.mesh_color
        if opacity is None:
            opacity = self.mesh_opacity 
            
        fk = self.robot.visual_trimesh_fk()

        for tm in fk:
            pose = fk[tm]
            # transform to base frame
            pose = self.T0 @ pose
            
            # Convert trimesh to pyvista mesh
            pv_mesh = pv.wrap(tm)
            # Apply pose transformation
            transform = np.eye(4)
            transform[:3, :3] = pose[:3, :3]
            transform[:3, 3] = pose[:3, 3]
            pv_mesh.transform(transform, inplace=True)
            # Add mesh to plotter
            actor = self.plotter.add_mesh(pv_mesh, color=color, opacity=opacity)
            self.mesh_actors[(tm,id)] = (pv_mesh, actor)
            
    def fk(self, q, ee_link_name="CS_6"):
        """ Generate forward kinemaics for given joint configuration."""
        pose = self.robot.link_fk(q, ee_link_name)
        # transform to base frame
        pose = self.T0 @ pose
        
        return pose
    
    def update(self, q, id = 0):
        if not self.mesh_actors:
            self.set_robot_mesh(id=id)
        
        if id not in self.id_list:
            self.set_robot_mesh(id=id)

        fk = self.robot.visual_trimesh_fk(q)
        for tm in fk:
            pose = fk[tm]
            # transform to base frame
            pose = self.T0 @ pose
            
            pv_mesh, actor = self.mesh_actors[(tm,id)]
            # Reset mesh to original and apply new pose
            pv_mesh.points = pv.wrap(tm).points
            transform = np.eye(4)
            transform[:3, :3] = pose[:3, :3]
            transform[:3, 3] = pose[:3, 3]  
            pv_mesh.transform(transform, inplace=True)
            # No need to update actor, as mesh is updated in-place

    def plot_ee(self, q, Tgp = np.eye(4), ee_link_name="CS_6", color="red", **kwargs):
        """
        Plot the end-effector position for a given joint configuration.

        Args:
            q (np.ndarray): Joint configuration of the robot.
            Tgp (np.ndarray): Transformation from end-effector to gripper pose (default is identity).
            ee_link_name (str): Name of the end-effector link.
        """
        # Compute end-effector pose
        ee_pose = self.fk(q, ee_link_name) @ Tgp
        # Extract end-effector position
        ee_pos = ee_pose[:3, 3]
        
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
    
    def plot_ee_frame(self, q, Tgp = np.eye(4), ee_link_name="CS_6"):
        """
        Plot the end-effector position for a given joint configuration.

        Args:
            q (np.ndarray): Joint configuration of the robot.
            ee_link_name (str): Name of the end-effector link.
        """
        pose = self.fk(q, ee_link_name) @ Tgp

        # Plot a low-res red sphere at the end-effector position
        ee_pos = pose[:3, 3]

        # Plot a coordinate frame at the end-effector
        axes = pv.Arrow(start=ee_pos, direction=pose[:3, 0], scale=0.05)
        self.plotter.add_mesh(axes, color='r')
        axes = pv.Arrow(start=ee_pos, direction=pose[:3, 1], scale=0.05)
        self.plotter.add_mesh(axes, color='g')
        axes = pv.Arrow(start=ee_pos, direction=pose[:3, 2], scale=0.05)
        self.plotter.add_mesh(axes, color='b')

    def plot_ee_path(self, path, Tgp = np.eye(4), ee_link_name="CS_6", color=None, opacity=1.0, line_width=4):
        """
        Plot the end-effector path for a given sequence of joint configurations.
        """
        if color is None:
            color = self.mesh_color
        
        pos = []
        for q in path:
            pose = self.fk(q, ee_link_name) @ Tgp
            pos.append(pose[:3, 3])
        
        mesh = pv.lines_from_points(np.array(pos), close=False)         
        actor = self.plotter.add_mesh(mesh, color=color, line_width=line_width, opacity=self.mesh_opacity)

        return actor