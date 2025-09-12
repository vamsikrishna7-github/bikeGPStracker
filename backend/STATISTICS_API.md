# GPS Statistics API Endpoints

This document describes the statistics endpoints for GPS tracking data analysis.

## Base URL
All endpoints are prefixed with `/iot/statistics/`

## Endpoints

### 1. General Device Statistics
**GET** `/iot/statistics/{device_id}/`

Get comprehensive statistics for a specific device over a configurable time period.

#### Query Parameters:
- `period` (optional): Time period - `day`, `week`, `month`, or `year` (default: `day`)
- `start_date` (optional): Start date in ISO format (e.g., `2024-01-01T00:00:00Z`)
- `end_date` (optional): End date in ISO format (e.g., `2024-01-31T23:59:59Z`)

#### Example Requests:
```
GET /iot/statistics/device123/?period=day
GET /iot/statistics/device123/?period=week
GET /iot/statistics/device123/?start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z
```

#### Response:
```json
{
  "device_id": "device123",
  "period": "day",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-01-01T23:59:59Z",
  "total_records": 1440,
  "total_distance_km": 45.67,
  "average_speed_kmh": 32.5,
  "max_speed_kmh": 85.2,
  "total_idle_time_hours": 2.5,
  "total_moving_time_hours": 21.5,
  "ignition_on_count": 1200,
  "ignition_off_count": 240,
  "route_points": [
    {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "timestamp": "2024-01-01T00:00:00Z",
      "speed": 0.0,
      "ignition": true
    }
  ]
}
```

### 2. Daily Statistics
**GET** `/iot/statistics/{device_id}/daily/`

Get daily breakdown of statistics over a date range.

#### Query Parameters:
- `start_date` (required): Start date in ISO format
- `end_date` (required): End date in ISO format

#### Example Request:
```
GET /iot/statistics/device123/daily/?start_date=2024-01-01T00:00:00Z&end_date=2024-01-07T23:59:59Z
```

#### Response:
```json
[
  {
    "date": "2024-01-01",
    "total_distance_km": 45.67,
    "average_speed_kmh": 32.5,
    "max_speed_kmh": 85.2,
    "total_idle_time_hours": 2.5,
    "total_moving_time_hours": 21.5,
    "route_points": [...]
  }
]
```

### 3. Weekly Statistics
**GET** `/iot/statistics/{device_id}/weekly/`

Get weekly breakdown of statistics with daily details.

#### Query Parameters:
- `start_date` (required): Start date in ISO format
- `end_date` (required): End date in ISO format

#### Example Request:
```
GET /iot/statistics/device123/weekly/?start_date=2024-01-01T00:00:00Z&end_date=2024-01-31T23:59:59Z
```

#### Response:
```json
[
  {
    "week_start": "2024-01-01",
    "week_end": "2024-01-07",
    "total_distance_km": 320.45,
    "average_speed_kmh": 35.2,
    "max_speed_kmh": 95.8,
    "total_idle_time_hours": 15.5,
    "total_moving_time_hours": 152.5,
    "daily_breakdown": [
      {
        "date": "2024-01-01",
        "total_distance_km": 45.67,
        "average_speed_kmh": 32.5,
        "max_speed_kmh": 85.2,
        "total_idle_time_hours": 2.5,
        "total_moving_time_hours": 21.5,
        "route_points": [...]
      }
    ]
  }
]
```

### 4. Monthly Statistics
**GET** `/iot/statistics/{device_id}/monthly/`

Get monthly breakdown of statistics with weekly details.

#### Query Parameters:
- `year` (optional): Year (default: current year)

#### Example Request:
```
GET /iot/statistics/device123/monthly/?year=2024
```

#### Response:
```json
[
  {
    "month": 1,
    "year": 2024,
    "total_distance_km": 1250.78,
    "average_speed_kmh": 38.5,
    "max_speed_kmh": 120.3,
    "total_idle_time_hours": 65.2,
    "total_moving_time_hours": 654.8,
    "weekly_breakdown": [
      {
        "week_start": "2024-01-01",
        "week_end": "2024-01-07",
        "total_distance_km": 320.45,
        "average_speed_kmh": 35.2,
        "max_speed_kmh": 95.8,
        "total_idle_time_hours": 15.5,
        "total_moving_time_hours": 152.5,
        "daily_breakdown": [...]
      }
    ]
  }
]
```

### 5. Yearly Statistics
**GET** `/iot/statistics/{device_id}/yearly/`

Get yearly breakdown of statistics with monthly details.

#### Query Parameters:
- `start_year` (optional): Start year (default: previous year)
- `end_year` (optional): End year (default: current year)

#### Example Request:
```
GET /iot/statistics/device123/yearly/?start_year=2023&end_year=2024
```

#### Response:
```json
[
  {
    "year": 2024,
    "total_distance_km": 15000.45,
    "average_speed_kmh": 42.3,
    "max_speed_kmh": 135.7,
    "total_idle_time_hours": 780.5,
    "total_moving_time_hours": 7850.2,
    "monthly_breakdown": [
      {
        "month": 1,
        "year": 2024,
        "total_distance_km": 1250.78,
        "average_speed_kmh": 38.5,
        "max_speed_kmh": 120.3,
        "total_idle_time_hours": 65.2,
        "total_moving_time_hours": 654.8,
        "weekly_breakdown": [...]
      }
    ]
  }
]
```

## Statistics Fields Explained

- **total_records**: Total number of GPS data points
- **total_distance_km**: Total distance traveled in kilometers (calculated using Haversine formula)
- **average_speed_kmh**: Average speed in km/h
- **max_speed_kmh**: Maximum speed recorded in km/h
- **total_idle_time_hours**: Total time when vehicle was idle (speed < 5 km/h or ignition off)
- **total_moving_time_hours**: Total time when vehicle was moving
- **ignition_on_count**: Number of records with ignition on
- **ignition_off_count**: Number of records with ignition off
- **route_points**: Array of GPS coordinates for mapping/route visualization

## Use Cases

### For Graphs and Charts:
- Use daily/weekly/monthly endpoints for time-series data
- Plot distance, speed, idle time trends over time
- Create speed distribution charts
- Generate fuel efficiency reports

### For Route Visualization:
- Use `route_points` array to plot GPS tracks on maps
- Filter by date ranges for specific trips
- Overlay speed and ignition data on route maps

### For Fleet Management:
- Compare statistics across multiple devices
- Monitor driver behavior (speeding, idle time)
- Track vehicle utilization and efficiency
- Generate compliance reports

## Error Responses

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Device not found
- `500`: Internal server error

Error response format:
```json
{
  "error": "Error message description"
}
```
