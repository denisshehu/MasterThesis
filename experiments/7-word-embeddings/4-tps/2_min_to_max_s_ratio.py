import winsound

from models.point_cloud import *
from methods.topological_polysemy import *

n = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']

neighborhood_size = 100
min_to_max_s_ratios = [1 - 0.1 * i for i in range(10)]
r_to_s_ratio = 0.1
n_steps_values = [2, 5, 10, 20]

color_bar_min = None
color_bar_max = None

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):
    for n_steps in n_steps_values:
        for min_to_max_s_ratio in min_to_max_s_ratios:
            prefix = f'{i + 1}_{filename_prefix}_s{n_steps}_mms{min_to_max_s_ratio:.1f}'

            point_cloud = PointCloud()
            point_cloud.embeddings_constructor(embeddings_path, n)

            calculate(point_cloud, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps, filename_prefix=prefix)
            visualize_topological_polysemy(point_cloud, prefix, color_bar_min=color_bar_min, color_bar_max=color_bar_max)

winsound.Beep(500, 3000)
