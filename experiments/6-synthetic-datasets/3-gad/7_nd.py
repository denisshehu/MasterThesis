from methods.gad import *
from models.point_cloud import *

n = 200 + 2
n1 = n // 2
intrinsic_dimensions = [i for i in range(2, 6)]
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = 300
neighborhood_size = n - 2
min_to_max_s_ratio = 1
r_to_s_ratio = 0.7
n_steps = 1

summary = ''

for intrinsic_dimension in intrinsic_dimensions:
    summary += f'd = {intrinsic_dimension}, k = {neighborhood_size}: '

    data = [
        ('regular', sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)),
        ('cones', sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension)),
        ('planes', sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed,
                                                   ambient_dimension))
    ]

    for i, (string, points) in enumerate(data):
        prefix = f'd{intrinsic_dimension}_k{neighborhood_size}_{i + 1}_{string}'

        # point_cloud = PointCloud()
        # point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
        point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
        print(prefix)

        # for query in point_cloud.queries:
        #     if i == 2:
        #         query.intrinsic_dimension = intrinsic_dimension - 1
        #     else:
        #         query.intrinsic_dimension = intrinsic_dimension

        # detect(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, prefix)
        summary += f'{string} classified as {[query.classification for query in point_cloud.queries][0]}, '
    summary += '\n'

file_path = os.path.join(results_directory, f'summary_d{intrinsic_dimensions[0]}_{intrinsic_dimensions[-1]}.txt')
with open(file_path, 'w') as file:
    file.write(summary)
