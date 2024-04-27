from dataclasses import dataclass

from constants import Feature


@dataclass(frozen=True)
class NanoReviewInfo:
    name: str
    performance: int
    gaming: int
    display: int
    battery: int
    connectivity: int
    portability: int
    nano_score: int
    weight: float
    screen_to_body_ratio: int
    refresh_rate: int
    ppi: int
    max_brightness: int

    def to_features(self) -> dict[Feature, [float, int]]:
        return {
            Feature.NAME: self.name,
            Feature.PERFORMANCE: self.performance,
            Feature.GAMING: self.gaming,
            Feature.DISPLAY: self.display,
            Feature.BATTERY_LIFE: self.battery,
            Feature.CONNECTIVITY: self.connectivity,
            Feature.PORTABILITY: self.portability,
            Feature.NANO_SCORE: self.nano_score,
            Feature.WEIGHT: self.weight,
            Feature.SCREEN_TO_BODY_RATIO: self.screen_to_body_ratio,
            Feature.REFRESH_RATE: self.refresh_rate,
            Feature.PPI: self.ppi,
            Feature.MAX_BRIGHTNESS: self.max_brightness
        }
