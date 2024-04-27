from enum import Enum


class CriteriaType(Enum):
    MAX = "MAX"
    MIN = "MIN"


class Feature(Enum):
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


class FeatureToCriteriaType(Enum):
    PERFORMANCE = CriteriaType.MAX
    GAMING = CriteriaType.MAX
    DISPLAY = CriteriaType.MAX
    BATTERY_LIFE = CriteriaType.MAX
    CONNECTIVITY = CriteriaType.MAX
    PORTABILITY = CriteriaType.MAX
    NANO_SCORE = CriteriaType.MAX
    WEIGHT = CriteriaType.MIN
    SCREEN_TO_BODY_RATIO = CriteriaType.MAX
    REFRESH_RATE = CriteriaType.MAX
    PPI = CriteriaType.MAX
    MAX_BRIGHTNESS = CriteriaType.MAX
