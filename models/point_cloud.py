from utils.main import *
from models.query import Query


class PointCloud:

    def __init__(self):
        self._points = None
        self._tree = None
        self._queries = None

    def random_constructor(self, points, n_queries, seed=None):
        np.random.seed(seed)

        self._points = points
        self._tree = KDTree(points)

        identifiers = range(n_queries)
        n_points = points.shape[0]
        indices = np.random.choice(a=n_points, size=n_queries, replace=False)
        query_points = points[indices]
        queries = [Query(identifier, point) for identifier, point in zip(identifiers, query_points)]

        self._queries = queries

    def non_random_constructor(self, points, query_points):
        self._points = points
        self._tree = KDTree(points)

        n_query_points = query_points.shape[0]
        identifiers = range(n_query_points)
        if len(query_points.shape) != 1:
            queries = [Query(identifier, point) for identifier, point in zip(identifiers, query_points)]
        else:
            queries = [Query(0, query_points)]

        self._queries = queries

    def embeddings_constructor(self, embeddings_path, neighborhood_size, query_words_path=words_path,
                               filter_word_embeddings=True):
        embeddings = load_embeddings(embeddings_path)
        embeddings.unit_normalize_all()

        if filter_word_embeddings:
            embeddings = filter_embeddings(embeddings)

        query_words = load_csv(query_words_path)
        keys = list(query_words['Word'])
        types = list(query_words['Type'])

        identifiers = range(len(keys))
        query_points = [embeddings[key] for key in keys]
        queries = [Query(identifier, point, word, word_type) for identifier, point, word, word_type in
                   zip(identifiers, query_points, keys, types)]

        point_keys = set()
        for i in range(len(query_points)):
            point = query_points[i]
            most_similar = embeddings.similar_by_vector(vector=point, topn=(neighborhood_size + 1))
            most_similar_keys = [key for key, similarity in most_similar]
            point_keys.update(most_similar_keys)
        points = np.array([embeddings[key] for key in point_keys])

        self._points = points
        self._tree = KDTree(points)
        self._queries = queries

    @property
    def points(self):
        return self._points

    @property
    def queries(self):
        return self._queries

    @queries.setter
    def queries(self, queries):
        self._queries = queries

    def get_query_points(self):
        query_points = np.array([query.point for query in self._queries])
        return query_points

    def _get_distances_and_indices(self, neighborhood_size):
        query_points = self.get_query_points()
        distances, indices = self._tree.query(X=query_points, k=(neighborhood_size + 1))

        indices = np.array([
            indices[i][1:] if distances[i][0] == 0 else indices[i][:-1] for i in range(len(indices))
        ])
        distances = np.array([
            distances[i][1:] if distances[i][0] == 0 else distances[i][:-1] for i in range(len(distances))
        ])
        return distances, indices

    def get_neighborhoods(self, neighborhood_size):
        distances, indices = self._get_distances_and_indices(neighborhood_size)

        neighborhoods = self._points[indices]
        return neighborhoods

    def _get_annulus(self, point, s, r):
        large_ball_indices = self._tree.query_radius(X=point.reshape(1, -1), r=s)[0]
        small_ball_indices = self._tree.query_radius(X=point.reshape(1, -1), r=r)[0]
        annulus_indices = np.setdiff1d(ar1=large_ball_indices, ar2=small_ball_indices)

        annulus = (self._points[annulus_indices], s, r)
        return annulus

    def get_annuli(self, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
        if None in [min_to_max_s_ratio, r_to_s_ratio]:
            return self.get_annuli1(neighborhood_size, n_steps)
        else:
            return self.get_annuli2(neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps)

    def get_annuli1(self, neighborhood_size, n_steps):
        distances, indices = self._get_distances_and_indices(neighborhood_size)
        radii = [[d[0], d[neighborhood_size // 3 - 1], d[-1]] for d in distances]

        annuli = list()
        for point, point_radii in zip(self.get_query_points(), radii):
            point_annuli = list()

            for s in np.linspace(start=point_radii[1], stop=point_radii[2], num=n_steps):
                for r in np.linspace(start=point_radii[0], stop=point_radii[1], num=n_steps):
                    if r < s:
                        point_annuli.append(self._get_annulus(point, s, r))

            annuli.append(point_annuli)
        return annuli

    def get_annuli2(self, neighborhood_size, min_to_max_s_ratio, r_to_s_ratio, n_steps):
        distances, indices = self._get_distances_and_indices(neighborhood_size)
        neighborhoods_radius = [d[-1] for d in distances]

        annuli = list()
        for point, neighborhood_radius in zip(self.get_query_points(), neighborhoods_radius):
            min_neighborhood_radius = min_to_max_s_ratio * neighborhood_radius if n_steps > 1 else neighborhood_radius

            point_annuli = list()
            for s in np.linspace(start=min_neighborhood_radius, stop=neighborhood_radius, num=n_steps):
                r = r_to_s_ratio * s
                point_annuli.append(self._get_annulus(point, s, r))

            annuli.append(point_annuli)

        return annuli
