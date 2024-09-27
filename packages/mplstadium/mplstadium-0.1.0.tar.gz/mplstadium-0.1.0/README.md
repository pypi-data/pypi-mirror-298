**A Python plotting library to visualize stadium data**

# Quick start

Install the package using `pip` (or `pip3`).

```
pip install mplstadium
```

Plot an outdoor 400m running track, with the origin at the centre of the track:


```python
from mplstadium.utils import OutdoorAthleticsTrack
from matplotlib import pyplot as plt

track = OutdoorAthleticsTrack()
fig, ax = track.draw(line_kwargs={"color": "black"})
plt.show()
```

<p align="center">
    <img src="figs/outdoor_athletics_track.png">
</p>

Plot an Olympic Velodrome in 3D and a trajectory on the surface:

```python
from utils import OlympicVelodrome
import numpy as np
from matplotlib import pyplot as plt

track = OlympicVelodrome()
fig, ax = track.draw_3d(color="peru", alpha=0.5)

s = np.linspace(0, 250, 250)
d = 4 + 4 * np.sin(s / 10)

track.trajectory(s, d, c="r")

ax.set_aspect("equal")
ax.axis("off")
plt.show()
```

<p align="center">
  <img src="figs/olympic_velodrome_3d_trajectory.png" width="75%">
</p>

Define a custom Stadium geometry and plot scatter points over it:

```python
from stadium import Stadium
import numpy as np
from matplotlib import pyplot as plt

track = Stadium(
    length=500,
    radius=24.37,
    width=12,
    straight_banking=0,
    curve_banking=20,
)
fig, ax = track.draw_3d(color="black", alpha=0.5)

s = np.linspace(0, 500, 50)
d = np.random.uniform(0, 12, 50)

track.scatter(s, d, c="r")

ax.set_aspect("equal")
ax.axis("off")
plt.show()
```

<p align="center">
  <img src="figs/custom_stadium_scatter.png" width="75%">
</p>

# License

[MIT](https://raw.githubusercontent.com/mlsedigital/mplbasketball/main/LICENSE.txt)