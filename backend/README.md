# GPS Tracker Backend (Django + DRF)

## Setup
```
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## IoT GPS API
- Base: `/api/iot/`
- Endpoints:
  - `GET /api/iot/gps/` list all GPS records
  - `POST /api/iot/gps/` create GPS record
  - `GET /api/iot/gps/{id}/` retrieve record
  - `PUT /api/iot/gps/{id}/` update record
  - `DELETE /api/iot/gps/{id}/` delete record

### Sample cURL
```
curl -X POST http://localhost:8000/api/iot/gps/ \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device-123",
    "latitude": 37.422,
    "longitude": -122.084
  }'
```

## Docs
See `API_DOCUMENTATION.md` for detailed API reference.
