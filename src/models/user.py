from base import BaseModel
from attributes import (
    UnicodeAttribute,
    MapAttribute,
    SeatsMapAttribute,
    CamerasMapAttribute,
    MirrorsMapAttribute,
    AutonomousDrivingMapAttribute,
)


class UserModel(BaseModel):
    user_name = UnicodeAttribute(null=True)
    user_phone = UnicodeAttribute(null=True)
    mirrors = MapAttribute(of=MirrorsMapAttribute, null=True)
    seats = MapAttribute(of=SeatsMapAttribute, null=True)
    cameras = MapAttribute(of=CamerasMapAttribute, null=True)
    autonomous_driving = MapAttribute(of=AutonomousDrivingMapAttribute, null=True)
    expiration_date = UnicodeAttribute(null=True)
    expiration_ttl = UnicodeAttribute(null=True)

    @staticmethod
    def get_user_meta(user_id: str):
        return UserModel.get(f"ID#{user_id}", "#META#")

    @staticmethod
    def get_user_preferences(user_id: str, feature: str):
        return UserModel.get(f"ID#{user_id}", f"PREFERENCES#{feature.upper()}")
