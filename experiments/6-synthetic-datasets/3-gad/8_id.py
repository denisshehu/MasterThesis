from methods.intrinsic_dimension_estimators.danco import estimate
from models.point_cloud import *

n = 20000
n1 = n // 4
intrinsic_dimension = 2
r = 1
seed = 1
ambient_dimension = 3

n_queries = 10000
min_neighborhood_size = 20
max_neighborhood_size = 20

prefix = 'id'
points = sample_from_intersecting_planes(n1, r, n1, r, intrinsic_dimension, seed, seed, ambient_dimension)
point_cloud = PointCloud()
point_cloud.random_constructor(points, n_queries, seed)
# point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

estimate(point_cloud, min_neighborhood_size, max_neighborhood_size, filename_prefix=prefix)

new_queries = list()
for query in point_cloud.queries:
    if query.point[1] >= 0:
        new_queries.append(query)
point_cloud.queries = new_queries

visualize_dimension(point_cloud, prefix, include_individual_plots=False)
