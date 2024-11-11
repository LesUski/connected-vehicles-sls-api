# Create a vehicle
$vehicleBody = @{
    vehicle_id = "WDDJK7DA4FF954840"
    torque = "308"
    drivetrain = "4WD"
    engine = "gasoline"
    horsepower = "406"
} | ConvertTo-Json

$createVehicleParams = @{
    Method = "POST"
    Uri = "http://localhost:3000/vehicles"
    ContentType = "application/json"
    Body = $vehicleBody
}

Invoke-RestMethod @createVehicleParams

# Create a vehicle feature
$featureBody = @{
    feature_type = "cameras"
    feature_data = @{
        cameras = @{
            front_camera_center = @{
                foo = "bar"
            }
        }
        recording_is_active = $true
    }
} | ConvertTo-Json -Depth 10

$createFeatureParams = @{
    Method = "POST"
    Uri = "http://localhost:3000/vehicles/WDDJK7DA4FF954840/features"
    ContentType = "application/json"
    Body = $featureBody
}

Invoke-RestMethod @createFeatureParams