from methods.intrinsic_dimension_estimators.danco import *
from models.point_cloud import *

n = 20000
intrinsic_dimension_values = [2, 5, 10, 20, 50, 100]
r = 1
seed = 1
ambient_dimension = 300
min_neighborhood_size = 0
max_neighborhood_size = 50

for intrinsic_dimension in intrinsic_dimension_values:
    prefix = f'd{intrinsic_dimension}'

    # points = sample_from_ball(n, intrinsic_dimension, r, seed, ambient_dimension)
    # point_cloud = PointCloud()
    # point_cloud.non_random_constructor(points, np.array(ambient_dimension * [0]))
    point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

    # estimate(point_cloud, min_neighborhood_size, max_neighborhood_size, filename_prefix=prefix)
    visualize_dimension(point_cloud, prefix, known_dimension=intrinsic_dimension)
