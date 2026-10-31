from utils.sample_generation import *
from utils.visualization_generation import *

n = 10000
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 3
figure_size = (2.2, 2.2)
pad = 0
point_size = 10

points = sample_from_sphere(n, intrinsic_dimension, r, seed, ambient_dimension)
points = np.array([p for p in points if p[0] <= 0])
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                    hide_color_bar=True, figure_name='sphere', figure_size=figure_size, pad=pad, point_size=point_size)

intrinsic_dimension = 3
points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
points = np.array([p for p in points if p[0] <= 0])
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                    hide_color_bar=True, figure_name='ball', figure_size=figure_size, pad=pad, point_size=point_size)

n = 4000
angle_in_degrees = 30
points = sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)
values = [p[0] for p in points]
plot_3d_scatterplot(points, values, hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                    hide_color_bar=True, figure_name='cones', figure_size=figure_size, pad=pad, point_size=point_size)

n1, n2 = 2000, 2000
r1, r2 = 1, 1
intrinsic_dimension = 2
seed1, seed2 = 1, 1
points = sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1, seed2, ambient_dimension)
points = np.array([p for p in points if p[1] >= 0])
values = [-1 * p[1] for p in points]
plot_3d_scatterplot(points, values, hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                    hide_color_bar=True, figure_name='planes', figure_size=figure_size, pad=pad, point_size=point_size)
