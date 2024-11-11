from typing import Dict, Any


class ValidationError(Exception):
    pass


class ValidationService:
    @staticmethod
    def validate_vehicle_data(data: Dict[str, Any]) -> bool:
        required_fields = ["vehicle_id"]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")

        # Validate VIN format
        vin = data["vehicle_id"]
        if not ValidationService._validate_vin(vin):
            raise ValidationError("Invalid VIN format")

        return True

    @staticmethod
    def validate_user_data(data: Dict[str, Any]) -> bool:
        required_fields = ["user_name", "user_phone"]

        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")

        # Validate phone number format
        if not ValidationService._validate_phone(data["user_phone"]):
            raise ValidationError("Invalid phone number format")

        return True

    @staticmethod
    def validate_feature_data(feature_type: str, data: Dict[str, Any]) -> bool:
        valid_features = ["cameras", "mirrors", "seats", "autonomous_driving"]

        if feature_type not in valid_features:
            raise ValidationError(
                f"Invalid feature type. Must be one of: {valid_features}"
            )

        if feature_type == "cameras":
            if "recording_is_active" not in data:
                raise ValidationError("Cameras data must include recording_is_active")

        elif feature_type == "mirrors":
            if "position" not in data:
                raise ValidationError("Mirrors data must include position")

        elif feature_type == "seats":
            required_seat_fields = [
                "driver_seat",
                "passenger_seat",
                "heating_is_active",
            ]
            for field in required_seat_fields:
                if field not in data:
                    raise ValidationError(f"Seats data must include {field}")

        elif feature_type == "autonomous_driving":
            required_fields = ["is_enabled", "version"]
            for field in required_fields:
                if field not in data:
                    raise ValidationError(
                        f"Autonomous driving data must include {field}"
                    )

        return True

    @staticmethod
    def _validate_vin(vin: str) -> bool:
        """Validate Vehicle Identification Number format"""
        return len(vin) == 17 and vin.isalnum()

    @staticmethod
    def _validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        import re

        pattern = r"^\+[1-9]\d{1,14}$"
        return bool(re.match(pattern, phone))
