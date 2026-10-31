from utils.main import *


def execute(point_cloud, neighborhood_size, maximum_dimension, n_steps, filename_prefix=None, keep_terminal_open=False):
    output_path = _execute(point_cloud, neighborhood_size, maximum_dimension, n_steps, filename_prefix,
                           keep_terminal_open)
    update_point_cloud(point_cloud, output_path)
    save_point_cloud(point_cloud, filename_prefix)


def _execute(point_cloud, neighborhood_size, maximum_dimension, n_steps, filename_prefix, keep_terminal_open):
    points = point_cloud.points
    query_points = point_cloud.get_query_points()

    filename_prefix = f'{filename_prefix}_' if filename_prefix is not None else ''
    input_path = os.path.join(results_directory, f'{filename_prefix}tardis_input.txt')
    query_path = os.path.join(results_directory, f'{filename_prefix}tardis_query.txt')
    output_path = os.path.join(results_directory, f'{filename_prefix}tardis_output.csv')

    save_ndarray(points, input_path)
    save_ndarray(query_points, query_path)

    keep = 'k' if keep_terminal_open else 'c'
    n = points.shape[0]
    command = f'start cmd /{keep} \"cd \"{tardis_directory}\" & \"{activate_path}\" & ' \
              f'python cli.py \"{input_path}\" -k {neighborhood_size} -d {maximum_dimension} ' \
              f'--num-steps {n_steps} -b {n} > \"{output_path}\"\"'

    os.system(command)
    wait_until_completion(output_path)

    return output_path


def wait_until_completion(output_path):
    while not os.path.exists(output_path):
        continue

    completed = False
    while not completed:
        time.sleep(1)
        completed = os.path.getsize(output_path) != 0


def update_point_cloud(point_cloud, output_path):
    dataframe = load_csv(output_path)

    n_columns = len(dataframe.columns)
    dimensions = dataframe.iloc[:, (n_columns - 1)].values
    euclidicities = dataframe.iloc[:, (n_columns - 2)].values

    for query, dimension, euclidicity in zip(point_cloud.queries, dimensions, euclidicities):
        query.intrinsic_dimension = dimension
        query.euclidicity = euclidicity
