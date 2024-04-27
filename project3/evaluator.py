import numpy as np

from project3.constants import Feature, FEATURE_TO_CRITERIA_TYPE, CriteriaType, ACTIVE_FEATURES


class Evaluator:
    def __init__(self):
        """
        Initialize evaluator
        """
        self.__feature_matrix = np.empty((0, len(ACTIVE_FEATURES)))
        # Metadata for each model
        self.__meta = dict()
        self.__meta_inverted = dict()
        self.__exhausted = False

    def add(self, features: dict) -> None:
        """
        Add a feature vector to the evaluator

        :param features: info from nano review api
        """
        feature_vector = list()

        for feature in ACTIVE_FEATURES:
            value = features.get(feature, None)

            if value is None:
                raise ValueError(f"Missing feature {feature.name}")

            feature_vector.append(value)

        self.__feature_matrix = np.vstack((self.__feature_matrix, feature_vector))

        # Mark laptop features to its name
        current_idx = len(self.__feature_matrix) - 1
        self.__meta[features[Feature.NAME]] = current_idx
        self.__meta_inverted[current_idx] = features[Feature.NAME]

    @staticmethod
    def normalize(matrix: np.ndarray) -> np.ndarray:
        min_vals = matrix.min(axis=0)
        max_vals = matrix.max(axis=0)

        range_vals = max_vals - min_vals
        range_vals[range_vals == 0] = 1

        return (matrix - min_vals) / range_vals

    def run(self):
        if not len(self.__feature_matrix):
            raise ValueError('There is nothing to evaluate')

        if self.__exhausted:
            raise ValueError('Evaluator is exhausted, please create new instance')

        self.__feature_matrix = self.normalize(self.__feature_matrix)

        row_sums = list()
        # Small number to avoid divisions by zero
        # E.g. every item's weight value is shifted by epsilon
        epsilon = 1

        for row in self.__feature_matrix:
            total = 0
            for idx, feature in enumerate(ACTIVE_FEATURES):
                if FEATURE_TO_CRITERIA_TYPE[feature] == CriteriaType.MAX:
                    total += row[idx]
                if FEATURE_TO_CRITERIA_TYPE[feature] == CriteriaType.MIN:
                    total += (1 / (row[idx] + epsilon))

            row_sums.append(total)

        # sort in ascending order
        sorted_indices = sorted(range(len(row_sums)), key=lambda k: row_sums[k])

        best = self.__meta_inverted[sorted_indices[-1]]
        worst = self.__meta_inverted[sorted_indices[0]]
        diff = row_sums[sorted_indices[-1]] - row_sums[sorted_indices[0]]

        percentage = diff / row_sums[sorted_indices[-1]]

        return {
            'best': best,
            'worst': worst,
            'diff': diff,
            'percentage': percentage
        }
