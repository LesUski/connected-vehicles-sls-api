from pynamodb.attributes import UnicodeAttribute, MapAttribute
from .base import BaseModel
from .attributes import (
    SeatsMapAttribute,
    CamerasMapAttribute,
    MirrorsMapAttribute,
    AutonomousDrivingMapAttribute,
)


class VehicleModel(BaseModel):
    vehicle_id = UnicodeAttribute(null=True)
    torque = UnicodeAttribute(null=True)
    drivetrain = UnicodeAttribute(null=True)
    engine = UnicodeAttribute(null=True)
    horsepower = UnicodeAttribute(null=True)
    mirrors = MapAttribute(of=MirrorsMapAttribute, null=True)
    seats = MapAttribute(of=SeatsMapAttribute, null=True)
    cameras = MapAttribute(of=CamerasMapAttribute, null=True)
    autonomous_driving = MapAttribute(of=AutonomousDrivingMapAttribute, null=True)

    @staticmethod
    def get_vehicle_meta(vin: str):
        return VehicleModel.get(f"VIN#{vin}", "#META#")

    @staticmethod
    def get_vehicle_feature(vin: str, feature: str):
        return VehicleModel.get(f"VIN#{vin}", f"FEATURE#{feature.upper()}")
