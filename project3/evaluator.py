import numpy as np

from project3.constants import Feature, FEATURE_TO_CRITERIA_TYPE, CriteriaType


class Evaluator:
    def __init__(self):
        """
        Initialize evaluator
        """
        self.__feature_matrix = np.empty((0, len(Feature)))
        # Name to features map
        self.__models = dict()

    def add(self, features: dict) -> None:
        """
        Add a feature vector to the evaluator

        :param features: info from nano review api
        """
        feature_vector = np.zeros(len(Feature))

        for idx, feature in enumerate(Feature):
            if FEATURE_TO_CRITERIA_TYPE[feature] == CriteriaType.NONE:
                continue

            value = features.get(feature, None)

            if value is None:
                raise ValueError(f"Missing feature {feature.name}")

            feature_vector[idx] = value

        self.__feature_matrix = np.vstack((self.__feature_matrix, feature_vector))
        self.__feature_matrix = self.normalize(self.__feature_matrix)

        # Mark laptop features to its name
        self.__models[features[Feature.NAME]] = len(self.__feature_matrix - 1)

    @staticmethod
    def normalize(matrix: np.ndarray) -> np.ndarray:
        min_vals = matrix.min(axis=0)
        max_vals = matrix.max(axis=0)

        range_vals = max_vals - min_vals
        range_vals[range_vals == 0] = 1

        return (matrix - min_vals) / range_vals
