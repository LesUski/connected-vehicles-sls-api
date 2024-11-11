from typing import Dict, Any
from pynamodb.exceptions import PutError
from src.models.vehicle import VehicleModel


class DynamoDBService:
    @staticmethod
    def create_vehicle(vehicle_data: Dict[str, Any]) -> Dict[str, Any]:
        vin = vehicle_data["vehicle_id"]

        vehicle = VehicleModel(PK=f"VIN#{vin}", SK="#META#", **vehicle_data)

        try:
            vehicle.save()
            return {"status": "success", "message": "Vehicle created successfully"}
        except PutError as e:
            raise Exception(f"Failed to create vehicle: {str(e)}")

    @staticmethod
    def create_vehicle_feature(
        vin: str, feature_type: str, feature_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        vehicle_feature = VehicleModel(
            PK=f"VIN#{vin}",
            SK=f"FEATURE#{feature_type.upper()}",
            **{feature_type: feature_data},
        )

        try:
            vehicle_feature.save()
            return {
                "status": "success",
                "message": f"Vehicle {feature_type} feature created successfully",
            }
        except PutError as e:
            raise Exception(f"Failed to create vehicle feature: {str(e)}")
