from typing import List, Union
import random


class Method:
    def __init__(self, x: float, y: float, z: float, lon: float, lat: float, name: str):
        self.x = x
        self.y = y
        self.z = z
        self.lon = lon
        self.lat = lat
        self.name = name
        self.depth_top = None  # Initialize with None
        self.depth_base = None  # Initialize with None

    def add_depth(self, depth_top: float, depth_base: float):
        self.depth_top = depth_top
        self.depth_base = depth_base
        self.predict()

    def predict(self):
        self.predictions = self.predict_soil_layers(num_splits=2)

    def predict_soil_layers(
        self, num_splits=2, types=["sand", "clay", "silt", "quick_clay"]
    ):
        if self.depth_base is None or self.depth_top is None:
            return []
        split_depth = (self.depth_base - self.depth_top) / num_splits
        current_depth = self.depth_top

        predictions = []
        for _ in range(num_splits):
            next_depth = current_depth + split_depth
            if next_depth > self.depth_base:
                next_depth = self.depth_base

            soil_type = random.choice(types)
            predictions.append(
                {
                    "start": self.z - current_depth,
                    "end": self.z - next_depth,
                    "x": self.x,
                    "y": self.y,
                    "soil_type": soil_type,
                }
            )

            current_depth = next_depth
        return predictions


def get_methods(locations, method_types: list[int] = None) -> List[str]:
    method_result = []
    for location in locations:
        method = Method(
            x=location["point_easting"],
            y=location["point_northing"],
            z=location["point_z"] if location["point_z"] else 0,
            lon=location["point_x_wgs84_web"],
            lat=location["point_y_wgs84_web"],
            name=location["name"],
        )
        if "methods" in location and location["methods"]:
            if method_types is not None:
                valid_method = get_valid_method(location["methods"], method_types)
                if valid_method:
                    method.add_depth(
                        valid_method["depth_top"], valid_method["depth_base"]
                    )
                    method_result.append(method)
            else:
                valid_method = get_valid_method(location["methods"])
                if valid_method:
                    method.add_depth(
                        valid_method["depth_top"], valid_method["depth_base"]
                    )
                    method_result.append(method)

    return method_result


def get_valid_method(
    methods: dict,
    method_types: list[int] = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
    ],
) -> Union[dict, None]:
    for method in methods:
        if method["method_type_id"] in method_types:
            if method["depth_top"] and method["depth_base"]:
                return method
    return None
