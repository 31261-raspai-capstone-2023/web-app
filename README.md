# web-app

Web app for raspai capstone

Demo to find car location based on entering a number plate

## Setup Dev environment
### Python virtual environment
Use Python 3.11.5

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
pip install -r requirements-dev.txt
```

### Running the app
```bash
python -m web_app.server --debug
```

## Prod environment
Build the image
```bash
docker build . -t licence_system/web_app:latest
```

Run the container
```bash
docker run -d -p 5000:5000 licence_system/web_app:latest
```

Accessible via http://localhost:5000/

You will need to add a camera, then use this Camera ID returned as the camera_id when adding a plate to a location.

## API Usage
### Add a camera
```bash
curl -H "Content-Type: application/json" -X POST -d '{"location": "B1"}' http://127.0.0.1:5000/add_camera
```

### Register a car entering the carpark
```bash
curl -H "Content-Type: application/json" -X POST -d '{"plate": "DEEZ-NUTS"}' http://127.0.0.1:5000/enter_carpark
```

### Register a car exiting the carpark
```bash
curl -H "Content-Type: application/json" -X POST -d '{"plate": "DEEZ-NUTS"}' http://127.0.0.1:5000/exit_carpark
```

### Add a car to a location
```bash
curl -H "Content-Type: application/json" -X POST -d '{"plate": "DEEZ-NUTS", "camera_id": 1}' http://127.0.0.1:5000/add_location_entry
```

### Get Car info
```bash
curl http://127.0.0.1:5000/get_car_info/DEEZ-NUTS
```