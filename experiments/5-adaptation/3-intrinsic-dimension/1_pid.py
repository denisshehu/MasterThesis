from methods.intrinsic_dimension_estimators.pid import *
from models.point_cloud import *

n = 20000
intrinsic_dimension_values = [i + 1 for i in range(10)]
r = 1
seed = 1
ambient_dimension = 300

neighborhood_size = 60
n_steps = 10

results = list()
for intrinsic_dimension in intrinsic_dimension_values:
    prefix = f'd{intrinsic_dimension}_k{neighborhood_size}'
    maximum_dimension = intrinsic_dimension + 1

    # points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    # point_cloud = PointCloud()
    # point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
    point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
    print(prefix)

    # estimate(point_cloud, neighborhood_size, maximum_dimension, n_steps=n_steps, filename_prefix=prefix)
    results.append([query.intrinsic_dimension for query in point_cloud.queries][0])

x_label, y_label = 'Intrinsic dimension', 'Estimated intrinsic dimension'
padding = 0.2
min_x, max_x = 0, intrinsic_dimension_values[-1] + padding
min_y, max_y = 0, intrinsic_dimension_values[-1] + padding
figure_size = (3.5, 3.5)
pad = 2.4
point_size = 3
line_width = 1
save_space = False
ticks = [0, 2, 4, 6, 8, 10]
plot_line_plot(intrinsic_dimension_values, results, x_label=x_label, y_label=y_label, min_x=min_x, max_x=max_x,
               min_y=min_y, max_y=max_y, plot_y_equals_x=True, figure_name='pid', figure_size=figure_size, pad=pad,
               point_size=point_size, line_width=line_width, save_space=save_space, x_ticks=ticks, y_ticks=ticks)
