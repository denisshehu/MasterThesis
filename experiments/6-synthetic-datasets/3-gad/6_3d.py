import winsound

from models.point_cloud import *
from methods.gad import *

n = 20000
n1 = n // 4
intrinsic_dimension = 3
r = 1
angle_in_degrees = 30
seed = 1
ambient_dimension = intrinsic_dimension

data = [
    ('regular', sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension), 0, 270),
    ('cones', sample_from_intersecting_cones(n, intrinsic_dimension, r, angle_in_degrees, seed, ambient_dimension),
     0, 270),
    ('planes', sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension - 1, seed, seed, ambient_dimension),
     None, None)
]

neighborhood_size = 150
min_to_max_s_ratio = 1
r_to_s_ratio = 0.7
n_steps = 1
n_queries = 10000

for i, (string, points, elev, azim) in enumerate(data):
    prefix = f'{i + 1}_{string}'

    # point_cloud = PointCloud()
    # point_cloud.random_constructor(points, n_queries, seed)
    point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))
    print(prefix)

    # for query in point_cloud.queries:
    #     if i == 2:
    #         query.intrinsic_dimension = intrinsic_dimension - 1
    #     else:
    #         query.intrinsic_dimension = intrinsic_dimension

    # detect(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)

    new_queries = list()
    for query in point_cloud.queries:
        if query.point[1] >= 0:
            new_queries.append(query)
    point_cloud.queries = new_queries

    hide_legend = True if i != 1 else False
    if i == 1:
        visualize_classification(point_cloud, prefix, elev=elev, azim=azim, hide_legend=hide_legend)

winsound.Beep(500, 3000)
