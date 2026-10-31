from methods.euclidicity import *
from models.point_cloud import *

n = 20000
intrinsic_dimension = 2
r_values = [pow(10, i) for i in range(5)]
seed = 1
ambient_dimension = 2
neighborhood_size = 50
n_steps = 10

not_scaled = list()
scaled = list()

for i, (string, perform_scaling) in enumerate([('not_scaled', False), ('scaled', True)]):
    for r in r_values:
        prefix = f'{i + 1}_{string}_r{r}'

        points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
        point_cloud = PointCloud()
        point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
        # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

        for query in point_cloud.queries:
            query.intrinsic_dimension = intrinsic_dimension

        calculate(point_cloud, neighborhood_size, n_steps=n_steps, perform_scaling=perform_scaling,
                  filename_prefix=prefix)

        if i == 0:
            not_scaled.append([query.euclidicity for query in point_cloud.queries])
        else:
            scaled.append([query.euclidicity for query in point_cloud.queries])

y1_label, y2_label = 'Without scaling', 'With scaling'
x_label, y_label = 'Radius', 'Euclidicity score'
min_y, max_y = 0, 0.4
figure_size = (3.5, 3.5)
pad = 2.4
point_size = 3
line_width = 1
save_space = False
plot_line_plot(r_values, not_scaled, scaled, y1_label=y1_label, y2_label=y2_label, x_label=x_label, y_label=y_label,
               use_x_log_scale=True, use_y_log_scale=True, figure_name='scaling', figure_size=figure_size, pad=pad,
               point_size=point_size, line_width=line_width, save_space=save_space)
