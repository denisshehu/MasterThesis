from models.point_cloud import *
from methods.euclidicity import *

n1, n2 = 10000, 10000
intrinsic_dimension = 2
r1, r2 = 1, 1
seed1, seed2 = 1, 1
ambient_dimension = intrinsic_dimension + 1

neighborhood_size = 100
min_to_max_s_ratio = None
r_to_s_ratio = None
n_steps_values = [1, 2, 5, 10]
perform_scaling = True
n_queries = 10000
color_bar_min = None
color_bar_max = None

for n_steps in n_steps_values:
    prefix = f's{n_steps}'

    points = sample_from_intersecting_planes(n1, r1, n2, r2, intrinsic_dimension, seed1, seed2, ambient_dimension)
    point_cloud = PointCloud()
    point_cloud.random_constructor(points, n_queries, seed1)
    # point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

    for query in point_cloud.queries:
        query.intrinsic_dimension = intrinsic_dimension

    calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling, prefix)

    new_queries = list()
    for query in point_cloud.queries:
        if query.point[1] >= 0:
            new_queries.append(query)
    point_cloud.queries = new_queries

    visualize_euclidicity(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)
