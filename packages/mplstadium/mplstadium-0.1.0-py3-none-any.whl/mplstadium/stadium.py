from typing import Tuple, Union
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Stadium:

    """
    A class to represent a stadium-shaped track and facilitate plots of and on its surface.

    Attributes
    ----------
    length : float
        The length of the track.
    radius : float
        The radius of the track.
    width : float
        The width of the track.
    straight_banking : float
        The banking angle (deg) of the straight sections of the track.
    curve_banking : float
        The banking angle (deg) of the curved sections of the track.

    """

    def __init__(
        self, 
        length: float,
        radius: float,
        width: float, 
        straight_banking: float,
        curve_banking: float,
    ):
        self.length = length
        self.radius = radius
        self.width = width
        self.straight_banking = straight_banking
        self.curve_banking = curve_banking

        self._q_straight: float = (self.length - 2 * np.pi * self.radius) / 4
        self._ax: Union[plt.Axes , Axes3D] = None
        self._projection = Union[str, None]

    def _banking(self, s) -> float:
        return np.pi * (
            ((self.straight_banking + self.curve_banking) / 2) 
            - (self.curve_banking - self.straight_banking)/2 * np.cos(4 * (s / self.length) * np.pi)
        ) / 180
    
    def _transform_xyz(self, s, d) -> Tuple[float, float, float]:
        s = s % self.length
        banking_angle = self._banking(s)
        d_xy = d * np.cos(banking_angle)
        d_z = d * np.sin(banking_angle)
        if s < self._q_straight:
            return (
                s, 
                -1 * (self.radius + d_xy), 
                d_z
            )
        elif s < self._q_straight + np.pi * self.radius:
            angle = (s - self._q_straight) / self.radius
            return (
                self._q_straight + (self.radius + d_xy) * np.sin(angle), 
                -1 * (self.radius + d_xy) * np.cos(angle), 
                d_z
            )
        elif s < 3 * self._q_straight + np.pi * self.radius:
            return (
                2 * self._q_straight + np.pi * self.radius - s, 
                self.radius + d_xy, 
                d_z
            )
        elif s < 3 * self._q_straight + 2 * np.pi * self.radius:
            angle = (s - (3 * self._q_straight + np.pi * self.radius)) / self.radius
            return (
                -1 * self._q_straight - (self.radius + d_xy) * np.sin(angle), 
                (self.radius + d_xy) * np.cos(angle), 
                d_z
            )
        else:
            return (
                s - 4 * self._q_straight - 2 * np.pi * self.radius, 
                -1 * (self.radius + d_xy), 
                d_z
            )
        
    def _init_ax(self, ax: plt.Axes, projection=None):
        self._ax = ax
        if self._ax is None:
            self.fig = plt.figure()
            self._ax = self.fig.add_subplot(111, projection=projection)
            self._projection = projection
        else:
            if self._projection != projection:
                raise ValueError("Cannot change projection of existing axis")

    
    def draw(
        self,
        ax: plt.Axes = None,
        line_args: list = [],
        line_kwargs: dict = {},
        fill_args: list = [],
        fill_kwargs: dict = {},
        s_points: int = 250,
        d_points: int = 9,
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot the stadium in 2D.
        
        Parameters
        ----------
        ax : plt.Axes
            The axis to plot on.
        fill_color : str
            The color to fill the stadium with.
        fill_alpha : float
            The alpha value of the fill color.
        edge_color : str
            The color of the edges of the stadium.
        edge_alpha : float
            The alpha value of the edge color.
        s_points : int
            The number of points to use in the tangential direction.

        """
        assert d_points >= 2, "d_points must be at least 2"

        self._init_ax(ax)

        all_s = np.linspace(0, self.length, s_points)
        all_d = np.linspace(0, self.width, d_points)

        lines = [
            np.array([self._transform_xyz(s, d) for s in all_s]) for d in all_d
        ]

        for line in lines:
            self._ax.plot(line[:, 0], line[:, 1], *line_args, **line_kwargs)

        self._ax.fill(lines[-1][:, 0], lines[-1][:, 1], *fill_args, **fill_kwargs)
        self._ax.fill(lines[0][:, 0], lines[0][:, 1], color="white", alpha=1)

        return self.fig, self._ax
    
    def draw_3d(
        self,
        ax: plt.Axes = None,
        s_points: int = 250,
        d_points: int = 10,
        *args,
        **kwargs,
    ) -> tuple[plt.Figure, plt.Axes]:
        """
        Plot the stadium in 3D.
        
        Parameters
        ----------
        ax : plt.Axes
            The axis to plot on.
        s_points : int
            The number of points to use in the tangential direction.
        d_points : int
            The number of points to use in the radial direction.
        args: list
            Additional positional arguments to pass to the plot
            function.
        kwargs: dict
            Additional keyword arguments to pass to the plot
            function.

        """
        assert d_points >= 2, "d_points must be at least 2"

        self._init_ax(ax, projection="3d")

        s = np.linspace(0, self.length, s_points)
        d = np.linspace(0, self.width, d_points)

        points = np.array([
            [self._transform_xyz(s_, d_) for s_ in s] for d_ in d
        ])

        self._ax.plot_surface(
            points[:,:,0], 
            points[:,:,1], 
            points[:,:,2], 
            *args,
            **kwargs,
        )

        return self.fig, self._ax
    
    def trajectory(
        self,
        s: np.ndarray,
        d: np.ndarray,
        *args,
        **kwargs,
    ):
        """
        Plot a trajectory on the stadium.
        
        Parameters
        ----------
        s : np.ndarray
            The tangential position of the trajectory.
        d : np.ndarray
            The radial of the trajectory.
        args : list
            Additional positional arguments to pass to the plot
            function.
        kwargs : dict
            Additional keyword arguments to pass to the plot
            function.
        
        """
        points = np.array([
            self._transform_xyz(s_, d_) for s_, d_ in zip(s, d)
        ])

        if self._projection == "3d":
            self._ax.plot(points[:, 0], points[:, 1], points[:, 2], *args, **kwargs)
        else:
            self._ax.plot(points[:, 0], points[:, 1], *args, **kwargs)
        
        return self.fig, self._ax
    
    def scatter(
        self,
        s: np.ndarray,
        d: np.ndarray,
        *args,
        **kwargs,
    ):
        """
        Scatter points on the stadium.

        Parameters
        ----------
        s : np.ndarray
            The tangential position of the points.
        d : np.ndarray
            The radial of the points.
        args : list
            Additional positional arguments to pass to the scatter
            function.
        kwargs : dict
            Additional keyword arguments to pass to the scatter
            function.
        
        """
        points = np.array([
            self._transform_xyz(s_, d_) for s_, d_ in zip(s, d)
        ])

        if self._projection == "3d":
            self._ax.scatter(points[:, 0], points[:, 1], points[:, 2], *args, **kwargs)
        else:
            self._ax.scatter(points[:, 0], points[:, 1], *args, **kwargs)
        
        return self.fig, self._ax
