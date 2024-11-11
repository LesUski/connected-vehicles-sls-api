from pynamodb.attributes import (
    UnicodeAttribute,
    MapAttribute,
    NumberAttribute,
    BooleanAttribute,
)


class PositionAttribute(MapAttribute):
    x = NumberAttribute()
    y = NumberAttribute()
    z = NumberAttribute()


class SeatAttribute(MapAttribute):
    cusion_1 = NumberAttribute()
    temperature = NumberAttribute()
    x = NumberAttribute()
    y = NumberAttribute()
    z = NumberAttribute()


class SeatsMapAttribute(MapAttribute):
    driver_seat = MapAttribute(of=SeatAttribute)
    passenger_seat = MapAttribute(of=SeatAttribute)
    heating_is_active = BooleanAttribute()
    position_is_active = BooleanAttribute()


class CamerasMapAttribute(MapAttribute):
    cameras = MapAttribute()
    recording_is_active = BooleanAttribute()


class MirrorsPositionAttribute(MapAttribute):
    left = MapAttribute(of=PositionAttribute)
    right = MapAttribute(of=PositionAttribute)
    is_active = BooleanAttribute()


class MirrorsMapAttribute(MapAttribute):
    position = MapAttribute(of=MirrorsPositionAttribute)


class AutonomousDrivingMapAttribute(MapAttribute):
    is_enabled = BooleanAttribute()
    version = UnicodeAttribute()
