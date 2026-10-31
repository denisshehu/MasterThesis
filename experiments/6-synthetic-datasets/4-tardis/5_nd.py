import winsound

from methods.euclidicity import *
from models.point_cloud import *

n = 70 + 2
n1 = n // 2
intrinsic_dimensions = [i for i in range(2, 11)]
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = 300

neighborhood_size = n - 2
min_to_max_s_ratio = 1
r_to_s_ratio = 0.5
n_steps = 1
perform_scaling = True
filtering = None

summary = [[], [], []]

for intrinsic_dimension in intrinsic_dimensions:
    data = [
        ('regular', None),#sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)),
        ('cones', None),#sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)),
        ('planes', None),#sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed,
                                                   # ambient_dimension))
    ]

    for i, (string, points) in enumerate(data):
        prefix = f'd{intrinsic_dimension}_{i + 1}_{string}'

        # point_cloud = PointCloud()
        # point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
        point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
        print(prefix)

        # for query in point_cloud.queries:
        #     query.intrinsic_dimension = intrinsic_dimension

        # calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling, filtering,
        #           prefix)
        summary[i].append([query.euclidicity for query in point_cloud.queries][0])

y1_label, y2_label, y3_label = 'regular', 'singular (cones)', 'singular (planes)'
x_label = 'Intrinsic dimension'
y_label = 'Euclidicity score'
figure_name = f'summary_d{intrinsic_dimensions[0]}_{intrinsic_dimensions[-1]}'
figure_size = (4.9, 3)
pad = 2.4
point_size = 3
line_width = 1
save_space = False
plot_line_plot(intrinsic_dimensions, summary[0], summary[1], summary[2], y1_label, y2_label, y3_label, x_label, y_label,
               min_y=0, figure_name=figure_name, figure_size=figure_size, pad=pad,
               point_size=point_size, line_width=line_width, save_space=save_space)

winsound.Beep(500, 3000)
