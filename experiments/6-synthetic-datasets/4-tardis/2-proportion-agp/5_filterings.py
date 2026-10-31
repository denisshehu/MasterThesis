from models.point_cloud import *
from methods.euclidicity import *

n = 10000
n1 = n // 2
intrinsic_dimension = 2
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = intrinsic_dimension

data = [
    ('regular', sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension), None),
    ('cones', sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension),
     90),
    ('planes', sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed, ambient_dimension),
     None)
]

neighborhood_size = 250
min_to_max_s_ratio = 1
r_to_s_ratio = 0.5
n_steps = 1
perform_scaling = True
filterings = [None, 'dynamic'] + [0.5 * i for i in range(5)]
n_queries = 10000
color_bar_min = None  # 0
color_bar_max = None  # 0.55

for filtering in filterings:
    for i, (string, points, roll) in enumerate(data):
        prefix = f'f{filtering}_{i + 1}_{string}'

        point_cloud = PointCloud()
        point_cloud.random_constructor(points, n_queries, seed)
        # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

        for query in point_cloud.queries:
            if i == 2:
                query.intrinsic_dimension = intrinsic_dimension - 1
            else:
                query.intrinsic_dimension = intrinsic_dimension

        calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling, filtering,
                  prefix)

        visualize_euclidicity(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max, roll=roll)
