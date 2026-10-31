from utils.main import *


class Query:

    def __init__(self, identifier, point, word=None, word_type=None):
        self._identifier = identifier
        self._point = point

        self._initial_intrinsic_dimension_estimates = None
        self._filtered_intrinsic_dimension_estimates = None
        self._intrinsic_dimension = None

        self._classification_estimates = None
        self._classification = None

        self._euclidicity_estimates = None
        self._euclidicity = None

        self._topological_polysemy_estimates = None
        self._topological_polysemy = None

        self._original_neighborhood_thickness = None
        self._translated_neighborhood_thickness = None

        self._neighborhood_variance = None

        self._word = word
        self._word_type = word_type

    @property
    def identifier(self):
        return self._identifier

    @property
    def point(self):
        return self._point

    @property
    def initial_intrinsic_dimension_estimates(self):
        return self._initial_intrinsic_dimension_estimates

    @property
    def filtered_intrinsic_dimension_estimates(self):
        return self._filtered_intrinsic_dimension_estimates

    @property
    def intrinsic_dimension(self):
        return self._intrinsic_dimension

    @intrinsic_dimension.setter
    def intrinsic_dimension(self, intrinsic_dimension):
        self._intrinsic_dimension = intrinsic_dimension

    @property
    def classification_estimates(self):
        return self._classification_estimates

    @property
    def classification(self):
        return self._classification

    @classification.setter
    def classification(self, classification):
        self._classification = classification

    @property
    def euclidicity(self):
        return self._euclidicity

    @euclidicity.setter
    def euclidicity(self, euclidicity):
        self._euclidicity = euclidicity

    @property
    def topological_polysemy(self):
        return self._topological_polysemy

    @topological_polysemy.setter
    def topological_polysemy(self, topological_polysemy):
        self._topological_polysemy = topological_polysemy

    @property
    def original_neighborhood_thickness(self):
        return self._original_neighborhood_thickness

    @original_neighborhood_thickness.setter
    def original_neighborhood_thickness(self, original_neighborhood_thickness):
        self._original_neighborhood_thickness = original_neighborhood_thickness

    @property
    def translated_neighborhood_thickness(self):
        return self._translated_neighborhood_thickness

    @translated_neighborhood_thickness.setter
    def translated_neighborhood_thickness(self, translated_neighborhood_thickness):
        self._translated_neighborhood_thickness = translated_neighborhood_thickness

    @property
    def neighborhood_variance(self):
        return self._neighborhood_variance

    @neighborhood_variance.setter
    def neighborhood_variance(self, neighborhood_variance):
        self._neighborhood_variance = neighborhood_variance

    @property
    def word(self):
        return self._word

    @property
    def word_type(self):
        return self._word_type

    def process_intrinsic_dimension_estimates(self, initial_intrinsic_dimension_estimates):
        self._initial_intrinsic_dimension_estimates = initial_intrinsic_dimension_estimates
        self._filter_intrinsic_dimension_estimates()
        self._calculate_intrinsic_dimension()

    def _filter_intrinsic_dimension_estimates(self):
        sorted_estimates = sorted(self._initial_intrinsic_dimension_estimates.items(), key=lambda item: item[1])
        n_estimates = len(sorted_estimates)
        quartile_index = n_estimates // 4

        if quartile_index == 0:
            self._filtered_intrinsic_dimension_estimates = self._initial_intrinsic_dimension_estimates
        else:
            filtered_estimates = dict(sorted_estimates[quartile_index:(-quartile_index)])
            filtered_estimates = dict(sorted(filtered_estimates.items(), key=lambda item: item[0]))
            self._filtered_intrinsic_dimension_estimates = filtered_estimates

    def _calculate_intrinsic_dimension(self):
        estimates = self._filtered_intrinsic_dimension_estimates.values()
        intrinsic_dimension = sum(estimates) / len(estimates)

        self._intrinsic_dimension = intrinsic_dimension

    def process_classification_estimates(self, classification_estimates):
        self._classification_estimates = classification_estimates

        unique_values, counts = np.unique(list(classification_estimates.values()), return_counts=True)
        index_most_common_value = np.argmax(counts)
        self._classification = unique_values[index_most_common_value]

    def process_euclidicity_estimates(self, euclidicity_estimates):
        self._euclidicity_estimates = euclidicity_estimates
        self._euclidicity = sum(euclidicity_estimates.values()) / len(euclidicity_estimates)

    def process_topological_polysemy_estimates(self, topological_polysemy_estimates):
        self._topological_polysemy_estimates = topological_polysemy_estimates
        self._topological_polysemy = sum(topological_polysemy_estimates.values()) / len(topological_polysemy_estimates)
