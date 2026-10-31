import winsound

from models.point_cloud import *
from methods.neighborhood_variance import *

n = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
neighborhood_sizes = [10 * (i + 1) for i in range(20)]
n_components = 10

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):

    # point_cloud = PointCloud()
    # point_cloud.embeddings_constructor(embeddings_path, n)

    for neighborhood_size in neighborhood_sizes:
        filename = f'{i + 1}_{filename_prefix}_c{n_components}_k{neighborhood_size}'
        # calculate(point_cloud, neighborhood_size, n_components, filename)
        if neighborhood_size == 130:
            point_cloud = load_yaml(os.path.join(results_directory, f'{filename}_point_cloud.yaml'))
            visualize_variance(point_cloud, filename)

winsound.Beep(500, 3000)
