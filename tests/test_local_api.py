"""Test local API endpoints"""

import pytest
import requests

BASE_URL = "http://localhost:4000"


def test_create_vehicle():
    """Test vehicle creation endpoint"""
    vehicle_data = {
        "vehicle_id": "WDDJK7DA4FF954840",
        "torque": "308",
        "drivetrain": "4WD",
        "engine": "gasoline",
        "horsepower": "406",
    }

    response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data)

    assert response.status_code == 202
    data = response.json()
    assert "executionArn" in data


def test_create_vehicle_feature():
    """Test vehicle feature creation endpoint"""
    feature_data = {
        "feature_type": "cameras",
        "feature_data": {
            "cameras": {"front_camera_center": {"foo": "bar"}},
            "recording_is_active": True,
        },
    }

    response = requests.post(
        f"{BASE_URL}/vehicles/WDDJK7DA4FF954840/features", json=feature_data
    )

    assert response.status_code == 202
    data = response.json()
    assert "executionArn" in data


if __name__ == "__main__":
    import subprocess
    import time

    # Start serverless offline in background
    process = subprocess.Popen(
        ["serverless", "offline", "start", "--stage", "local"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for server to start
    time.sleep(5)

    try:
        # Run tests
        pytest.main([__file__])
    finally:
        # Cleanup
        process.terminate()
