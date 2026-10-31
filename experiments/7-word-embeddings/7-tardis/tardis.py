import winsound

from methods.euclidicity import *

n = 300
filename_prefixes = ['word2vec', 'fasttext', 'glove']

neighborhood_sizes = [10 * (i + 1) for i in range(20)]
upper_bounds = [{10: None, 20: None, 30: None, 40: 13, 50: 8, 60: 7, 70: 6, 80: 5, 90: 5, 100: 5,
                110: 4, 120: 4, 130: 4, 140: 4, 150: 4, 160: 4, 170: 4, 180: 4, 190: 4, 200: 3},
                {10: None, 20: None, 30: None, 40: 12, 50: 8, 60: 7, 70: 6, 80: 5, 90: 5, 100: 5,
                 110: 4, 120: 4, 130: 4, 140: 4, 150: 4, 160: 4, 170: 4, 180: 4, 190: 4, 200: 3},
                {10: None, 20: None, 30: None, 40: 9, 50: 7, 60: 6, 70: 5, 80: 5, 90: 5, 100: 4,
                 110: 4, 120: 4, 130: 4, 140: 4, 150: 4, 160: 4, 170: 4, 180: 4, 190: 3, 200: 3}]
min_to_max_s_ratio = 1
r_to_s_ratio = 0.5
n_steps = 1
perform_scaling = True
filtering = None

color_bar_min = 0.29
color_bar_max = 0.49

for i, filename_prefix in enumerate(filename_prefixes):
    for neighborhood_size in neighborhood_sizes:
        if ((filename_prefix == 'word2vec' and neighborhood_size == 110) or
                (filename_prefix == 'fasttext' and neighborhood_size == 100) or
                (filename_prefix == 'glove' and neighborhood_size == 90)):
            upper_bound = upper_bounds[i][neighborhood_size]
            prefix = f'{i + 1}_{filename_prefix}_k{neighborhood_size}_ub{upper_bound}'

            # point_cloud = load_yaml(os.path.join(results_directory, f'{i + 1}_{filename_prefix}_30_45_point_cloud.yaml'))
            point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

            # for query in point_cloud.queries:
            #     if upper_bound is not None:
            #         query.intrinsic_dimension = upper_bound

            # calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, perform_scaling, filtering,
            #           prefix)
            visualize_euclidicity(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)

winsound.Beep(500, 3000)
