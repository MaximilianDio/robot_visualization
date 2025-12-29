from setuptools import setup, find_packages

setup(
    name='robot_visualization',
    version='0.1.0',
    packages=find_packages(include=['robot_visualization', 'robot_visualization.*',
                                    'urdfpy', 'urdfpy.*']),
    install_requires=[
        # 'urdfpy',
        'pyvista',
        'numpy',
    ]
)