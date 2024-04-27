import numpy as np

from project3.constants import Feature


class Evaluator:
    def __init__(self):
        """
        Initialize evaluator
        """
        self.__feature_matrix = np.empty((0, len(Feature)))

    def add(self, features: dict) -> None:
        """
        Add a feature vector to the evaluator

        :param features: info from nano review api
        """
        feature_vector = np.zeros(0)

        for feature in Feature:
            value = features.get(feature.name, None)

            if value is None:
                raise ValueError(f"Missing feature {feature.name}")

            feature_vector = np.append(feature_vector, features[feature.name])

        self.__feature_matrix = np.vstack((self.__feature_matrix, feature_vector))

    def normalize(self) -> None:
        min_vals = self.__feature_matrix.min(axis=0)
        
        


eval = Evaluator()
eval.add({'name': 'Acer Aspire 3', 'price': 500, 'rating': 4.5, 'reviews': 1000})
