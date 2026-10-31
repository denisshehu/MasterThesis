import winsound

from models.point_cloud import *
from methods.intrinsic_dimension_estimators.danco import *

n = 300
embeddings_paths = [word2vec_embeddings_path, fasttext_embeddings_path, glove_embeddings_path]
filename_prefixes = ['word2vec', 'fasttext', 'glove']
min_neighborhood_size = 30
max_neighborhood_size = 45

for i, (embeddings_path, filename_prefix) in enumerate(zip(embeddings_paths, filename_prefixes)):
    filename = f'{i + 1}_{filename_prefix}_{min_neighborhood_size}_{max_neighborhood_size}'

    # point_cloud = PointCloud()
    # point_cloud.embeddings_constructor(embeddings_path, n)
    point_cloud = load_yaml(os.path.join(results_directory, f'{filename}_point_cloud.yaml'))

    # estimate(point_cloud, min_neighborhood_size, max_neighborhood_size, filename)
    visualize_dimension(point_cloud, filename, include_individual_plots=False, color_bar_min=15, color_bar_max=65)

winsound.Beep(500, 3000)
