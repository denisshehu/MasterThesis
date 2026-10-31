import winsound

from models.point_cloud import *
from methods.topological_polysemy import *

n = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']

neighborhood_sizes = [10 * (i + 1) for i in range(20)]
min_to_max_s_ratio = 1
r_to_s_ratio = 0.1
n_steps = 1

limits = {10: (3, 6), 20: (6, 10), 30: (10, 15), 40: (13, 19), 50: (17, 24), 60: (20, 28), 70: (24, 32), 80: (26, 36),
          90: (31, 41), 100: (33, 45), 110: (36, 49), 120: (39, 53), 130: (42, 57), 140: (46, 62), 150: (48, 66),
          160: (51, 69), 170: (56, 73), 180: (59, 77), 190: (62, 82), 200: (65, 86)}

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):
    for neighborhood_size in neighborhood_sizes:
        if ((filename_prefix == 'word2vec' and neighborhood_size == 170) or
                (filename_prefix == 'fasttext' and neighborhood_size == 180) or
                (filename_prefix == 'glove' and neighborhood_size == 110)):
            prefix = f'{i + 1}_{filename_prefix}_{neighborhood_size}'

            # point_cloud = PointCloud()
            # point_cloud.embeddings_constructor(embeddings_path, n)
            point_cloud = load_yaml(os.path.join(results_directory, f'{prefix}_point_cloud.yaml'))

            # calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)

            x_min, x_max = limits[neighborhood_size]
            if neighborhood_size == 170:
                x_min, x_max = 61, 73
            elif neighborhood_size == 180:
                x_min, x_max = 65, 77
            elif neighborhood_size == 110:
                x_min, x_max = 36, 49
            visualize_topological_polysemy(point_cloud, prefix, color_bar_min=x_min, color_bar_max=x_max)

winsound.Beep(500, 3000)
