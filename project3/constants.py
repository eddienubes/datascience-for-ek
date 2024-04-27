from enum import Enum


class CriteriaType(Enum):
    MAX = "MAX"
    MIN = "MIN"
    NONE = "NONE"


class Feature(Enum):
    """
    Preserve the order of keys here.
    """
    NAME = "NAME"
    PERFORMANCE = "PERFORMANCE"
    GAMING = "GAMING"
    DISPLAY = "DISPLAY"
    BATTERY_LIFE = "BATTERY_LIFE"
    CONNECTIVITY = "CONNECTIVITY"
    PORTABILITY = "PORTABILITY"
    NANO_SCORE = "NANO_SCORE"
    WEIGHT = "WEIGHT"
    SCREEN_TO_BODY_RATIO = "SCREEN_TO_BODY_RATIO"
    REFRESH_RATE = "REFRESH_RATE"
    PPI = "PPI"
    MAX_BRIGHTNESS = "MAX_BRIGHTNESS"


FEATURE_TO_CRITERIA_TYPE = {
    Feature.NAME: CriteriaType.NONE,
    Feature.PERFORMANCE: CriteriaType.MAX,
    Feature.GAMING: CriteriaType.MAX,
    Feature.DISPLAY: CriteriaType.MAX,
    Feature.BATTERY_LIFE: CriteriaType.MAX,
    Feature.CONNECTIVITY: CriteriaType.MAX,
    Feature.PORTABILITY: CriteriaType.MAX,
    Feature.NANO_SCORE: CriteriaType.MAX,
    Feature.WEIGHT: CriteriaType.MIN,
    Feature.SCREEN_TO_BODY_RATIO: CriteriaType.MAX,
    Feature.REFRESH_RATE: CriteriaType.MAX,
    Feature.PPI: CriteriaType.MAX,
    Feature.MAX_BRIGHTNESS: CriteriaType.MAX
}

ACTIVE_FEATURES = [feature for feature in Feature if FEATURE_TO_CRITERIA_TYPE[feature] != CriteriaType.NONE]